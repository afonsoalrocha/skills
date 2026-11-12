---
name: stakeholder-deliverables
description: "Use when producing a PDF or slide deck that a stakeholder will read: build from an approved template, from validated data, with the source cited, and review every rendered page or slide with a human preview before sending."
---

# Stakeholder deliverables

## Objective

Material that leaves the team looks consistent and carries numbers someone can trace.
This skill covers the process around a PDF or deck, not the look of a specific brand.

## Invariants

- **Template, never from scratch.** Start from the team's approved template. If none
  exists, ask the owner for one; do not invent a design for a stakeholder.
- **Validated data only.** Generate from results that passed their integrity checks. If a
  result is partial or blocked, say so on the material itself.
- **Cite the source.** Every table, chart and number names its source (system, table or
  report, and the extraction date) inside the document, not only in the chat.
- **Render and review every page or slide** before sending: cut text, overlap, unreadable
  images, broken links, footer and page numbers. Then a human previews it.
- The generator script is saved with the work, so the file can be rebuilt. Do not edit
  the output by hand and lose that.
- Links inside the material are web links (skill `share-web-links`), never drive paths.
- Do not send. Sending is a human decision after the preview.

## Flow

1. Confirm the data is validated and note its source and date.
2. Pick the template and the structure (`references/deck-structure.md` for decks).
3. Generate from a saved script.
4. Render to images and inspect each one (`references/pdf-qa.md`).
5. Fix, regenerate, re-inspect. Show the preview to the human.
6. Save the final file where the team keeps outputs and share its web link.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Checking a PDF: render to PNG, what to look for, fallback when the PDF library fails | `references/pdf-qa.md` |
| Building a slide deck: order, KPI slide, tables, charts, source notes, closing | `references/deck-structure.md` |
| Putting a link to the finished file in a ticket or message | the `share-web-links` skill |

Meeting minutes and weekly decks have their own flow: the `meeting-minutes` skill, which
uses this one for the PDF.
