# Horse Truth MCP

Public discovery surface for the production Horse Truth remote Model Context Protocol server.

Horse Truth provides **derived Australian racehorse intelligence** for AI agents and software. This repository contains distribution metadata and a lightweight gateway only; proprietary Horse Truth production source, provider records, and scientific model internals remain private.

## Connect

Remote Streamable HTTP MCP:

```text
https://horsetruth.com.au/api/v1/mcp
```

Claude Code:

```bash
claude mcp add --transport http horse-truth https://horsetruth.com.au/api/v1/mcp
```

Generic configuration:

```json
{
  "mcpServers": {
    "horse-truth": {
      "url": "https://horsetruth.com.au/api/v1/mcp"
    }
  }
}
```

Official MCP Registry identifier:

```text
au.com.horsetruth/machine-intelligence
```

Useful public metadata:

- Server card: https://horsetruth.com.au/api/v1/mcp/server-card
- Machine discovery: https://horsetruth.com.au/api/v1/machine/discovery
- Products: https://horsetruth.com.au/api/v1/machine/products
- Tollbooth catalog: https://horsetruth.com.au/api/v1/machine/tollbooths
- OpenAPI: https://horsetruth.com.au/api/v1/machine/openapi.json
- LLM discovery: https://horsetruth.com.au/llms.txt
- Full LLM discovery: https://horsetruth.com.au/llms-full.txt
- Developers: https://horsetruth.com.au/developers

## Tools

Horse Truth currently exposes **11 MCP tools**.

### Free discovery tools

- `sandbox_preview` — fixed schema and capability preview.
- `discover_purchase_options` — current self-service purchase and machine-payment routes.

### Paid derived-intelligence tools

- `horse_intelligence` — derived intelligence for one named horse.
- `horse_changes` — material Horse Truth state-change events.
- `horse_rankings` — current derived rankings from the warmed canonical model cache.
- `resolve_horse` — resolve a horse identity against Horse Truth profiles.
- `horse_snapshot` — compact derived operating snapshot.
- `horse_explanation` — structured explanation of the current derived read.
- `horse_compare` — compare two to five horse snapshots.
- `horse_provenance` — cryptographic provenance receipt for derived intelligence.
- `horse_signal` — request one named derived signal such as readiness, biomechanics, class, reliability, progression or alerts.

All tools are read-only with respect to Horse Truth racing truth. Commercial/distribution code has **production authority 0** over Race Day scientific selection.

## Accountless x402 payment

The preferred autonomous rail is **x402**.

Paid tool metadata returned by `tools/list` exposes:

- price: **US$0.02 per successful call**
- settlement asset: **USDC**
- network: **Base — `eip155:8453`**
- `PAYMENT-REQUIRED`
- `PAYMENT-SIGNATURE`
- `PAYMENT-RESPONSE`
- an exact x402 execution URL template for that tool

Example rankings route:

```text
https://horsetruth.com.au/api/v1/x402/rankings?limit={limit}
```

An autonomous client can call the route, read the standard payment challenge, submit its payment signature, and retry the same route. No Horse Truth account or API-key claim is required for x402.

## Other payment rails

Direct reusable credits:

- A$1 starter pack
- 50 machine credits
- effective A$0.02 per successful direct call

One-click checkout:

```text
https://horsetruth.com.au/buy/starter
```

Programmatic checkout:

```http
POST https://horsetruth.com.au/api/v1/machine/checkout
Content-Type: application/json

{"product_key":"AI_AGENT_TRIAL"}
```

Apify Pay-Per-Event fallback:

```text
https://apify.com/crocheted_poacher/horse-truth-machine-intelligence
```

Current Apify price: **US$0.02 per successful result**.

## Example MCP request

List tools:

```json
{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}
```

Call derived horse intelligence:

```json
{
  "jsonrpc":"2.0",
  "id":"2",
  "method":"tools/call",
  "params":{
    "name":"horse_intelligence",
    "arguments":{"horse":"Chance With Wolves"}
  }
}
```

A caller without a direct entitlement receives machine-readable purchase navigation. Paid tool metadata also provides the exact x402 route template so an autonomous client does not need to infer payment routing.

## Protocol surfaces

- MCP: https://horsetruth.com.au/api/v1/mcp
- A2A agent card: https://horsetruth.com.au/.well-known/agent-card.json
- A2A JSON-RPC: https://horsetruth.com.au/api/v1/a2a
- AI catalog: https://horsetruth.com.au/.well-known/ai-catalog.json
- OpenAPI: https://horsetruth.com.au/api/v1/machine/openapi.json

## Evidence boundary

Horse Truth exposes derived intelligence only. Raw provider records are not sold or exposed through this MCP surface. Odds/market data does not gain authority over Horse Truth scientific conclusions through the commercial layer.

## Production health

```text
https://horsetruth.com.au/api/v1/health
```

Canonical production is deployed from the private Horse Truth source repository. This public repository exists only for discovery, interoperability, directory indexing, and integration examples.
