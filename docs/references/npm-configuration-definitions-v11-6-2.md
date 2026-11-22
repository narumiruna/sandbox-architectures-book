---
title: "npm Configuration Definitions (v11.6.2)"
source_type: "web"
url: "https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js"
created: "2026-11-22"
updated: "2026-11-22"
---

# npm Configuration Definitions (v11.6.2)

[Original source](https://github.com/npm/cli/blob/v11.6.2/workspaces/config/lib/definitions/definitions.js)

## Content

`--offline` prevents npm from fetching packages over the network. It does not block network access for lifecycle scripts. `--ignore-scripts` skips package scripts; commands such as `npm test` still run the requested script, but not its pre- or post-scripts.
