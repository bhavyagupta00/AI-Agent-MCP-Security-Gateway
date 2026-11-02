# Build and validate this project with IBM Bob

Use the prompts below in IBM Bob. Start in **Plan** mode, review the plan, then switch to **Agent** mode. Bob's tools can read and write project files, run commands, and work with MCP integrations; review every proposed change before accepting it.

## Prompt 1 — Plan mode

I am building a student project titled “AI Agent and MCP Security Gateway”. Inspect this repository and create an implementation plan. The prototype must demonstrate API-key authentication, role-based access control (Viewer/Developer/Admin), least-privilege tool allow-lists, human approval for high-risk tools, and audit logging. Keep tools harmless and mocked. Do not claim this is a production MCP implementation. Identify security gaps and propose tests before changing code.

## Prompt 2 — Agent mode: improve implementation

Implement the approved plan in this Python FastAPI project. Keep all tools mocked and non-destructive. Add robust validation, consistent error responses, unit tests for unauthenticated requests, role-denied requests, permitted calls, approval-required calls, and admin-only audit access. Do not store real secrets in source code. Update README with exact run and demo instructions. Run the tests and fix failures.

## Prompt 3 — Security review (Ask mode)

Review this project as a security reviewer. Check authentication, authorization, privilege escalation, approval bypass, input validation, audit-log integrity, secret handling, and error leakage. List findings by severity with file and line references. Do not modify files yet.

## Prompt 4 — Test and documentation (Agent mode)

Generate a clear architecture diagram in Mermaid, a concise project report, and a test-results summary based only on tests you actually run. Clearly distinguish implemented features from recommendations and limitations. Do not describe the REST demo as a full MCP protocol gateway.

## IBM Bob workflow evidence to capture for the college demo

1. Screenshot of Bob **Plan** mode showing the generated implementation plan.
2. Screenshot of Bob **Agent** mode creating or improving the code.
3. Screenshot of Bob running the test suite with the actual result.
4. Screenshot of Bob **Ask** mode security review.
5. Screenshot of the running dashboard and `/docs` API test.

Only claim Bob performed a step after you have actually run it in Bob and captured the result.
