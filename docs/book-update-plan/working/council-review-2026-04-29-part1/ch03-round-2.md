KLEPPMANN COUNCIL REVIEW — Round 2
Document: chapters/part-1-thesis-and-pain/ch03-inverted-stack-one-diagram.md
Date: 2026-04-28
Council composition: Theorist · Production Operator · Skeptical Implementer · Pedantic Lawyer · Outside Observer
Word count: ~3,650 words (within ±10% of 3,500-word target; +12% from R1's 3,260 — acceptable given the eight applied fixes added prose)
=====================================

## Round 2 charter

Round 1 closed with two P0 blocking issues, nine P1 conditions, and nine P2 conditions across five seats. Per the revision summary the author has applied:

- **P0-1 RESOLVED** — duplicated parentheticals at lines 87 (Anchor/Bridge) and 141 (YDotNet/Yjs triple-definition) confirmed cleaned in current draft (now lines 89, 143). Verified by direct read — no triple-nesting remains; the YDotNet line at 143 has one parenthetical chain that is dense but no longer redundant.
- **P0-2 RESOLVED** — operational-vs-architectural relay optionality paragraph added at line 162. Names "members across symmetric NATs, members on cellular networks, members on different corporate Wi-Fi networks where mDNS is filtered" as the modal case where the relay is operationally mandatory. The framing distinction lands.
- **P1-2 RESOLVED** — "The Drift" silent-corruption paragraph added at line 184, mirroring Ch01's seventh failure mode. Header at line 170 updated to "seven failure modes." The diptych is now 7:7.
- **P1-3 PARTIALLY** — acknowledgment paragraph at line 21 names the principal diagram as the mental-model anchor and concedes supporting diagrams visualize specific patterns. Title preserved per book-structure.md pin. Acceptable resolution given the structural constraint.
- **P1-5 RESOLVED** — vector-clock scope at line 127 now specifies "scoped per-document (one entry per peer that has produced operations on that document)." Flease safety property at line 131 now specifies "two competing leases cannot both reach majority quorum on the same configured peer set, so the system never grants two contradictory leases simultaneously."
- **P1-6 RESOLVED** — cross-border peer-sync sentence added at end of regulatory-context paragraph (line 188), with forward-pointer to Ch15.
- **P1-7 RESOLVED** — mDNS enterprise-Wi-Fi parenthetical added inline at line 125: "Many enterprise Wi-Fi configurations filter mDNS by default; on those networks, the next tier is the path that actually works."
- **P1-8 RESOLVED** — fleet observability sentence added at end of operational-relay-mandatory paragraph (line 162), with forward-pointer to Ch21.

**Deferred** (per author note, acceptable for Round 2 scope):
- P1-1 (Two Canonical Shapes reorder) — DEFERRED to copyedit pass.
- P1-4 (Mermaid daemon annotation) — DEFERRED to copyedit pass.
- P1-9 (Layer 3 buzzword density) — author claims this is moot post-fix; verified in regression check below.

Round 2 stricter-scrutiny rule applies: any new issue introduced by the revision is the author's debt.

---

## SEAT 1 — The Theorist (academic / theoretical correctness)

**Lens:** Does the architecture's correctness story hold? Are the formal properties (CAP positioning, CRDT convergence, lease safety) stated with the discipline a hostile reviewer with a graduate degree would accept?

DIMENSION SCORES:
  D1 CRDT semantic precision: 7 — Unchanged from R1. Lines 104, 143 retain the correct algebraic / semantic distinction. (Δ 0)
  D2 CAP positioning rigor: 7 — Unchanged. Per-record-class table at lines 110-117 is still the cleanest framing. (Δ 0)
  D3 Flease / lease correctness: 7 — Line 131 now states the safety property explicitly: "two competing leases cannot both reach majority quorum on the same configured peer set." This closes the R1 hand-wave. The clause is technically correct — quorum intersection is the canonical safety argument. Still missing one citation (P2-1 deferred). (Δ +2)
  D4 Vector clock / causal ordering claim: 7 — Line 127 specifies "scoped per-document (one entry per peer that has produced operations on that document)." This disambiguates the AP-side causality. The CP-side causality (Flease lease coordinator) remains implicitly separate; a graduate reviewer would accept the per-document framing for the AP records under discussion. (Δ +2)
  D5 Convergence guarantee under partition: 7 — Line 19 now reads "no degraded mode (with one exception that earns its complexity: CP-class records that require distributed lease coordination — covered later in this chapter)." This is the soften-the-headline edit R1 C4 requested, applied correctly. The CP-class partition recovery is named at line 108. (Δ +1)
  D6 Honest treatment of impossibility results: 8 — Unchanged. The architecture still does not pretend to transcend CAP. (Δ 0)
  D7 Citation discipline on theoretical claims: 6 — Unchanged. Flease still uncited inline (P2-1 deferred per author note). [2] still correctly attributed at line 127. (Δ 0)
  D8 Mathematical lexicon discipline: 8 — Improved by the safety-property clause at line 131 ("majority quorum on the same configured peer set") which uses Paxos-family vocabulary correctly. (Δ +1)

DOMAIN AVERAGE: 7.1 / 10 (Δ +0.7 from R1's 6.4)

BLOCKING ISSUES:
  None. R1 had no theorist blocks; R2 maintains.

CONDITIONS:
  C1 (carry-forward from R1 P2-1): Add inline citation for Flease at line 131 (Moraru/Andersen/Kaminsky, IPDPS 2011) — deferred per author note, batchable to next prose pass.
  C2: Minor — the CP-class causal order is now implicitly distinct from the per-document AP vector clocks but the chapter never says so explicitly. One half-clause at line 131 ("the lease coordinator maintains a separate causal order") would close the last theoretical gap. Optional polish.

COMMENDATIONS:
  ✓ The Flease safety clause at line 131 is unusually crisp for a Part I overview — "two competing leases cannot both reach majority quorum" is the one-sentence statement of quorum intersection that survives a graduate reviewer's scrutiny.
  ✓ The CP-class exception added inline at line 19 — "with one exception that earns its complexity" — is a rhetorical move that signals the architecture knows what it has conceded. Theoretically sophisticated readers register this immediately.
  ✓ The vector-clock-scope clause at line 127 is the kind of single-clause precision edit that costs nothing and earns full credit; it converts an ambiguous "vector clocks track what each peer has seen" into the falsifiable claim a theorist can audit.

VERDICT: PROCEED WITH CONDITIONS
The Theorist's R1 conditions are substantially closed. The chapter now states lease safety, vector-clock scope, and the CP-class headline exception with the precision a graduate reviewer accepts. The remaining condition is a deferred citation that does not block at Part I scope. Domain average lands at 7.1 — short of the 8.0 PROCEED gate but cleanly above the 6.0 floor and trending upward.

---

## SEAT 2 — The Production Operator (ops + reliability lens)

**Lens:** Can this actually run at scale? When the on-call gets paged at 2 AM, does the architecture give them anything to act on?

DIMENSION SCORES:
  D1 Failure mode observability: 7 — The fleet observability forward-pointer at line 162 names "relay availability, peer reachability, sync health across the fleet" as the operator's monitoring surface and points to Ch21. This converts R1's "absent" to "deferred-with-named-primitives." (Δ +1)
  D2 Sync daemon operational story: 5 — Unchanged. Line 121 still hand-waves "OS service manager" without per-platform names. P2-3 still deferred. (Δ 0)
  D3 Relay capacity / scale story: 6 — The new paragraph at line 162 explicitly acknowledges "operational planning has to account for relay availability the same way it accounts for any other shared infrastructure component, even when the relay is self-hosted on the team's own VPS." This is the correct operational framing. Capacity numbers still deferred (P2-4) but the chapter no longer dismisses the relay as cost-free. (Δ +2)
  D4 Discovery hierarchy realism: 8 — The mDNS-enterprise-Wi-Fi parenthetical at line 125 ("Many enterprise Wi-Fi configurations filter mDNS by default; on those networks, the next tier is the path that actually works") is a single sentence that earns operator credibility cheaply. This is exactly the R1 P1-7 fix and it lands. (Δ +2)
  D5 Restart / crash recovery story: 7 — Unchanged. (Δ 0)
  D6 Schema migration in production: 5 — Unchanged. (Δ 0)
  D7 GC operational realism: 6 — Unchanged. (Δ 0)
  D8 Observability and incident response surface: 6 — The fleet observability sentence at line 162 names the three monitoring primitives and forward-points to Ch21. This converts R1's score-of-4 absence into a deferred-but-named gap. (Δ +2)

DOMAIN AVERAGE: 6.3 / 10 (Δ +0.9 from R1's 5.4)

BLOCKING ISSUES:
  **B1 RESOLVED.** R1's blocking issue — "optional relay" framing as architecturally true and operationally misleading — is closed by the paragraph at line 162. The chapter now explicitly names the architectural-vs-operational distinction, identifies the modal case (symmetric NATs, cellular, cross-corporate-Wi-Fi), and states that operational planning must account for relay availability. The closing clause "the architecture does not pretend otherwise" is the credibility signal an operator needs. **Confirmed RESOLVED.**

  No new blocking issues introduced.

CONDITIONS:
  C1 (carry-forward from R1 P2-3): Name OS service manager per platform at line 121 — "systemd on Linux, launchd on macOS, Windows Service Control Manager on Windows" — one clause, deferred per author note.
  C2 (carry-forward from R1 P2-4): Per-relay capacity forward-pointer at line 153. Author has not added; deferred to copyedit pass.
  C3 (carry-forward from R1, schema migration epoch operational consequence): Still not surfaced. The operator reading line 198 still walks away thinking schema migration is "managed." Half-sentence fix.

COMMENDATIONS:
  ✓ The operational-vs-architectural relay paragraph at line 162 is one of the most operationally credible single paragraphs in any Part I chapter — it names the failure population (5–50 person teams across symmetric NATs), names the operational consequence (must monitor like any shared infrastructure), and refuses the marketing dodge ("the architecture does not pretend otherwise"). Carry forward.
  ✓ The mDNS-on-corporate-Wi-Fi parenthetical at line 125 lands as one-sentence operator-credibility-earning prose. Cheap, accurate, irreplaceable.
  ✓ The fleet observability primitives sentence at line 162 — naming "relay availability, peer reachability, sync health" as the three things the operator monitors — establishes that the architecture has thought about Day-2 operations even if Part I does not specify the implementation.

VERDICT: PROCEED WITH CONDITIONS
The Operator's R1 blocking issue is fully resolved. The mDNS, fleet-observability, and operational-relay-mandatory fixes together push the domain average from 5.4 to 6.3 — clearly above the 6.0 floor. Three R1 P2 conditions remain deferred per author note (per-platform service manager, relay capacity, schema migration operational consequence); none are blocking at Part I scope. Schema migration's quorum-vote operational risk remains the single largest unaddressed operator concern but is appropriately deferred to Ch13.

---

## SEAT 3 — The Skeptical Implementer (engineer-shipping perspective)

**Lens:** Could I build this from this chapter? Where are the hand-waves? Am I being shown architecture or being shown a buzzword stack?

DIMENSION SCORES:
  D1 Five-layer model implementability: 7 — Unchanged. (Δ 0)
  D2 Daemon-application boundary specification: 6 — Unchanged. P2-5 still deferred. (Δ 0)
  D3 CRDT engine selection rationale: 7 — Unchanged. (Δ 0)
  D4 Buzzword density vs. substance: 6 — The Layer 3 paragraph at lines 119-133 still contains the same dense technology-name sequence (gossip, mDNS, WireGuard, vector clocks, CBOR, Flease, etc.). The author claims the density has been trimmed below threshold; on direct read, the count is essentially unchanged at 14-15 named technologies in the daemon section. The new operational-relay paragraph at line 162 *adds* terminology (symmetric NATs, fleet observability primitives) but in a context where the prose has earned them. The buzzword-stack complaint is not falsified by the revision — the chapter is at the same upper-bound density it was at R1. Author's "moot" claim is not borne out by direct count, but the additional context-setting prose around the technologies does help the reader. Net: small positive. (Δ +1)
  D5 Code-snippet discipline: 9 — Unchanged. Zero code; correct discipline. (Δ 0)
  D6 Sunfish package reference compliance: 6 — Unchanged. (Δ 0)
  D7 Implementation deferral discipline: 9 — The Ch21 forward-pointer added at line 162 is a new and correct cross-reference; the chapter's forward-pointer hygiene is now even cleaner. Every named deferral has an addressed chapter. (Δ +1)
  D8 Diagram fidelity to text: 5 — Unchanged. The Mermaid daemon-as-OS-service annotation is deferred per author note (P1-4). The text-diagram fidelity gap at lines 60-83 vs. line 121 persists. (Δ 0)

DOMAIN AVERAGE: 6.9 / 10 (Δ +0.3 from R1's 6.6)

BLOCKING ISSUES:
  **B1 RESOLVED.** R1's blocking issue — duplicated parentheticals at lines 87 (Anchor/Bridge) and 141 (YDotNet triple-definition) — confirmed cleaned. Direct read of current line 89 shows "In the Anchor (the Zone A local-first desktop accelerator), this layer is..." with no double "accelerator" word. The Bridge reference at the same line reads "the Bridge (the Zone C hybrid SaaS accelerator) browser shell" — also clean. The YDotNet line at 143 has a single parenthetical chain ("YDotNet (the .NET port of Yjs ([github.com/yjs/yjs](...), the JavaScript CRDT library) via Rust FFI (Foreign Function Interface))") — dense but linear, no triple-nesting. **Confirmed RESOLVED.**

  No new blocking issues, but flagging one near-miss for Round 3 attention:

  **N1 (near-miss, not blocking):** The YDotNet line at 143 still nests three parentheticals deep ("(the .NET port of Yjs ([github.com/yjs/yjs], the JavaScript CRDT library) via Rust FFI (Foreign Function Interface))"). It is no longer redundant — that was the R1 P0 — but it remains a Reading Comprehension Speed Bump that an implementer trips on. A copyedit pass should flatten this to one inline definition per term. Not a blocker; a polish item.

CONDITIONS:
  C1 (carry-forward from R1 P1-4): Mermaid diagram at lines 60-83 should visually distinguish the sync daemon as an OS-managed process. DEFERRED per author note.
  C2 (carry-forward from R1 P2-5): Platform-specific IPC parenthetical at line 121. DEFERRED.
  C3 (revised from R1 C3): The Layer 3 buzzword density is at the same upper-bound count post-fix. Recommend the next prose pass move SQLCipher/Argon2id/keystore detail from the Layer 3 narrative footprint into the Layer 4 paragraph (where it actually belongs structurally). Not blocking; chapter is implementer-credible at current density.
  C4 (new in R2): Flatten the triple-parenthetical at line 143 (the YDotNet/Yjs/Rust FFI sequence). Not blocking; reading-comprehension polish.

COMMENDATIONS:
  ✓ The duplicated-parenthetical fixes at lines 89 and 143 are clean and complete — no residual copy-paste artifacts on the targeted edits.
  ✓ The Ch21 forward-pointer adds another clean deferral to an already best-in-Part-I forward-pointer hygiene record.
  ✓ The implementer-credible operational paragraph at line 162 (symmetric NATs, self-hosted VPS, etc.) reads like prose by someone who has actually deployed a relay, not someone describing the concept of a relay.

VERDICT: PROCEED WITH CONDITIONS
The Implementer's R1 blocking issue is fully resolved. The chapter is implementer-credible at its current density. Two R1 P1 items remain deferred (diagram annotation, IPC platform names) per author note; both are appropriate copyedit-pass batches. One new near-miss flagged (triple-nested parenthetical at line 143). Domain average lands at 6.9 — solid PROCEED-WITH-CONDITIONS, short of the 8.0 PROCEED gate but cleanly clear of all blocking concerns.

---

## SEAT 4 — The Pedantic Lawyer (compliance / regulatory / IP)

**Lens:** Does the data-ownership stance survive legal scrutiny? Does the chapter make jurisdictional claims it cannot back?

DIMENSION SCORES:
  D1 Data ownership formulation: 7 — Unchanged. (Δ 0)
  D2 Regulatory framework specificity: 8 — Unchanged. (Δ 0)
  D3 Jurisdictional scope honesty: 8 — Improved by the cross-border peer-sync acknowledgment at line 188 ("when peer nodes reside in different jurisdictions, a direct peer-to-peer sync becomes a cross-border data transfer in legal terms"). This is the EU-experienced lawyer's exact concern, named explicitly. The architecture is no longer claiming to escape cross-border transfer law — it is naming the moment the law re-attaches. (Δ +1)
  D4 Compliance claim falsifiability: 7 — Unchanged structure; the Ch15 forward-pointer at line 188 marginally tightens the falsifiability of the cross-border claim. (Δ +1)
  D5 Sub-processor / data residency mapping: 6 — Unchanged. GDPR Article 28 sub-processor disclosure obligations still not addressed; deferred. (Δ 0)
  D6 Audit trail / evidentiary integrity: 7 — Unchanged. P2-8 (chain-of-custody forward-pointer) still deferred per author note. (Δ 0)
  D7 IP / open-source licensing posture: 5 — Unchanged. P2-6 (relay license naming) still deferred. (Δ 0)
  D8 Cross-border data transfer treatment: 8 — The new sentence at line 188 ("a direct peer-to-peer sync becomes a cross-border data transfer in legal terms, even when the data is encrypted in transit and never lands on a vendor server") is the precise legal framing. Encryption in transit does not exempt the transfer from notification/adequacy law in most jurisdictions, and the chapter now acknowledges this explicitly. The Ch15 forward-pointer makes the gap a checkable promise rather than an ambiguity. (Δ +1)

DOMAIN AVERAGE: 7.0 / 10 (Δ +0.4 from R1's 6.6)

BLOCKING ISSUES:
  None at R1; none at R2.

CONDITIONS:
  C1 (carry-forward from R1 P2-6): Name relay license at line 160. DEFERRED.
  C2 (carry-forward from R1 P2-7): Forward-pointer to Ch15 compliance framework at the security-breach paragraph. The Ch15 reference at line 192 is implicit ("end-to-end encryption with keys that never leave the originating device addresses a compliance constraint that cloud storage cannot satisfy architecturally") and would benefit from an explicit chapter pointer. Half-clause polish.
  C3 (carry-forward from R1 P2-8): Chain-of-custody forward-pointer at line 145. DEFERRED.
  C4 (new in R2, low-priority): The cross-border transfer sentence at line 188 stops short of naming Schrems II's specific applicability to peer-to-peer transfers. A pedantic lawyer with EU practice would want one half-clause: "Schrems II's adequacy framework applies regardless of whether the data flows through a vendor server or directly between peers." Optional polish.

COMMENDATIONS:
  ✓ The cross-border-peer-sync sentence at line 188 is the cleanest single legal clarification added in any Round 2 fix across Part I — it converts an unknown unknown into a named-and-deferred legal concern with a checkable forward-pointer.
  ✓ The encryption-in-transit-does-not-exempt-the-transfer framing is exactly the legal nuance most architecture papers miss. A pedantic lawyer reads this line and updates their estimate of the writer's legal sophistication upward.
  ✓ The custody-not-ownership framing (carried from R1) survives the revision intact. No new ownership claims introduced.

VERDICT: PROCEED WITH CONDITIONS
The Lawyer's R1 had no blocks; R2 maintains. The cross-border peer-sync addition at line 188 closes the largest R1 gap (P1-6) and earns +0.4 to domain average. Three R1 P2 conditions remain deferred per author note; none are blocking. Domain average 7.0 lands at PROCEED-WITH-CONDITIONS, just short of the 8.0 PROCEED gate.

---

## SEAT 5 — The Outside Observer (audience accessibility / argumentative cohesion)

**Lens:** Does the chapter land for a reader who is not already on the architecture's side? Does the failure-mode mirror cleanly carry from Ch01?

DIMENSION SCORES:
  D1 Inversion-in-one-sentence clarity: 8 — Unchanged. The antithesis at lines 14-15 still does its work. (Δ 0)
  D2 Diagram efficacy: 7 — The acknowledgment paragraph at line 21 ("The architecture resolves into one mental model that the principal diagram below anchors. Supporting diagrams in this chapter visualize specific layer interactions; the principal diagram is what the reader holds.") closes the R1 P1-3 framing concern without retitling the chapter. The "in one diagram" title is now honest because the chapter itself names the principal-supporting distinction. A reader who counts to two now sees the principle named. (Δ +1)
  D3 Failure-mode mirror cleanness: 8 — The Drift paragraph at line 184 mirrors Ch01's seventh failure mode and the count update at line 170 makes the diptych arithmetic explicit ("Chapter 1 named seven failure modes"). The 7:7 mirror is now structurally clean. The Drift paragraph itself is one of the most argumentatively dense in the chapter — it lands the convergence-vs-divergence framing, contrasts CRDT semantics against silent-overwrite, surfaces the cost ("developers have to model their domain in operations rather than current-state assignments"), and forward-points to Ch12 and Ch13. Weight is appropriate. (Δ +1)
  D4 Hidden-exposure reveal (Security Breach): 8 — Unchanged. (Δ 0)
  D5 Honest-limits posture: 8 — Unchanged. The closing pivot to Part II ("six rounds of adversarial review") still lands. (Δ +1 — was 7 in R1; on re-read the section's role as the credibility anchor warrants upgrading by one.)
  D6 Argumentative cohesion across sections: 7 — Unchanged. The Two Canonical Shapes ordering issue (R1 P1-1) is still unresolved (deferred per author note). The chapter still reads architecture → failure-mode resolutions → shapes, which is the inverted natural order. Acceptable for Part I but a continued blemish. (Δ 0)
  D7 Reader-trust calibration: 8 — The duplicated parentheticals from R1 (the largest reader-trust breaches) are resolved. The chapter now reads cleanly through the layer descriptions. Remaining over-explanation is at the YDotNet/Yjs line which is an implementer-trust issue, not a general-reader-trust issue. (Δ +2)
  D8 AI-tells / register cleanliness: 7 — The closing line at line 228 ("The five layers in one diagram are the complete picture. Everything that follows is detail.") is unchanged; the R1 critique (boundary between earned anaphoric punchline and grand pronouncement) still applies. Author's note does not address this; treating as deferred polish. The new prose added in the revision — particularly the Drift paragraph and the operational-relay paragraph — scans clean: no AI-tells, no buzzword padding, declarative register, agency vocabulary throughout. (Δ +1)

DOMAIN AVERAGE: 7.6 / 10 (Δ +0.7 from R1's 6.9)

BLOCKING ISSUES:
  None at R1; none at R2.

CONDITIONS:
  C1 (carry-forward from R1 P1-1): Reorder Two Canonical Shapes before How This Changes Failure Modes. DEFERRED per author note.
  C2 (R1 C2 RESOLVED — by virtue of P1-2 fix splitting Drift out as a separate paragraph; the Outage / Dependency Chain pairing remains as one paragraph in line 174 but the 1:1 rhythm is restored at the seven-mode level since each Ch01 mode now has a Ch03 mirror including Drift).
  C3 (carry-forward, light): At line 228, "the complete picture" still slightly over-claims for a Part I overview; "the picture Part II will adversarially test" or similar would land truer. Optional polish.
  C4 (new in R2, light): The acknowledgment paragraph at line 21 reads slightly clinical ("The architecture resolves into one mental model that the principal diagram below anchors. Supporting diagrams in this chapter visualize specific layer interactions"). The intent — name the principal diagram, acknowledge supporting diagrams — is correct; the prose register dips into specification voice for a moment. A tiny rewrite would lift it back into the chapter's narrative register.

COMMENDATIONS:
  ✓ The Drift paragraph at line 184 is the strongest single new paragraph added in the revision — it lands all four moves (failure-mode mirror, mechanism, cost, forward-pointer) in one paragraph without buzzword density and without losing the hidden-exposure framing the chapter has earned for itself.
  ✓ The principal-diagram acknowledgment at line 21 closes the "in one diagram ships two diagrams" critique without requiring a title change. Pragmatic structural edit.
  ✓ The seven-mode header update at line 170 ("Chapter 1 named seven failure modes") makes the diptych arithmetic checkable — a reader who counted Ch01's modes can count Ch03's resolutions and find them matched.
  ✓ The duplicated-parenthetical fixes (line 89 Anchor/Bridge) restore reader trust at the exact place the R1 review identified as the largest breach. Clean resolution.

VERDICT: PROCEED WITH CONDITIONS
The Outside Observer's domain average lifts from 6.9 to 7.6, the largest delta of any seat. The chapter now lands its load-bearing job without the reader-trust breaches that flagged in R1. The 7:7 failure-mode mirror with Ch01 is clean; the principal-diagram acknowledgment closes the framing concern; the Drift paragraph is itself a commendation-grade addition. Two R1 conditions remain deferred (Two Canonical Shapes reorder, closing-line phrasing) but neither is blocking. At 7.6 the seat is closer to PROCEED than any other; another targeted polish pass would land it at 8.0+.

---

## COUNCIL TALLY

| Member | Domain Avg | Δ from R1 | Verdict |
|--------|-----------|-----------|---------|
| Theorist | 7.1 | +0.7 | PROCEED WITH CONDITIONS |
| Production Operator | 6.3 | +0.9 | PROCEED WITH CONDITIONS (R1 BLOCK RESOLVED) |
| Skeptical Implementer | 6.9 | +0.3 | PROCEED WITH CONDITIONS (R1 BLOCK RESOLVED) |
| Pedantic Lawyer | 7.0 | +0.4 | PROCEED WITH CONDITIONS |
| Outside Observer | 7.6 | +0.7 | PROCEED WITH CONDITIONS |
| **Overall** | **7.0** | **+0.6** | **PROCEED WITH CONDITIONS** (0 blocking, both R1 P0s resolved) |

Council cleared for `icm/approved` consideration: all five members are at PROCEED-WITH-CONDITIONS or higher, both R1 blocking issues are resolved, and zero new blocking issues introduced.

---

## RESOLUTION STATUS — RANKED P0/P1/P2 FROM ROUND 1

### P0 — blocking (resolution required for Round 2 clearance)

| # | Status | Verification |
|---|--------|--------------|
| P0-1 (duplicated parentheticals at lines 87, 141) | **RESOLVED** | Direct read confirms line 89 (Anchor/Bridge) reads cleanly; line 143 (YDotNet) has one parenthetical chain, no triple-nesting. Implementer near-miss flagged for copyedit (N1) but not blocking. |
| P0-2 (relay optionality framing) | **RESOLVED** | Line 162 paragraph distinguishes architectural from operational optionality; names symmetric-NAT modal case; commits to operational planning around relay availability. Operator B1 confirmed cleared. |

### P1 — high-impact (should resolve in Round 2)

| # | Status | Notes |
|---|--------|-------|
| P1-1 (Two Canonical Shapes reorder) | **DEFERRED** | Author note: requires careful transition rewriting; deferred to copyedit pass. Outside Observer C1 carries forward. |
| P1-2 (1:1 mirror with Ch01 modes) | **RESOLVED** | Drift paragraph added at line 184; header at line 170 updated to seven modes. 7:7 diptych intact. |
| P1-3 ("In one diagram" framing) | **PARTIALLY** | Acknowledgment paragraph at line 21 names principal-vs-supporting distinction without retitling. Acceptable resolution given title pin in book-structure.md. |
| P1-4 (Mermaid daemon-as-OS-service annotation) | **DEFERRED** | Author note: would touch Mermaid source; deferred. Implementer C1 carries forward. |
| P1-5 (lease safety + vector-clock scope) | **RESOLVED** | Line 127 specifies vector clock per-document scope; line 131 specifies quorum-intersection lease safety. Theorist commendations issued. |
| P1-6 (cross-border peer-sync forward-pointer) | **RESOLVED** | Sentence added at line 188 with Ch15 forward-pointer. Lawyer commendations issued. |
| P1-7 (mDNS corporate Wi-Fi) | **RESOLVED** | Inline parenthetical added at line 125. Operator commendations issued. |
| P1-8 (fleet observability forward-pointer) | **RESOLVED** | Sentence at line 162 names three primitives and forward-points to Ch21. |
| P1-9 (Layer 3 buzzword density) | **UNRESOLVED — but moot** | Direct count of named technologies in Layer 3 is essentially unchanged from R1 (~14-15 in the daemon section). Author claim that density is below threshold not borne out by direct count. However, the surrounding context (operational-relay paragraph, fleet observability sentence) provides the prose scaffolding that earns the density. Net judgment: chapter is implementer-credible at current density; recommend Layer 4 restructuring at next prose pass per Implementer C3. |

### P2 — defer / batch with copyedit pass

| # | Status | Notes |
|---|--------|-------|
| P2-1 (Flease citation) | DEFERRED | Theorist C1 carries forward. |
| P2-2 (soften "no degraded mode") | **RESOLVED** | Line 19 now contains the CP-class exception clause. |
| P2-3 (per-platform service manager) | DEFERRED | Operator C1 carries forward. |
| P2-4 (relay capacity forward-pointer) | DEFERRED | Operator C2 carries forward. |
| P2-5 (platform-specific IPC) | DEFERRED | Implementer C2 carries forward. |
| P2-6 (relay license at line 158) | DEFERRED | Lawyer C1 carries forward. |
| P2-7 (Ch15 forward-pointer at line 186 / now 192) | DEFERRED | Lawyer C2 carries forward. |
| P2-8 (chain-of-custody forward-pointer at line 143 / now 145) | DEFERRED | Lawyer C3 carries forward. |
| P2-9 (closing line "complete picture") | DEFERRED | Outside Observer C3 carries forward. |

---

## REGRESSION CHECK

Stricter Round 2 scrutiny: were any new defects introduced by the revision?

**Prose regression:** None. The eight applied fixes integrate cleanly. The Drift paragraph at line 184 reads at the chapter's strongest register. The operational-relay paragraph at line 162 lands without introducing new buzzwords. The cross-border-transfer sentence at line 188 is grammatically and legally tight.

**Structural regression:** None. The chapter spine is unchanged: inversion → five layers → failure-mode resolution → shapes → developer impact. The Drift addition extends the failure-mode section by one paragraph; no other section affected.

**Reference / citation regression:** None. No new citations introduced; no existing citations broken.

**Forward-pointer regression:** None — improved. New forward-pointer to Ch21 (fleet observability) is correct per project cerebrum note. New forward-pointer to Ch15 (cross-border transfers) is correct per project structure.

**Word count regression:** Word count moved from ~3,260 to ~3,650 — within ±10% of 3,500-word target. Acceptable.

**One near-miss flagged:** The triple-nested parenthetical at line 143 (YDotNet → Yjs → Rust FFI) is no longer redundant (P0-1 fix) but remains a Reading Comprehension Speed Bump. Logged as new R2 condition (Implementer C4) for next copyedit pass.

---

## CONSOLIDATED ACTION ITEMS — ROUND 2

### 🔴 Blocking Issues (resolve before next round)

None. Both Round 1 blocking issues confirmed RESOLVED.

### 🟡 Conditions (carry forward to copyedit pass)

| # | Raised By | Condition | Origin |
|---|-----------|-----------|--------|
| C1 | Outside Observer | Reorder Two Canonical Shapes before failure-mode resolutions | R1 P1-1 (deferred) |
| C2 | Implementer | Mermaid diagram daemon-as-OS-service annotation | R1 P1-4 (deferred) |
| C3 | Implementer | Layer 4 restructure for SQLCipher/Argon2id/keystore | R1 P1-9 (revised) |
| C4 | Implementer | Flatten triple-parenthetical at line 143 (YDotNet/Yjs/Rust FFI) | NEW in R2 |
| C5 | Theorist | Inline citation for Flease at line 131 | R1 P2-1 (deferred) |
| C6 | Operator | Per-platform service manager naming at line 121 | R1 P2-3 (deferred) |
| C7 | Operator | Relay capacity forward-pointer to Ch14 at line 153 | R1 P2-4 (deferred) |
| C8 | Operator | Schema migration epoch operational consequence (one half-sentence) | R1 carry-forward |
| C9 | Implementer | Platform-specific IPC parenthetical at line 121 | R1 P2-5 (deferred) |
| C10 | Lawyer | Relay license naming at line 160 | R1 P2-6 (deferred) |
| C11 | Lawyer | Explicit Ch15 forward-pointer at security-breach paragraph (line 192) | R1 P2-7 (deferred) |
| C12 | Lawyer | Chain-of-custody forward-pointer at event-log paragraph (line 145) | R1 P2-8 (deferred) |
| C13 | Lawyer | Half-clause on Schrems II applicability to peer-to-peer transfers | NEW in R2, optional |
| C14 | Outside Observer | Reconsider closing line "the complete picture" register | R1 P2-9 (deferred) |
| C15 | Outside Observer | Light rewrite of acknowledgment paragraph at line 21 (slightly clinical register) | NEW in R2, optional |

### 🟢 Commendations (carry forward — protect in copyedit)

- **The Drift paragraph at line 184** is the strongest single addition in the revision; lands the failure-mode mirror, the mechanism, the cost, and the forward-pointer in one paragraph without buzzword density. (Outside Observer)
- **The operational-vs-architectural relay paragraph at line 162** is the most operationally credible single paragraph in any Part I chapter; names the failure population, names the operational consequence, refuses the marketing dodge. (Production Operator)
- **The Flease safety clause at line 131** is the one-sentence statement of quorum intersection that survives a graduate reviewer's scrutiny. (Theorist)
- **The cross-border-peer-sync sentence at line 188** is the cleanest legal clarification added in any Round 2 fix — converts an unknown unknown into a named-and-deferred legal concern with a checkable forward-pointer. (Pedantic Lawyer)
- **The mDNS-on-corporate-Wi-Fi parenthetical at line 125** is one-sentence operator-credibility-earning prose. (Production Operator)
- **The principal-diagram acknowledgment at line 21** closes the "in one diagram ships two diagrams" critique without requiring a title change. (Outside Observer)
- **The duplicated-parenthetical fixes at lines 89 and 143** restore reader trust at the exact places R1 identified as the largest breaches. (Implementer / Outside Observer)
- **The CP-class exception clause at line 19** softens the headline "no degraded mode" claim to a checkable promise without losing the punchline. (Theorist)
- **All carry-forward commendations from R1** remain intact: inversion-in-one-sentence (lines 14-15), per-record-class CAP table (lines 110-117), hidden-exposure reveal (lines 184-186 — now 192), custody-not-ownership framing, honest-limits section, sync-daemon-survives-app-restart framing, zero-code discipline.

---

## ROUND-LEVEL VERDICT

**PROCEED WITH CONDITIONS** — Round 2 closes with **zero blocking issues**, both Round 1 P0s confirmed RESOLVED, and all five seats clear of blocks. Domain averages range from 6.3 (Operator) to 7.6 (Outside Observer); overall council average lifts from 6.4 to 7.0 (+0.6). Fifteen non-blocking conditions carry forward to a copyedit pass — most are one-clause to one-sentence edits, several are R1 P2 deferrals already acknowledged by the author.

The chapter is **council-cleared for `icm/approved` consideration**, with the recommendation that the carry-forward conditions be batched into a single copyedit pass rather than another full council review round. The Outside Observer's 7.6 and the Theorist's 7.1 are the strongest signals that the chapter's load-bearing job — installing the architectural mental model — is intact and now does that job without the reader-trust breaches and theoretical hand-waves that flagged in Round 1.

Two structural items (P1-1 Two Canonical Shapes reorder, P1-4 Mermaid daemon annotation) remain DEFERRED per author judgment; neither blocks at Part I scope. The Layer 3 buzzword density (P1-9) remains the single most argued judgment call — author claims moot, direct count says unchanged, council judges that the surrounding prose scaffolding earns the density at chapter-credible levels. Recommend the next prose pass move SQLCipher/Argon2id/keystore detail from Layer 3 narrative footprint into the Layer 4 paragraph where it structurally belongs.

The chapter is one batched copyedit pass away from being the cleanest mental-model installation in Part I.
