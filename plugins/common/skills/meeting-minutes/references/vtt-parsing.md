# Parsing a `.vtt` transcript

Parsing is deterministic, so it is a script, not inline code.

```
python scripts/vtt_to_utterances.py transcript.vtt utterances.txt
```

## What it does

- Extracts `<v Speaker>text</v>` cues.
- Merges consecutive cues from the same speaker into one utterance.
- Drops empty utterances.
- Writes one `[Speaker] text` line per utterance. The output is written to a temporary
  file and renamed, so a failure never leaves a half-written file.
- Exits 1 with `ERRO` if no utterance is found, and writes nothing.

## After a failure

An empty result usually means a different format (no `<v>` voice tags, or a plain-text
export), not a silent meeting. Open the first lines of the transcript and check the format
before reporting anything about the meeting. For a format without voice tags, ask the user
for a speaker-labelled export.

## Next

Save `utterances.txt` with the work for the meeting, in the project's own folder for
working files. Read it to separate topics, extract explicit actions and dates, and draft
the text summary (`references/minutes-structure.md`).
