import json
import os
from pathlib import Path

import requests
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

CORE_BASE_URL = (os.environ.get("CORE_BASE_URL") or "https://horsetruth.com.au").rstrip("/")
APIFY_URL = "https://apify.com/crocheted_poacher/horse-truth-machine-intelligence"
VERSION = "1.0.1"

def _paid_tool(name: str, description: str, input_schema: dict, x402_template: str) -> dict:
    return {
        "name": name,
        "description": "PAID: US$0.02 per successful autonomous x402 call, or 1 Horse Truth direct credit. " + description,
        "_meta": {
            "com.horsetruth/pricing": {
                "preferredAutonomousProvider": "X402",
                "pricePerCallUsd": 0.02,
                "pricingModel": "per_call",
                "anonymousCallable": True,
                "x402Currency": "USDC",
                "x402Network": "eip155:8453",
                "x402UrlTemplate": CORE_BASE_URL + x402_template,
                "marketplaceFallbackProvider": "APIFY",
                "apifyPriceUsdPerSuccessfulResult": 0.02,
            },
            "com.horsetruth/commerce": {
                "preferredProvider": "X402",
                "priceUsdPerSuccessfulResult": 0.02,
                "network": "eip155:8453",
                "paymentRequiredHeader": "PAYMENT-REQUIRED",
                "paymentSignatureHeader": "PAYMENT-SIGNATURE",
                "paymentResponseHeader": "PAYMENT-RESPONSE",
                "x402UrlTemplate": CORE_BASE_URL + x402_template,
                "oneClickStarterCheckoutUrl": CORE_BASE_URL + "/buy/starter",
                "apifyFallbackUrl": APIFY_URL,
            },
        },
        "inputSchema": input_schema,
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
    }


TOOL_DEFS = [
    {
        "name": "sandbox_preview",
        "description": "FREE: Return a fixed Horse Truth schema/capability preview. No paid entitlement is consumed.",
        "_meta": {"com.horsetruth/pricing": {"free": True, "units": 0}, "com.horsetruth/auth": {"required": False}},
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
    },
    {
        "name": "discover_purchase_options",
        "description": "FREE: Return Horse Truth machine pricing and autonomous purchase routes.",
        "_meta": {"com.horsetruth/pricing": {"free": True, "units": 0}, "com.horsetruth/auth": {"required": False}},
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "openWorldHint": False, "destructiveHint": False},
    },
    _paid_tool(
        "horse_intelligence",
        "Return derived intelligence for one named Australian racehorse.",
        {"type":"object","properties":{"horse":{"type":"string"}},"required":["horse"],"additionalProperties":False},
        "/api/v1/x402/horse-intelligence?horse={horse}",
    ),
    _paid_tool(
        "horse_changes",
        "Return material Horse Truth state-change events for one horse.",
        {"type":"object","properties":{"horse":{"type":"string"},"limit":{"type":"integer","minimum":1,"maximum":100}},"required":["horse"],"additionalProperties":False},
        "/api/v1/x402/horse-changes?horse={horse}",
    ),
    _paid_tool(
        "horse_rankings",
        "Return current derived Horse Truth rankings.",
        {"type":"object","properties":{"limit":{"type":"integer","minimum":1,"maximum":500}},"additionalProperties":False},
        "/api/v1/x402/rankings?limit={limit}",
    ),
    _paid_tool(
        "resolve_horse",
        "Resolve a horse identity against Horse Truth profiles.",
        {"type":"object","properties":{"query":{"type":"string"}},"required":["query"],"additionalProperties":False},
        "/api/v1/x402/resolve-horse?q={query}",
    ),
    _paid_tool(
        "horse_snapshot",
        "Return a compact derived operating snapshot for one horse.",
        {"type":"object","properties":{"horse":{"type":"string"}},"required":["horse"],"additionalProperties":False},
        "/api/v1/x402/horse-snapshot?horse={horse}",
    ),
    _paid_tool(
        "horse_explanation",
        "Return a structured explanation of the current derived Horse Truth read.",
        {"type":"object","properties":{"horse":{"type":"string"}},"required":["horse"],"additionalProperties":False},
        "/api/v1/x402/horse-explanation?horse={horse}",
    ),
    _paid_tool(
        "horse_compare",
        "Compare compact derived snapshots for two to five horses.",
        {"type":"object","properties":{"horses":{"type":"array","items":{"type":"string"},"minItems":2,"maxItems":5}},"required":["horses"],"additionalProperties":False},
        "/api/v1/x402/horse-compare?horses={horses}",
    ),
    _paid_tool(
        "horse_provenance",
        "Return a cryptographic provenance receipt for derived horse intelligence.",
        {"type":"object","properties":{"horse":{"type":"string"}},"required":["horse"],"additionalProperties":False},
        "/api/v1/x402/horse-provenance?horse={horse}",
    ),
    _paid_tool(
        "horse_signal",
        "Return one named derived Horse Truth signal for a horse.",
        {"type":"object","properties":{"horse":{"type":"string"},"signal":{"type":"string"}},"required":["horse","signal"],"additionalProperties":False},
        "/api/v1/x402/horse-signal?horse={horse}&signal={signal}",
    ),
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
            "provider": "X402",
            "routePrefix": CORE_BASE_URL + "/api/v1/x402/",
            "tollboothCatalog": CORE_BASE_URL + "/api/v1/machine/tollbooths",
            "network": "eip155:8453",
            "asset": "USDC",
            "priceUsdPerSuccessfulResult": 0.02,
            "paymentRequiredHeader": "PAYMENT-REQUIRED",
            "paymentSignatureHeader": "PAYMENT-SIGNATURE",
            "paymentResponseHeader": "PAYMENT-RESPONSE",
            "reason": "Accountless autonomous payment; paid tools advertise an exact x402 URL template.",
        },
        "marketplaceFallback": {
            "provider": "APIFY",
            "url": APIFY_URL,
            "billingAuthority": "APIFY_PAY_PER_EVENT",
            "priceUsdPerSuccessfulResult": 0.02,
        },
        "preferredDirectPath": {
            "provider": "HORSE_TRUTH_STRIPE",
            "productKey": "AI_AGENT_TRIAL",
            "priceAud": 1.0,
            "credits": 50,
            "effectiveAudPerCredit": 0.02,
            "checkoutUrl": CORE_BASE_URL + "/buy/starter",
            "checkout": {
                "method": "POST",
                "url": CORE_BASE_URL + "/api/v1/machine/checkout",
                "json": {"product_key": "AI_AGENT_TRIAL"},
            },
        },
        "publicGateway": base,
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
        "description": "Remote derived Australian racehorse intelligence with 11 MCP tools, accountless x402 payment, direct credits and Apify fallback.",
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
        "- Preferred autonomous billing: x402 US$0.02/successful call in USDC on Base (eip155:8453)",
        f"- Marketplace fallback: Apify Pay-Per-Event US$0.02/successful result: {APIFY_URL}",
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
                "protocolVersion": "2026-07-28",
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
            "message": "Horse Truth core intelligence is temporarily unavailable; use the advertised x402 or Apify fallback purchase path.",
            "data": data,
        },
    }), 503, {"Retry-After": "15"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
