# Appendix E — Citation Style

<!-- icm/approved -->
<!-- Target: ~500 words -->

This book uses IEEE numeric citation style, standard in engineering, computer science, and related technical disciplines. All sources are cited using bracketed numbers in the text, with full details in a numbered reference list at the end of the book.

---

## In-Text Citations

Cite sources using square brackets: [1], [2], [3], in the order they first appear in the text.

Reuse the same number every time you refer to the same source — do not assign a new number on each use.

Place citations before punctuation, with a space before the first bracket:

> …as shown in [1].
>
> …as described in [2], [4].

When quoting or referring to a specific part of a source, include page numbers:

> …as discussed in [3, p. 55].

---

## Reference List

All cited works are listed in a "References" section, ordered numerically by citation number, not alphabetically.

Each entry begins with its bracketed number: [1], [2], etc.

Use author initials followed by last name (e.g., A. B. Smith).

Include enough information — title, publisher or journal, year — for readers to locate the source.

---

## Common Reference Formats

**Book**

> [n] A. A. Author, *Title of Book*, xth ed. City, ST/Country: Publisher, Year.

**Edited Book Chapter**

> [n] A. A. Author, "Title of chapter," in *Title of Book*, xth ed., Editor Initial(s). Last Name, Ed. City, Country: Publisher, Year, pp. xx–yy.

**Journal Article**

> [n] A. A. Author, "Title of article," *Abbrev. Journal Title*, vol. x, no. y, pp. xx–yy, Month Year.

**Conference Paper**

> [n] A. A. Author, "Title of paper," in *Proc. Conf. Name*, City, Country, Year, pp. xx–yy.

**Web / Online Source**

> [n] A. A. Author, "Title of page," *Site Name*, Year. [Online]. Available: URL. [Accessed: Month Day, Year].

**Technical Report**

> [n] A. A. Author, B. B. Author, and C. C. Author, "Title of report," Institution, City, Tech. Rep. XX-NNNN, Month Year.

**Pre-print (arXiv and similar)**

> [n] A. A. Author and B. B. Author, "Title of paper," *arXiv:NNNN.NNNNN*, Month Year.

**Standard or RFC**

> [n] A. A. Author, "Title of specification," Organization, Standard/RFC Number, Month Year.

For IETF RFCs specifically: `[n] A. A. Author, "Title," IETF RFC NNNN, Month Year.`

**Legal Decision**

> [n] Court Name, "Case name — short form," Case No. XXX/YY, Judgment, Month Day, Year.

Example: CJEU Schrems II is cited as `[n] Court of Justice of the European Union, "Case C-311/18 — Data Protection Commissioner v. Facebook Ireland Ltd and Maximillian Schrems," Judgment, Jul. 16, 2020.`

**Statute or Regulation**

> [n] Enacting Body, Jurisdiction, "Title of Act, Year (Act No. XX of YYYY)," Month Day, YYYY (effective Month Day, YYYY).

Example: `[n] Government of India, The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), Aug. 11, 2023.`

For EU regulations specifically: `[n] Regulation (EU) NNNN/YYYY of the European Parliament and of the Council of Day Month YYYY on [subject], Official Journal of the European Union, L NNN/N, Month YYYY.`

---

## Consistency Rules

- Use IEEE style throughout the book: same in-text format and reference patterns everywhere.
- Maintain consistent capitalization of titles and abbreviations, especially journal and conference names.
- When citing multiple sources at once, list each number separately in its own bracket: [1], [3], [5].
- Do not merge multiple citations into a single bracket (not [1,3,5] — use [1], [3], [5]).

---

## Examples from This Book

The following in-text citations illustrate the variety of source types cited across the manuscript. The full reference list is assembled at the final-manuscript stage; Appendix C contains the complete annotated bibliography organized by topic.

| Citation | Format | Source |
|---|---|---|
| [1] | Conference paper | M. Kleppmann, A. Wiggins, P. van Hardenberg, and M. McGranaghan, "Local-first software: You own your data, in spite of the cloud," in *Proc. ACM SIGPLAN Int. Symp. New Ideas, New Paradigms, and Reflections on Programming and Software (Onward! '19)*, Athens, Greece, Oct. 2019, pp. 154–178, doi: 10.1145/3359591.3359737. [Online]. Available: https://www.inkandswitch.com/essay/local-first/ |
| [2] | Book | M. Kleppmann, *Designing Data-Intensive Applications*, 1st ed. Sebastopol, CA: O'Reilly Media, 2017. |
| [3] | Technical report | M. Shapiro, N. Preguiça, C. Baquero, and M. Zawirski, "A comprehensive study of convergent and commutative replicated data types," INRIA, Tech. Rep. RR-7506, Jan. 2011. |
| [4] | arXiv pre-print | H. Howard, D. Malkhi, and A. Spiegelman, "Flexible Paxos: Quorum intersection revisited," *arXiv:1608.06696*, Aug. 2016. |
| [5] | IETF RFC | S. Josefsson and I. Liusvaara, "Edwards-Curve Digital Signature Algorithm (EdDSA)," IETF RFC 8032, Jan. 2017. |
| [6] | Online source | T. Perrin, "The Noise Protocol Framework," Revision 34, Jul. 2018. [Online]. Available: https://noiseprotocol.org/noise.html |
| [7] | Legal decision | Court of Justice of the European Union, "Case C-311/18 — Data Protection Commissioner v. Facebook Ireland Ltd and Maximillian Schrems," Judgment, Jul. 16, 2020. |
| [8] | EU Regulation | Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation), *Official Journal of the European Union*, L 119/1, May 2016. |
| [9] | National statute | Government of India, The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023), Aug. 11, 2023. |
| [10] | Engineering blog | T. Palmer, "Scaling the Linear sync engine to 100M+ records," *Linear Engineering Blog*, 2023. [Online]. Available: https://linear.app/blog/scaling-the-linear-sync-engine |

Numbering above is illustrative. The canonical numbered assembly runs from the first citation in the manuscript's reading order.

---

## Assembly Guidance

At final-manuscript assembly:

1. Walk the manuscript in reading order and renumber every citation from [1] to [N] in first-appearance order.
2. Compile the numbered Reference List in the back matter, entries matching the renumbered in-text citations.
3. Verify every in-text bracket resolves to a Reference List entry and every Reference List entry is cited at least once.
4. Check legal and regulatory citations against primary sources — a misspelled case name or wrong regulation number in a book making a compliance argument is a credibility defect that security and legal reviewers will catch immediately.
5. Check URLs are reachable at the time of press; annotate any URL with a retrieval date if the content is expected to shift.
