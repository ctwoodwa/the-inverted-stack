# Appendix A — Sync Daemon Wire Protocol

<!-- icm/draft -->

<!-- Target: ~2,000 words -->
<!-- Source: v13 §6.2, Sunfish accelerators/anchor/README.md -->

---

## A.1 Overview

The sync daemon communicates over Unix domain sockets on Linux, macOS, and Windows 10 / Server 2019 and later, where kernel-level Unix domain socket support was introduced. All messages use binary CBOR encoding with a 4-byte length prefix. The protocol defines five message types that participate in the handshake sequence; once the handshake completes, the connection transitions to continuous delta streaming. The daemon initiates with HELLO, negotiates capabilities with CAPABILITY_NEG, and receives an ACK from the relay or peer before streaming begins. DELTA_STREAM messages carry CRDT operations for the lifetime of the connection. GOSSIP_PING messages flow on a 30-second interval to maintain membership state. Error messages terminate or pause a connection at any point in the lifecycle.

---

## A.2 Message Framing

Every message on the wire consists of a 4-byte little-endian `uint32` length prefix followed immediately by a CBOR-encoded message body of exactly that many bytes.

```
+------------------+-------------------------------+
| length: uint32   | body: CBOR map (length bytes)  |
| (little-endian)  |                               |
+------------------+-------------------------------+
```

The maximum allowed body size is 4,194,304 bytes (4 MiB). A receiver that encounters a length prefix exceeding this limit MUST close the connection without sending an error message. Receivers MUST read the full `length` bytes before decoding; partial reads are a protocol error.

Every CBOR body is a CBOR map. Every map contains a `type` field (tstr) that identifies the message type. Receivers MUST ignore unknown fields in any map; this rule enables optional fields to be added in minor protocol versions without breaking existing implementations.

---

## A.3 Handshake Messages

The handshake sequence is: **HELLO → CAPABILITY_NEG → ACK**. The connecting node sends HELLO immediately after the transport connection is established. The peer or relay responds with CAPABILITY_NEG. The relay then sends ACK. Streaming begins after ACK.

### A.3.1 HELLO

Sent by the connecting node as the first message on every new connection.

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `type` | tstr | required | Literal value `"HELLO"` |
| `node_id` | bstr | required | Ed25519 public key of the sending node, exactly 32 bytes |
| `schema_version` | tstr | required | Semver string (e.g. `"1.4.2"`) identifying the application schema version |
| `supported_versions` | array of tstr | required | All wire protocol semver strings this node can speak, for rolling-upgrade negotiation |
| `protocol_version` | uint | required | Wire protocol version. Current value: `1` |

`node_id` is the stable identity of the node across reconnections. The relay uses it as the lookup key for attestation and lease state. Nodes MUST NOT rotate their `node_id` without re-onboarding.

`supported_versions` MUST include the semver string corresponding to `protocol_version`. It MAY include older versions to allow a two-version overlap during rolling upgrades. See §A.7 for the compatibility policy.

### A.3.2 CAPABILITY_NEG

Sent by the connecting node immediately after HELLO, in the same connection. The relay does not respond to HELLO before CAPABILITY_NEG arrives; it buffers HELLO and waits for CAPABILITY_NEG to construct the full request context.

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `type` | tstr | required | Literal value `"CAPABILITY_NEG"` |
| `crdt_streams` | array of tstr | required | Stream identifiers for which the node requests CRDT delta subscription |
| `cp_leases` | array of tstr | optional | Record type identifiers for which the node requests CP-class lease capability |
| `bucket_subscriptions` | array of tstr | required | Sync bucket names the node requests access to |
| `attestation_bundle` | bstr | required | CBOR-encoded `AttestationBundle` (see §A.6) proving the node's role |

`crdt_streams` identifies the CRDT document streams by string key. Stream identifiers are application-defined and MUST be stable across reconnections. The relay validates each stream identifier against the role claims in `attestation_bundle` before granting access.

`cp_leases` is omitted when the node does not require CP-class (strongly-consistent) record access. When present, the relay acquires Flease-based distributed leases on behalf of the node before returning ACK.

`bucket_subscriptions` names the sync buckets defined in the application's bucket manifest. The relay grants only the subset the node's role attestation authorises.

### A.3.3 ACK

