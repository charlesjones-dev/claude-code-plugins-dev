---
name: git-pr-codex-loop
version: 1.0.0
description: |
  Open a PR for the current branch, then loop on Codex Code Review until it
  comes back clean: resolve each finding, reply, and re-request review with a
  single @codex review once the whole pass is handled. Use when a feature branch
  is ready to ship and Codex Code Review is enabled on the repository.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
disable-model-invocation: true
---

# /git-pr-codex-loop - Codex Code Review loop

> **Positioning:** Claude Code's native `/code-review` command (with `--fix`,
> `--comment`, and the cloud "ultra" mode) now covers automated
> review-and-fix loops natively, with no external dependencies. This skill is
> specifically for repositories standardized on OpenAI's Codex Code Review
> bot, and remains the right tool for that cross-tool workflow.

You drive the current branch's pull request through Codex Code Review until the
review is clean. The human makes the final merge decision; you never merge.

## Prerequisites

- The GitHub CLI (`gh`) is installed and authenticated (`gh auth login`).
- Codex Code Review is enabled for the repository in Codex settings. With
  **Automatic reviews** on, Codex reviews every new PR; otherwise you trigger a
  review manually with `@codex review`. Reviews post as the Codex bot
  (`chatgpt-codex-connector`).
- Codex applies a `## Review guidelines` section from your repo's `AGENTS.md`
  when present, so project-specific review rules are honored automatically.

## Process

### Step 1: Open or find the PR

1. Get the current branch: `git branch --show-current`. If it is `main` or
   `master`, stop and tell the user to switch to a feature branch.
2. Look for an existing PR: `gh pr view --json number,url,state 2>/dev/null`.
   If none exists, push the branch (`git push -u origin HEAD`) and open one with
   `gh pr create --fill` (write a real title/description if the change warrants
   it). Match the PR attribution style used by the `git-commit-push-pr` skill.
3. Capture the PR number and URL for the rest of the run.

### Step 2: Monitor CI

Watch checks with `gh pr checks --watch`. If any check fails, fix the cause,
commit, push, and watch again. Do not continue while checks are red — Codex
reviewing a non-compiling PR is wasted.

### Step 3: Monitor for the Codex review

When a review is requested — automatically on PR open, or by your `@codex
review` reply — Codex first **acknowledges** with a 👀 (`eyes`) reaction on the
triggering post, then works. The 👀 means "received the request," not "done" —
do not act on it. Poll for the real outcome with `gh pr view --comments`, the
review-thread query below, and the reactions check below.

If neither a 👀 reaction nor a review appears after a reasonable wait,
**Automatic reviews** is probably off for this repository. Do not tag `@codex`
to force one — stop the run and tell the user to enable Codex Code Review
(Automatic reviews) for the repo in Codex settings
(https://chatgpt.com/codex/settings/code-review), then re-run
`/git-pr-codex-loop`.

A review pass ends one of two ways — watch for **both**:

**a) Findings posted.** Codex labels each finding by priority (P0 / P1 / P2) and
usually posts several comments a few seconds apart followed by a summary. Do NOT proceed on the first
comment — you would resolve a partial review and miss the rest. Wait for the
pass to *settle*:

- Prefer the explicit end-of-pass signal: Codex's summary comment for this
  commit (the overview that ends in a verdict like "Codex Review: ...").
- Otherwise debounce on the count: poll the comment/thread count, sleep ~30s,
  poll again, and only continue once two consecutive polls match (no new
  comments arrived in the quiet window).

Collect every comment and thread from this pass, then go to Step 4.

**b) No issues — 👍.** When Codex finds nothing it may post no review at all and
instead add a 👍 (`+1`) reaction to the PR description (the opening post). Treat
that as a clean pass: skip Step 4 and go straight to Step 7. Check it with (the
PR description is issue `PR_NUMBER`; a `+1` from the Codex bot means "no issues
found"):

```bash
gh api repos/OWNER/REPO/issues/PR_NUMBER/reactions \
  --jq '.[] | select(.content=="+1") | .user.login'
```

### Step 4: Resolve every finding (worst priority first: P0, then P1, then P2)

Resolve in priority order — P0 first, then P1, then P2. For each Codex
comment:
- If it is correct: fix it, commit, push, and reply on the thread explaining the
  fix (reference the commit SHA). Do NOT tag `@codex` in per-thread replies.
- If it is wrong or not worth the change: reply with the reason and resolve the
  thread without a code change.

Do not request a re-review here. Tagging `@codex` on each thread would dispatch
a separate review per comment — handle every thread in this pass first, then
trigger exactly one re-review in Step 5.

Read and resolve review threads via the GitHub GraphQL API (the REST comments
endpoint cannot mark a thread resolved):

```bash
# list review threads (ids + resolved state + first comment)
gh api graphql -f query='
  query($owner:String!,$repo:String!,$pr:Int!){
    repository(owner:$owner,name:$repo){
      pullRequest(number:$pr){
        reviewThreads(first:100){ nodes { id isResolved comments(first:1){ nodes { body path } } } }
      }
    }
  }' -F owner=OWNER -F repo=REPO -F pr=PR_NUMBER

# resolve one thread after the fix lands
gh api graphql -f query='
  mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}){ thread { isResolved } } }' -F id=THREAD_ID
```

### Step 5: Re-review

Once every comment from this pass is fixed/replied and pushed, post a **single**
new comment on the PR — `@codex review` — to request one fresh pass over the
latest commit. Exactly one `@codex` mention per loop iteration; never one per
thread. Codex acknowledges with 👀, then reviews. Monitor for it as in Step 3.

### Step 6: Loop

Repeat Steps 4 and 5 until a pass comes back clean — either Codex's summary
reports no remaining issues ("Codex Review: Didn't find any major issues") or
Codex adds a 👍 reaction to the PR description (Step 3) — and every thread is
resolved.

### Step 7: Hand back

Show the PR URL and a short summary of what changed across the loop. Do not
merge. The human makes the final merge decision.

## Important rules

- Never merge the PR. Surface the result and stop.
- A 👀 reaction means Codex *received* the request, not that it finished — wait
  for findings or a 👍 before acting. A 👍 on the PR description means clean.
- Never force push. Push fixes to the same branch; do not open extra PRs.
- Claude makes every fix locally; never delegate fixes to Codex. The only
  `@codex` mention the skill posts is `@codex review`, exactly once per pass
  (after all threads are handled) — never one per thread, never `@codex fix` or
  any other command.
- Reply with specifics (commit SHA + what changed) so each re-review has context.
- If Codex is wrong, push back with a reasoned reply instead of churning the
  diff with a needless "fix".
