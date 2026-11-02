# AI Agent and MCP Security Gateway

A small educational prototype for the presentation topic. It demonstrates a security gateway that mediates access between an AI agent and a set of mock tools.

## Features
- API-key authentication (demo keys only)
- Role-based access control: Viewer, Developer, Admin
- Tool allow-list and least-privilege enforcement
- Human approval requirement for the high-risk `update_record` tool
- JSON-lines audit log (`audit.log`)
- Simple dashboard and interactive API docs

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` for the dashboard and `http://127.0.0.1:8000/docs` for API testing.

## Demo API keys
Use the `X-API-Key` header in Swagger (`/docs`):
- Viewer: `viewer-demo-key`
- Developer: `developer-demo-key`
- Admin: `admin-demo-key`

## Suggested demonstration
1. Call `GET /health`.
2. Call `GET /tools` as Viewer. Only `get_status` should appear.
3. Call `POST /tools/call` with `{"tool_name":"search_records","arguments":{"query":"sample"}}` as Viewer. Expect HTTP 403.
4. Repeat the search as Developer. Expect success.
5. Call `update_record` as Admin without `human_approval`. Expect HTTP 403.
6. Repeat with `human_approval: true`. The response clearly says the update is simulated and no data changed.
7. Call `GET /audit` as Admin to review allowed and blocked events.

## Example request body

```json
{
  "tool_name": "update_record",
  "arguments": {"record_id": "REC-101", "new_value": "Approved"},
  "human_approval": true
}
```

## Architecture
`Client / AI Agent → Authentication → Role & Permission Check → Risk / Approval Check → Mock Tool → Audit Log → Response`

## Important limitations
This is a classroom prototype, not a production MCP implementation. It demonstrates MCP gateway security concepts over a simple REST API; it does not implement the MCP JSON-RPC protocol, connect to a real LLM, or invoke external services. Credentials are hard-coded demo values. For production, use OAuth/OIDC, secret management, TLS, policy-as-code, rate limiting, input/output validation, tamper-resistant centralized logs, and an actual MCP client/server integration.
