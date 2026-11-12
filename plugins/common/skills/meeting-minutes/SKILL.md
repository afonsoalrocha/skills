---
name: meeting-minutes
description: Use when asked for minutes, a meeting summary or a weekly review deck from a meeting transcript (.vtt or PDF): parse it with the script, show the text summary first, then build the PDF minutes from a template with standard file names.
---

# Meeting minutes

## Objective

Turn a transcript into minutes people can act on, without adding anything nobody said.

## Invariants

- **Never invent.** Include only what was said in the meeting.
- **Ask for the owner** of an action when the transcript does not make it clear.
- **No deadline said = `TBD`** (or the reader's language equivalent). Never guess a date.
- **Show the text summary to the user before generating any file.** The file comes after
  a review of the text.
- If the minutes go to the whole group, leave out the participant list.
- The PDF is built from the team's template through the `stakeholder-deliverables` skill
  (template, render, review). Never a from-scratch layout.
- If the parser finds no speech, stop with the error. Do not conclude the meeting had none
  before checking the transcript format.
- Confirm to the user where the file was saved.

## File names

```
YYYY-MM-DD_meeting_name_in_snake_case_minutes.pdf
YYYY-MM-DD_meeting_name_in_snake_case_presentation.pptx
```

Name in lowercase snake_case, no accents, based on the real event title. Minutes and the
weekly presentation sit side by side, told apart by the suffix.

## Flow

1. Get the transcript. A ready PDF only needs renaming and moving (same name rule).
2. Parse a `.vtt` with `scripts/vtt_to_utterances.py` (`references/vtt-parsing.md`).
3. Split topics, extract explicit actions, dates and deadlines.
4. Show the summary as text, fix it with the user, ask about unclear owners.
5. Build the PDF following `references/minutes-structure.md`, then review it
   (`stakeholder-deliverables`).
6. For a weekly deck, follow `references/weekly-review.md`.

## Routes

Read only the reference for the task.

| If the task is... | Read |
|-------------------|------|
| Parsing a `.vtt` transcript into speaker lines | `references/vtt-parsing.md` |
| Layout of the minutes: header, topics, action table, milestones | `references/minutes-structure.md` |
| Weekly review deck from the last minutes and the work board | `references/weekly-review.md` |
| Running the parser | `scripts/vtt_to_utterances.py` (`--help`, `--self-test`) |
| Building and checking the PDF or deck | the `stakeholder-deliverables` skill |
