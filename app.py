import json
import os
from pathlib import Path

import requests
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

CORE_BASE_URL = (os.environ.get("CORE_BASE_URL") or "https://horsetruth.com.au").rstrip("/")
APIFY_URL = "https://apify.com/crocheted_poacher/horse-truth-machine-intelligence"
VERSION = "1.0.0"

TOOL_DEFS = [
    {
        "name": "sandbox_preview",
        "description": "FREE: Return a fixed Horse Truth schema/capability preview. No paid entitlement is consumed.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True},
    },
    {
        "name": "discover_purchase_options",
        "description": "FREE: Return Horse Truth machine pricing and the preferred autonomous payment route.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True},
    },
    {
        "name": "horse_intelligence",
        "description": "PAID: Derived Horse Truth intelligence for one named Australian racehorse.",
        "inputSchema": {"type": "object", "properties": {"horse": {"type": "string"}}, "required": ["horse"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
    {
        "name": "horse_changes",
        "description": "PAID: Material Horse Truth change events for one named Australian racehorse.",
        "inputSchema": {"type": "object", "properties": {"horse": {"type": "string"}}, "required": ["horse"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
    {
        "name": "resolve_horse",
        "description": "PAID: Resolve a horse identity against Horse Truth profiles.",
        "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
    {
        "name": "horse_rankings",
        "description": "PAID: Current derived Horse Truth rankings.",
        "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 100}}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False},
    },
]


def public_base() -> str:
    configured = (os.environ.get("PUBLIC_BASE_URL") or "").strip().rstrip("/")
    if configured:
        return configured
    return request.url_root.rstrip("/")


def commerce() -> dict:
    base = public_base()
    return {
        "preferredAutonomousPath": {
            "provider": "APIFY",
            "url": APIFY_URL,
            "billingAuthority": "APIFY_PAY_PER_EVENT",
            "priceUsdPerSuccessfulResult": 0.02,
            "operations": ["horse_intelligence", "horse_changes", "resolve_horse", "horse_rankings"],
            "reason": "Platform-metered Pay-Per-Event avoids browser checkout and Horse Truth key claiming.",
        },
        "preferredDirectPath": {
            "provider": "HORSE_TRUTH_STRIPE",
            "productKey": "AI_AGENT_TRIAL",
            "priceAud": 1.0,
            "credits": 50,
            "effectiveAudPerCredit": 0.02,
            "checkout": {
                "method": "POST",
                "url": base + "/api/v1/machine/checkout",
                "json": {"product_key": "AI_AGENT_TRIAL"},
            },
        },
        "microOffer": {
            "productKey": "AI_AGENT_MICRO",
            "priceAud": 5.0,
            "credits": 250,
            "effectiveAudPerCredit": 0.02,
        },
        "productionAuthority": 0,
    }


def forward_headers() -> dict:
    headers = {
        "Content-Type": request.headers.get("Content-Type", "application/json"),
        "User-Agent": request.headers.get("User-Agent", "HorseTruth-MCP-Gateway/1.0"),
        "X-Horse-Truth-Gateway": "1",
    }
    for name in ("Authorization", "X-Horse-Truth-Key"):
        value = request.headers.get(name)
        if value:
            headers[name] = value
    return headers


def proxy(path: str, *, timeout: float = 15.0):
    url = CORE_BASE_URL + path
    body = request.get_data() if request.method not in ("GET", "HEAD") else None
    last_error = None
    for _ in range(2):
        try:
            upstream = requests.request(
                request.method,
                url,
                params=request.args,
                data=body,
                headers=forward_headers(),
                timeout=timeout,
                allow_redirects=False,
            )
            if upstream.status_code < 500:
                excluded = {"content-length", "transfer-encoding", "connection", "content-encoding"}
                headers = [(k, v) for k, v in upstream.headers.items() if k.lower() not in excluded]
                return Response(upstream.content, upstream.status_code, headers)
            last_error = f"HTTP_{upstream.status_code}"
        except requests.RequestException as exc:
            last_error = type(exc).__name__
    return None, last_error


def degraded_payload(reason: str | None = None) -> dict:
    return {
        "status": "CORE_TEMPORARILY_UNAVAILABLE",
        "retryable": True,
        "retryAfterSeconds": 15,
        "commerce": commerce(),
        "reason": reason or "upstream_unavailable",
        "productionAuthority": 0,
    }


@app.get("/health")
def health():
    return jsonify({"status": "PASS", "service": "HORSE_TRUTH_STATELESS_MCP_GATEWAY", "version": VERSION, "productionAuthority": 0})


@app.get("/")
def root():
    return jsonify({
        "name": "Horse Truth MCP Gateway",
        "status": "PASS",
        "mcp": public_base() + "/api/v1/mcp",
        "discovery": public_base() + "/api/v1/machine/discovery",
        "commerce": commerce(),
        "productionAuthority": 0,
    })


@app.get("/api/v1/machine/discovery")
def discovery():
    return jsonify({
        "status": "PASS",
        "service": "Horse Truth Machine Intelligence",
        "mcp": public_base() + "/api/v1/mcp",
        "coreRuntime": CORE_BASE_URL,
        "commerce": commerce(),
        "derivedOutputOnly": True,
        "productionAuthority": 0,
    })


@app.get("/api/v1/machine/products")
def products():
    return jsonify({
        "status": "PASS",
        "products": [
            {"product_key": "AI_AGENT_TRIAL", "billing_mode": "ONE_TIME_CREDIT_PACK", "currency": "AUD", "price": 1.0, "credits": 50},
            {"product_key": "AI_AGENT_MICRO", "billing_mode": "ONE_TIME_CREDIT_PACK", "currency": "AUD", "price": 5.0, "credits": 250},
            {"product_key": "APIFY_PAY_PER_EVENT", "billing_mode": "MARKETPLACE_PAY_PER_EVENT", "currency": "USD", "price": 0.02, "url": APIFY_URL},
        ],
        "productionAuthority": 0,
    })


@app.route("/api/v1/machine/checkout", methods=["POST"])
def checkout():
    proxied = proxy("/api/v1/machine/checkout", timeout=20)
    if not isinstance(proxied, tuple):
        return proxied
    _, reason = proxied
    payload = degraded_payload(reason)
    payload["message"] = "Direct Stripe checkout is temporarily unavailable during a core transition. The Apify Pay-Per-Event route remains available."
    return jsonify(payload), 503, {"Retry-After": "15"}


@app.route("/api/v1/machine/claim", methods=["POST"])
def claim():
    proxied = proxy("/api/v1/machine/claim", timeout=20)
    if not isinstance(proxied, tuple):
        return proxied
    _, reason = proxied
    return jsonify(degraded_payload(reason)), 503, {"Retry-After": "15"}


@app.get("/api/v1/sandbox/chance-with-wolves")
def sandbox():
    return jsonify({
        "status": "PASS",
        "sample": True,
        "sampleType": "SCHEMA_AND_CAPABILITY_PREVIEW",
        "horse": "Chance With Wolves",
        "capabilities": ["identity_resolution", "derived_intelligence", "change_detection", "mcp"],
        "derivedOutputOnly": True,
        "rawProviderDataIncluded": False,
        "oddsOrMarketPricesUsed": False,
        "productionAuthority": 0,
    })


@app.get("/.well-known/mcp.json")
def mcp_manifest():
    base = public_base()
    doc = {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": "au.com.horsetruth/machine-intelligence",
        "title": "Horse Truth Machine Intelligence",
        "description": "Remote derived Australian horse racing intelligence with a stateless discovery gateway and platform-billed autonomous purchase path.",
        "version": VERSION,
        "remotes": [{"type": "streamable-http", "url": base + "/api/v1/mcp"}],
    }
    return jsonify(doc)


@app.get("/api/v1/mcp/server-card")
def server_card():
    return mcp_manifest()


@app.get("/llms.txt")
def llms_txt():
    base = public_base()
    body = "\n".join([
        "# Horse Truth Machine Intelligence",
        f"- MCP: {base}/api/v1/mcp",
        f"- Discovery: {base}/api/v1/machine/discovery",
        f"- Preferred autonomous billing: Apify Pay-Per-Event US$0.02/successful result: {APIFY_URL}",
        "- Direct starter: A$1 one-time = 50 machine credits",
        "- Derived intelligence only; raw provider records are not exposed.",
        "- Production authority over Race Day scientific selection: 0",
        "",
    ])
    return Response(body, 200, {"Content-Type": "text/plain; charset=utf-8"})


@app.route("/api/v1/mcp", methods=["POST"])
def mcp():
    body = request.get_json(silent=True) or {}
    method = str(body.get("method") or "")
    req_id = body.get("id")

    if method == "initialize":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "Horse Truth Machine Intelligence", "version": VERSION},
            },
        })
    if method == "notifications/initialized":
        return Response(status=204)
    if method == "tools/list":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOL_DEFS}})
    if method == "tools/call":
        params = body.get("params") or {}
        name = str(params.get("name") or "")
        if name == "discover_purchase_options":
            result = {"status": "PASS", "commerce": commerce(), "productionAuthority": 0}
            return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, sort_keys=True)}], "structuredContent": result}})
        if name == "sandbox_preview":
            result = {
                "status": "PASS", "sample": True, "horse": "Chance With Wolves",
                "derivedOutputOnly": True, "rawProviderDataIncluded": False,
                "capabilities": ["identity_resolution", "derived_intelligence", "change_detection", "mcp"],
                "productionAuthority": 0,
            }
            return jsonify({"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, sort_keys=True)}], "structuredContent": result}})

    proxied = proxy("/api/v1/mcp", timeout=20)
    if not isinstance(proxied, tuple):
        return proxied
    _, reason = proxied
    data = degraded_payload(reason)
    return jsonify({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32003,
            "message": "Horse Truth core intelligence is temporarily unavailable; autonomous marketplace billing remains available.",
            "data": data,
        },
    }), 503, {"Retry-After": "15"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
