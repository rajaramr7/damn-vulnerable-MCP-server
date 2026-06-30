# ai-surface in CI: gating the AI attack surface on this repo

This is a fork of [damn-vulnerable-MCP-server](https://github.com/harishsg993010/damn-vulnerable-MCP-server)
wired with [ai-surface](https://github.com/apisec-inc/AI-Surface) running as a GitHub Action. On every
pull request it maps the AI attack surface and fails the build when a high-severity surface is present,
posting the full inventory as a PR comment. A gate, not a one-time audit.

Everything here is reproducible: the tool is open source (`pip install apisec-ai-surface`) and this repo
is public.

## See it work: PR #1

[PR #1](../../pull/1) adds one file, `billing_mcp_server.py`: a new in-house MCP server exposing an
`issue_refund` (financial) and a `delete_account` (destructive) tool to the model, with no
human-approval step.

| | main (baseline) | PR #1 |
|---|---|---|
| MCP servers detected | 22 (medium) | 23 |
| Highest severity | medium | **high** |
| High finding | none | `financial action exposed` on `billing-mcp` |
| Gate result (`fail-on: high`) | **pass** | **fail** |

The ai-surface check on PR #1 turns red, and the bot comments the finding by name: `billing-mcp`, with
`in-house MCP server`, `unverified source`, `financial action exposed`. The 22 pre-existing MCP servers
are `medium` and sit below the `high` gate, so `main` stays green. A tool that can move money or delete
data, added with no approval step, cannot slip into the codebase unnoticed.

## The workflow

[`.github/workflows/ai-surface.yml`](.github/workflows/ai-surface.yml):

```yaml
name: AI Surface
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
  pull-requests: write
jobs:
  ai-surface:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: apisec-inc/AI-Surface@v1
        with:
          comment-on-pr: 'true'
          fail-on: 'high'
```

- **`comment-on-pr: true`** posts (and updates) the AI-surface inventory on the PR.
- **`fail-on: high`** fails the build when a high-severity AI surface is present. To accept a known
  baseline and fail only on *net-new* findings, ai-surface supports a committed baseline via the CLI
  (`ai-surface scan . --update-baseline`, then `--baseline --fail-on high`); see the
  [CI integration docs](https://github.com/apisec-inc/AI-Surface/blob/main/docs/CI_INTEGRATION.md).

## Reproduce it yourself

```
pip install apisec-ai-surface
ai-surface scan .
```

ai-surface reads source and config; it never executes project code and makes no network calls.

---

- Tool and source: https://github.com/apisec-inc/AI-Surface?utm_source=ci-demo&utm_medium=github&utm_campaign=muhd-ci
- State of AI Surface report: https://labs.apisec.ai/pulse?utm_source=ci-demo&utm_medium=github&utm_campaign=muhd-ci
- ai-surface maps and gates the AI attack surface in code. Proving which findings are exploitable at
  runtime is the APIsec platform.

*ai-surface performs discovery and code-level audit. Category presence is not a claim of exploitability;
a financial tool on an MCP server is a shape worth a look, not a proven vulnerability.*