Sent by the relay after validating HELLO and CAPABILITY_NEG. A single ACK closes the handshake and permits streaming to begin.

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `type` | tstr | required | Literal value `"ACK"` |
| `granted_streams` | array of tstr | required | Subset of `crdt_streams` from CAPABILITY_NEG that the relay grants |
| `granted_buckets` | array of tstr | required | Subset of `bucket_subscriptions` from CAPABILITY_NEG that the relay grants |
| `denied_reason` | tstr | optional | Human-readable explanation; present only when one or more requested streams or buckets are denied |

`granted_streams` and `granted_buckets` MAY be empty arrays. An empty grant is not an error; it means the attestation bundle does not authorise any of the requested resources. The node SHOULD surface this condition to the operator rather than silently continuing.

When `denied_reason` is present, the node MUST log it. The node MAY retry with a reduced request set without re-establishing the transport connection.

---

## A.4 Streaming Messages

### A.4.1 DELTA_STREAM

Carries a single CRDT operation from one node to all subscribed peers on the same stream. The relay fans out each DELTA_STREAM it receives to every node subscribed to that `stream_id`.

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `type` | tstr | required | Literal value `"DELTA_STREAM"` |
| `stream_id` | tstr | required | CRDT stream identifier; MUST match a value in `granted_streams` |
| `op_type` | tstr | required | One of `"insert"`, `"delete"`, `"update"` |
| `vector_clock` | map of tstr→uint | required | Logical clock at the time of operation; keys are node IDs (hex-encoded bstr), values are sequence numbers (uint) |
| `payload` | bstr | required | Opaque CRDT operation bytes; encoding is engine-specific (YDotNet or Loro binary format) |
| `epoch_id` | tstr | optional | Present only for CP-class records; identifies the epoch in which this operation was authorised |

`op_type` is advisory metadata for the receiving application layer. The CRDT engine applies `payload` without inspecting `op_type`; the field exists to allow the application to route operations to the correct merge handler before deserialization.

`epoch_id` is required for any operation on a CP-class record type. The receiver MUST verify that its local epoch matches `epoch_id` before applying `payload`. A mismatch produces ERR_EPOCH_MISMATCH (§A.5).

The relay does not reorder or buffer DELTA_STREAM messages. Operations arrive in network order. The CRDT engine is responsible for convergent merge regardless of delivery order.

### A.4.2 GOSSIP_PING

Sent by each node to all connected peers every 30 seconds. The relay does not generate GOSSIP_PING; it relays the message as-is to all nodes on the session. GOSSIP_PING maintains membership state for partition detection and stale peer recovery.

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `type` | tstr | required | Literal value `"GOSSIP_PING"` |
| `sender_id` | bstr | required | Ed25519 public key of the sending node, exactly 32 bytes |
| `membership_excerpt` | array of maps | required | Partial membership view; each entry is a map with three keys (see below) |
| `sender_vector_clock` | map of tstr→uint | required | Sender's full vector clock summary at the time of ping |

Each entry in `membership_excerpt` is a CBOR map with the following fields:

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `node_id` | bstr | required | Ed25519 public key of the described peer |
| `last_seen` | uint | required | Unix timestamp (seconds) of the last message received from this peer |
| `vector_clock_summary` | map of tstr→uint | required | Most recent vector clock the sender has recorded for this peer |

A receiver that observes a `last_seen` value older than 90 seconds for any peer SHOULD treat that peer as suspected-partitioned and escalate to the application layer. Three consecutive missed pings (90 seconds) constitutes a partition event.

---

## A.5 Error Codes

Error messages are valid at any point in the connection lifecycle, including during the handshake. On receipt of an error message, the receiver MUST apply the retry semantics defined below before reconnecting.

All error messages share the following structure:

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `type` | tstr | required | Error code string (see table below) |
| `reason` | tstr | required | Human-readable description of the specific error condition |

