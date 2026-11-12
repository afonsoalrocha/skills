# Structure of the minutes

## 1. Header

- Title: "Meeting minutes - <context>".
- Subtitle: the team or organisation, if relevant.
- Meeting date.

## 2. Main topics discussed

- Numbered, one per subject.
- Each topic has short bullets: what was said or decided.
- Objective language. Nothing that was not said.

## 3. Actions (table)

| # | Action | Owner | Due |
|---|--------|-------|-----|

- Only actions that were explicitly stated.
- Owner unclear: ask the user, do not assign one.
- Due date not mentioned: write `TBD`.

## 4. Next milestones

- Dates mentioned in the meeting.
- Format: the **date in bold**, then the description.

## Process

1. Draft the four sections as plain text and show them to the user.
2. Apply corrections and answer the owner questions.
3. Only then generate the PDF from the team template, with the data above as input.
4. Render and review each page (`stakeholder-deliverables`, `references/pdf-qa.md`).
5. Save with the standard name from `SKILL.md` and tell the user where.

The participant list is omitted when the minutes go to the whole group.

## A PDF that already exists

If the user already has the PDF, copy it to the minutes folder, rename it to
`YYYY-MM-DD_meeting_name_minutes.pdf` and confirm. The same applies to a ready deck with
the `_presentation.pptx` suffix.
