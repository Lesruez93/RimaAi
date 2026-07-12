# Proposal

[`RimaAI_AI4I_Proposal_Development.md`](RimaAI_AI4I_Proposal_Development.md) —
the AI4I 2026 (Track 3: Development) proposal.

## Convert to PDF

Target formatting: **Avenir/Arial 11pt, 1.15 line spacing, 1-inch margins,
max 10 pages** excluding the cover and appendices.

Using Pandoc + a LaTeX engine:
```bash
pandoc RimaAI_AI4I_Proposal_Development.md \
  -o RimaAI_AI4I_Proposal_Development.pdf \
  -V geometry:margin=1in -V fontsize=11pt -V mainfont="Arial" \
  --pdf-engine=xelatex
```

Or paste into Google Docs / Word, set Arial 11pt and 1.15 spacing, and export
to PDF. Fill in team details on the cover page before submitting.