| Error Code | `type` Value | Retry Semantics |
|---|---|---|
| Rate limit | `"ERR_RATE_LIMIT_EXCEEDED"` | Retry after exponential backoff: initial interval 1 s, maximum 60 s, with uniform jitter in [0, interval/2] |
| Version mismatch | `"ERR_VERSION_INCOMPATIBLE"` | No retry. Upgrade the daemon or relay to a compatible version before reconnecting |
| Missing attestation | `"ERR_ATTESTATION_REQUIRED"` | Re-authenticate with the IdP to obtain a fresh attestation bundle, then retry the handshake |
| Epoch mismatch | `"ERR_EPOCH_MISMATCH"` | Fetch the current epoch snapshot from any available peer, apply it locally, then retry the operation |
| Revoked key | `"ERR_KEY_REVOKED"` | Re-authenticate with the IdP. Obtain a new key bundle from the organisation administrator before reconnecting. The existing `node_id` key is permanently invalidated |
| Bucket unauthorised | `"ERR_BUCKET_NOT_AUTHORIZED"` | No retry. The node's role attestation does not grant access to the requested bucket. Obtain a new attestation with the correct role claims |
| Relay throttle | `"ERR_THROTTLE"` | Relay-enforced rate limit distinct from per-node rate limiting. Apply the same backoff policy as ERR_RATE_LIMIT_EXCEEDED |

Implementations MUST NOT retry on ERR_VERSION_INCOMPATIBLE or ERR_BUCKET_NOT_AUTHORIZED without operator intervention. Automatic retry on these codes produces a tight reconnect loop that degrades relay capacity.

---

## A.6 QR Onboarding Payload Format

The QR onboarding payload transfers both the attestation bundle and an initial state snapshot from an existing node to a new node. The payload is suitable for QR code encoding, NFC transfer, or secure paste. It is a flat byte sequence with the following layout:

```
+-------------------------+--------------------------------------+
| bundle_length: uint32   | attestation_bundle: CBOR (N bytes)   |
| (little-endian)         |                                      |
+-------------------------+--------------------------------------+
| snapshot_length: uint32  | snapshot: raw bytes (M bytes)       |
| (little-endian)          |                                     |
+-------------------------+--------------------------------------+
```

`attestation_bundle` is a CBOR map with the following fields:

| Field | CBOR Type | Required | Description |
|---|---|---|---|
| `issuer_public_key` | bstr | required | Ed25519 public key of the attestation issuer, exactly 32 bytes |
| `subject_public_key` | bstr | required | Ed25519 public key of the new node being attested, exactly 32 bytes |
| `role_claims` | array of tstr | required | Role names granted to the subject (e.g. `"editor"`, `"viewer"`) |
| `signature` | bstr | required | Ed25519 signature over the concatenation `issuer_public_key ‖ subject_public_key ‖ role_claims_cbor`, signed by the issuer's private key |
| `issued_at` | uint | required | Unix timestamp (seconds) at which the bundle was signed |

**Founder bundles:** `issuer_public_key` equals `subject_public_key`. The signature is self-signed by the founder's own private key. Founder bundles carry an implicit grant of all role claims and are accepted only during initial node creation.

**Joiner bundles:** `issuer_public_key` is the founder's key or any key already holding the `admin` role claim. The issuer signs with their private key. The relay verifies the signature against `issuer_public_key` before accepting the bundle during CAPABILITY_NEG.

Attestation bundles have no built-in expiry field. Revocation is enforced at the relay via a revocation list keyed on `issuer_public_key ‖ subject_public_key`. A revoked bundle produces ERR_KEY_REVOKED regardless of `issued_at`.

`snapshot` is an opaque byte sequence produced by the CRDT engine's snapshot serialisation. The format is engine-specific. The receiving node passes `snapshot` directly to the engine's hydration API. On hydration failure the node MUST discard the snapshot and request a full state transfer via DELTA_STREAM replay from a peer.

---

## A.7 Backward Compatibility Policy

The following guarantees apply across minor version increments (same major `protocol_version`):

1. The `type` field in each defined message type is stable. It will not be renamed or have its value changed in a minor version.
2. Fields documented as required in an existing message type will not be removed in a minor version. A receiver MAY reject a message that omits a required field.
3. Optional fields may be added to any existing message type in any minor version. Receivers MUST ignore unknown fields; this rule is mandatory, not advisory.
4. A message carrying `protocol_version` greater than the receiver's maximum supported version produces ERR_VERSION_INCOMPATIBLE. The receiver closes the connection immediately after sending the error.
5. The `supported_versions` array in HELLO enables a two-version overlap during rolling upgrades. If the receiver supports any version listed in `supported_versions`, it MUST negotiate down to the highest mutually supported version rather than returning ERR_VERSION_INCOMPATIBLE.

Breaking changes — removing required fields, renaming message types, or changing field semantics — require a major `protocol_version` increment. Implementations SHOULD NOT assume that two nodes with the same major version have identical optional field support; they MUST apply the unknown-field-ignore rule unconditionally.
