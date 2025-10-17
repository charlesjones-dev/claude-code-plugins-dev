# Commit and Push

Commit all changes to git and push to origin.

## Instructions

When this command is executed:

1. Run `git status` to see all changes
2. Run `git diff` to see the actual changes
3. Run `git log -3 --format='%s'` to see recent commit message style
4. Analyze all changes and draft a concise commit message that:
   - Follows the repository's commit message style
   - Accurately describes what changed and why
   - Uses conventional commit prefixes if the repo uses them (fix:, feat:, docs:, etc.)
5. Add all changes with `git add .`
6. Commit with the drafted message
7. Push to origin with `git push`
8. Confirm success and show the commit hash

IMPORTANT: Do not include the following in commit messages:

- 🤖 Generated with [Claude Code](https://claude.com/claude-code)
- Co-Authored-By: Claude <noreply@anthropic.com>
