# Contributing to Emergency Bangladesh

## Code of Conduct

Participants disagree with ideas, not people. Report harassment, personal attacks, insults, or private information sharing to [core@emergencybd.com](mailto:core@emergencybd.com). The Core Team handles reports confidentially.

Maintainers remove comments, commits, code, and issues that break this Code.

## Pull requests

Every change lands through a pull request. Never push directly to the main.

Open a pull request for every change, including typos. Keep each PR focused on a single purpose. Unrelated changes get split or rejected.

Reviewers may request changes, split PRs, or close them. This is routine, not a judgement of your work.

## Development workflow

1. Fork and branch from main. Never work on the default branch.

2. Name branches descriptively, e.g., feat/volunteer-management or feat/identity-verification.

3. Make the change.

4. Commit with a clear message: use conventional commits (feat:, fix:, docs:, etc.) and explain what changed and why.

5. Sign off every commit:

   ```bash
   git commit -s -m "feat: add forecast endpoint"
   ```

   The `-s` flag adds a `Signed-off-by` trailer. Every commit needs one. See [https\://developercertificate.org/](https://developercertificate.org/).

6. Push the branch and open the pull request.

## Testing

Correctness is the contributor's responsibility.

1. Add or update tests for every behaviour you add or change, including failure paths.
2. Run the full existing suite before requesting review and confirm it passes.
3. Run the project's lint, formatting, and type checks and resolve every warning. Do not suppress one to force a passing run.
4. If a test fails and you cannot fix it, say so in the pull request and explain why. Never report a run you did not perform.

## AI-assisted code

AI coding tools are allowed. You own every line you submit, including lines an AI wrote, and your name is on the pull request. Read every line before submitting and be able to explain it.

Verify generated logic against the specification, existing behaviour, and the test suite before submitting. You own the license and provenance of what you submit, so do not submit code you cannot trace to a source you have the right to use.

Noting which parts were AI-assisted in the pull request description is welcome. It does not reduce your responsibility.

## Bugs and security

Report bugs in the issue tracker with the version, environment, steps to reproduce, and expected behaviour. Do not file a bug as a pull request.

Do not open a public issue for a security vulnerability. Contact the Core Team first. See [SECURITY.md](SECURITY.md).

## License

Contributions are licensed under the terms in LICENSE. By opening a pull request you agree to license your contribution under those terms.

## Contact

| Name                | Title         | Role                   | Contact                                             |
|:------------------- |:------------- | ---------------------- |:--------------------------------------------------- |
| Core Team           | EBD Core Team | Project Governence     | [core@emergencybd.com](mailto:core@emergencybd.com) |
| Sneha Salam         | CEO, Docufy   | Project Coordination   | [sneha@docufybd.com](mailto:sneha@docufybd.com)     |
| Rakibul Hasan Ratul | CTO, Docufy   | Contributor Management | [ratul@docufybd.com](mailto:ratul@docufybd.com)     |

Docufy is the technology and documentation partner. The Core Team makes day-to-day decisions.
