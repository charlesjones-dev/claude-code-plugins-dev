# Contributing

Bug reports and fixes are welcome. Pull requests are for fixes only; new plugins, skills and features start as an issue.

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).

## Reporting a Bug

[Open an issue](https://github.com/charlesjones-dev/claude-code-plugins-dev/issues) with:

- The plugin and its version
- The slash command you ran and what you expected
- What happened instead, including any error text

Security problems go through [SECURITY.md](SECURITY.md), not a public issue.

## Sending a Fix

1. Fork the repository and create a branch.

2. Make the fix. Each plugin is self-contained:

   ```
   plugins/{plugin-name}/
     .claude-plugin/plugin.json     # name, version, description, author, keywords
     skills/{skill-name}/SKILL.md   # one folder per slash command
     agents/{agent-name}.md         # optional subagents; use `model: inherit`
     README.md
     LICENSE
   ```

   The root `.claude-plugin/marketplace.json` lists every plugin. Its entry and the plugin's own `plugin.json` must keep the same name, version, description, author and keywords.

3. Test it. Validate the manifests, then load your clone as a local marketplace and run the skill you changed:

   ```
   claude plugin validate plugins/{plugin-name}
   claude plugin validate .
   ```

   ```
   /plugin marketplace add /path/to/your/clone
   /plugin install {plugin-name}@claude-code-plugins-dev
   ```

4. Leave version numbers and `CHANGELOG.md` alone. They're updated at release.

5. Commit with a conventional prefix such as `fix:` or `docs:`, and leave Claude Code attribution out of the message.

6. Open a pull request that says what was broken, how you fixed it and how you tested it. Link the issue if there is one.

If you edit a README, keep it plain: no emoji in headings, no "AI-powered", and no figures you haven't measured. See the [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code/plugins) for the plugin format.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
