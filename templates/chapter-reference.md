# Chapter N — Component Name

<!-- Target: ~X,000 words -->
<!-- Source: vNN §X, vNN §Y -->
<!-- Part: III — specification voice -->

---

*Opening: state what this component is and what problem it solves. One paragraph. No "in this chapter we will cover". Just say what it is.*

---

## Architecture Overview

*The structural picture. What are the layers, the components, the boundaries? If there's a diagram, describe it here.*

## [First Major Concept]

*Specification voice: "The [component] does X" not "you should configure X". Complete — a developer reading this section should be able to implement it. Cross-reference Part IV for the tutorial path.*

### [Sub-concept]

*[Specific mechanism, invariant, or constraint. Be precise.]*

## [Second Major Concept]

*[Continue specification. Each section should be independently implementable.]*

### [Sub-concept]

## [Third Major Concept]

### [Sub-concept]

---

## Failure Modes and Edge Cases

*What breaks? Under what conditions? How does the system recover? This is not optional — specification without failure modes is incomplete.*

| Scenario | Behavior | Recovery |
|---|---|---|
| [Scenario 1] | [What happens] | [How to recover] |
| [Scenario 2] | [What happens] | [How to recover] |

---

## Sunfish Package Reference

*Which packages implement this component. Reference by package name only — no class APIs.*

| Package | Responsibility |
|---|---|
| `Sunfish.Kernel.X` | [What it does] |
| `Sunfish.Foundation.Y` | [What it does] |

*See [Chapter 17/18/19] for the tutorial path to wiring these packages.*

---

## References

<!-- Add citations here as you write -->
