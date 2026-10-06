# Security policy

## Reporting

Email [core@emergencybd.com](mailto:core@emergencybd.com) with the subject line `SECURITY: <short summary>`. Never use a public issue, pull request, or discussion. Encrypt if the report contains live personal data.

Include what an attacker can do, the steps to reproduce, the affected component or version, and the impact. A proof of concept helps. Say so if you are unsure whether something is a vulnerability.

## Response

We acknowledge within 3 days and finish an initial assessment within 7 days. Valid reports come with a fix plan and a date. Invalid ones come with the reason. We update you until the fix ships, credit you if you want to be credited, and publish nothing without your agreement on the wording.

## Sensitive data

A vulnerability here can expose the location or identity of someone at risk. Report it to us and nowhere else. Do not scan any deployment we operate. Do not reach data you did not need to show the issue. Do not use personal data you come across.

## Out of scope

- Scanner output with no demonstrated impact.
- Missing headers, rate limits, or CSRF tokens on endpoints with no sensitive action.
- Dependencies with no working exploit against this code.
- Denial of service through load or volume alone.
- Reports sent through a public channel.

## Scope

The source code in this repository and any service the project operates. Not third-party deployments, including forks and self-hosted instances maintained by others.