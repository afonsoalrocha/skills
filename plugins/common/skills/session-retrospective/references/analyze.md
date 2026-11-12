# Analyze

For each finding, separate the observed fact from the probable cause, then classify it.

| Type | Examples |
|------|----------|
| Agent mistake | wrong answer, ignored rule, forgotten step, scope exceeded |
| User correction | "that is not what I asked", "again", a repeated request, an interruption |
| Wasted tokens | re-reading, a huge output in context, a redundant search, an unneeded subagent, rework |
| Environment friction | a command that always fails, shell escaping, profile or permission trouble, a slow tool |
| Analytical conclusion | a number or conclusion that changed in the session, a divergence someone pointed out, a result recorded without checking the source |
| Stale or missing knowledge | documentation contradicted by code or data, an empty search followed by a long exploration, a rule rediscovered |
| Skill structure | a bloated skill, an invariant rule that sat in a reference and was ignored, a reference never opened, a new skill with no need, text duplicated across skills |
| Good practice | what worked and should be kept |

Check the ledger: did the same mechanism appear before? Did the environment already fix
it? An isolated transient failure does not become a rule.

## Analytical conclusions

For each piece of work changed that day, ask:

- Was the stated conclusion checked at the source?
- Did it change during the session, and does the written result match the final version?
- Was it already delivered to someone?

The summary only points at candidates. Confirm by reopening the script or query and the
source, never from the conversation. Not enough evidence: label it `investigate`, propose
no change. A wrong conclusion that was already delivered is top priority, even as a single
case.

## Stale knowledge

If a session read an article and then found something that contradicts it, or explored
code or data because the documentation did not answer, propose updating or creating the
article through the project's knowledge workflow.

## Skill structure

The summary lists skills triggered, skill files read, skill files edited and (when the
project has one) validator warnings. Ask, from evidence:

- **Skill triggered, rule broken.** Was the rule in the body or in a reference? If it was
  in a reference that was not read, either the route trigger in the table is weak (fix the
  row) or the rule is invariant and moves up into the body. If it was in the body and
  ignored, the wording or the instruction is the problem, not the structure.
- **A reference read whole for no need, or several references of one skill read together.**
  The route is too wide (split it) or two routes always travel together (merge them).
- **A skill loaded and barely used** (large body, the task used one line): shrink it or
  move content into references. Two skills that always fire together: merge them. A skill
  that almost never fires: turn it into an article.
- **A skill edited that day.** Did the change follow `CONVENTIONS.md` (right place, short
  body, a row in the routes table) and did the validator pass? A new skill with no reason
  why an existing one would not do is a finding.
- **Validator warnings that persist from one day to the next** are a direct proposal.
- **Preserve capability.** Every proposal to slim down shows a before/after diff proving
  no invariant rule is lost, and how to test that the skill still gives the same result.

## Generalization test

Before proposing a permanent change: the mechanism appears on 2 or more days, or one case
risks data integrity, security, a wrong write or a wrong delivery. Otherwise only record it.
