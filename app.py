from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime, timezone
from pathlib import Path
import json

app = FastAPI(title="AI Agent MCP Security Gateway", version="1.0.0")
LOG_FILE = Path("audit.log")

# Demo credentials only. Replace with a proper identity provider in production.
USERS = {
    "viewer-demo-key": {"user": "demo_viewer", "role": "viewer"},
    "developer-demo-key": {"user": "demo_developer", "role": "developer"},
    "admin-demo-key": {"user": "demo_admin", "role": "admin"},
}
ROLE_PERMISSIONS = {
    "viewer": {"get_status"},
    "developer": {"get_status", "search_records"},
    "admin": {"get_status", "search_records", "update_record"},
}
RISKY_TOOLS = {"update_record"}

class ToolRequest(BaseModel):
    tool_name: str
    arguments: dict = {}
    human_approval: bool = False


def audit(event: dict):
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def identify(api_key: str | None):
    user = USERS.get(api_key or "")
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorised: valid API key required")
    return user


def execute_mock_tool(name: str, args: dict):
    # Harmless mock tools: no real database or external system is modified.
    if name == "get_status":
        return {"service": "demo-record-service", "status": "healthy"}
    if name == "search_records":
        query = str(args.get("query", ""))[:100]
        return {"query": query, "results": [{"id": "REC-101", "label": "Sample record"}]}
    if name == "update_record":
        record_id = str(args.get("record_id", ""))[:40]
        new_value = str(args.get("new_value", ""))[:100]
        return {"message": "SIMULATED update only; no data was changed", "record_id": record_id, "new_value": new_value}
    raise HTTPException(status_code=404, detail="Unknown tool")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (Path("templates/index.html").read_text(encoding="utf-8"))

@app.get("/health")
def health():
    return {"status": "ok", "project": "AI Agent MCP Security Gateway"}

@app.get("/tools")
def list_tools(x_api_key: str | None = Header(default=None)):
    user = identify(x_api_key)
    allowed = ROLE_PERMISSIONS[user["role"]]
    tools = [
        {"name": "get_status", "description": "Read service status", "risk": "low"},
        {"name": "search_records", "description": "Search sample records", "risk": "low"},
        {"name": "update_record", "description": "Simulate a record update", "risk": "high"},
    ]
    audit({"event": "list_tools", "user": user["user"], "role": user["role"]})
    return {"role": user["role"], "tools": [t for t in tools if t["name"] in allowed]}

@app.post("/tools/call")
def call_tool(request: ToolRequest, x_api_key: str | None = Header(default=None)):
    user = identify(x_api_key)
    name = request.tool_name
    if name not in ROLE_PERMISSIONS[user["role"]]:
        audit({"event": "blocked_permission", "user": user["user"], "tool": name, "result": "denied"})
        raise HTTPException(status_code=403, detail="Blocked by gateway: role does not have permission")
    if name in RISKY_TOOLS and not request.human_approval:
        audit({"event": "blocked_approval", "user": user["user"], "tool": name, "result": "approval_required"})
        raise HTTPException(status_code=403, detail="Human approval required for this high-risk tool")
    result = execute_mock_tool(name, request.arguments)
    audit({"event": "tool_call", "user": user["user"], "role": user["role"], "tool": name, "result": "success"})
    return {"gateway": "approved", "tool": name, "result": result}

@app.get("/audit")
def get_audit(x_api_key: str | None = Header(default=None)):
    user = identify(x_api_key)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin role required to view audit log")
    if not LOG_FILE.exists():
        return {"events": []}
    events = [json.loads(line) for line in LOG_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {"events": events[-100:]}
