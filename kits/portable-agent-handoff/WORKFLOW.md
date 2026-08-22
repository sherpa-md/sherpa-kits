# Workflow

| Stage | Agent action | Required receipt | Stop condition |
|---|---|---|---|
| 1. Inventory | Inspect OS, workspace, Git, connectors, and repository target | Tools and interfaces found | None |
| 2. Read preflight | Run harmless repository and filesystem reads | `AVAILABLE_READ` or exact failure class | Authentication required |
| 3. Permission map | Read explicit connector/repository permissions | Read/write/admin/unknown map | Permission denied |
| 4. Workspace bootstrap | Select, clone, or initialize without overwriting work | Workspace path and Git state | Existing conflicting work |
| 5. Validation | Run repository-provided checks | Commands and exit results | Tests fail |
| 6. First write | Create a feature branch or requested file | Diff and target branch | Human approval required |
| 7. Optional bus | Configure message-only coordination | Round-trip lifecycle receipt | Missing recipient-owned config |
| 8. Handoff complete | Summarize verified capabilities and remaining limits | Final receipt table | None |

## Failure classification

| Result | Meaning | Next action |
|---|---|---|
| `AUTH_REQUIRED` | The relevant interface explicitly requested authentication | Complete that provider flow |
| `PERMISSION_DENIED` | Identity is known but lacks required permission | Repository owner adjusts access |
| `TOOL_UNAVAILABLE` | Relevant interface is not installed or exposed after discovery | Install or enable the named interface |
| `TRANSIENT_FAILURE` | Timeout, rate limit, or temporary service failure | Retry safely with backoff |
| `UNKNOWN` | Evidence is insufficient or contradictory | Gather one more targeted probe |

Never replace a specific classification with “it does not work.”

