# PDF visual QA

A PDF that generated without error is not a PDF that is right. Look at it.

## Render and inspect

Render every page to PNG with Poppler and open each image:

```
pdftoppm -r 80 -png output.pdf pages/page
```

`-r 80` is enough to read layout; raise it to 150 to check small text. Keep the PNGs next
to the working files, not in the delivery folder.

## Checklist, page by page

- Text is not cut at the page edge or inside a table cell.
- Images and charts are legible at the printed size; axis labels and legends are readable.
- Nothing overlaps: text over images, tables over footers, captions over figures.
- Links and references are present and, for web links, point to a web address.
- Footer and page numbers appear on every page and are in order.
- The source and extraction date are visible where numbers appear.
- No page is nearly empty because of a forced break; tighten spacing instead.
- Totals in the text match the tables.

## When the PDF library fails

Some PDF engines need system libraries that are missing on a machine. Do not switch to a
different design. Use the fallback: generate an HTML file from the same template and
print it to PDF from a browser (headless or manual "Save as PDF" with backgrounds
enabled). Then run the same render-and-inspect pass; browser output often paginates
differently from the library, so the check is not optional.

## Before sending

Show the rendered pages to the human. Send only after a yes. If the data changes, rebuild
from the script and inspect again.
