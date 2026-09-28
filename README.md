# Horse Truth MCP

Remote Model Context Protocol (MCP) access to Horse Truth derived Australian racehorse intelligence.

Horse Truth provides machine-readable derived intelligence for AI agents and software. This public repository is a distribution and discovery surface only; the proprietary Horse Truth production source remains private.

## Remote MCP endpoint

```text
https://horsetruth.com.au/api/v1/mcp
```

Official MCP Registry identifier:

```text
au.com.horsetruth/machine-intelligence
```

Registry manifest:

```text
https://horsetruth.com.au/.well-known/mcp.json
```

Server card:

```text
https://horsetruth.com.au/api/v1/mcp/server-card
```

## Available tools

- `horse_intelligence` — derived intelligence for one named horse.
- `horse_changes` — material Horse Truth change events for one horse.
- `resolve_horse` — resolve a horse identity against Horse Truth profiles.
- `horse_rankings` — current derived Horse Truth rankings.

## Free discovery

Use the free MCP discovery tool:

```text
discover_purchase_options
```

Or inspect:

```text
https://horsetruth.com.au/api/v1/machine/discovery
https://horsetruth.com.au/llms.txt
https://horsetruth.com.au/llms-full.txt
```

## Fastest paid paths

For accountless machine-to-machine payment, use Horse Truth's native **x402** routes. Paid operations return a standard `402 Payment Required` instruction; submit the payment signature and retry the equivalent x402 route. No Horse Truth account or API-key signup is required.

For a browser/card purchase, the direct **A$1 starter checkout** is one click:

```text
https://horsetruth.com.au/buy/starter
```

It provides **50 Horse Truth machine credits** after successful payment and claim.

For marketplace-metered usage, the **Apify Pay-Per-Event** Actor remains available at **US$0.02 per successful result**:

```text
https://apify.com/crocheted_poacher/horse-truth-machine-intelligence
```

The free MCP tool `discover_purchase_options` and paid HTTP 402 responses expose the currently available payment paths.

Example MCP intent:

```json
{"jsonrpc":"2.0","id":"1","method":"tools/call","params":{"name":"horse_intelligence","arguments":{"horse":"Chance With Wolves"}}}
```

## Machine access and pricing

Horse Truth exposes three self-service payment paths:

- Native x402: **US$0.02 per successful result** on x402-enabled operations.
- Direct Horse Truth starter: **A$1 one-time for 50 machine credits**.
- Apify marketplace: **US$0.02 per successful result** through Apify Pay-Per-Event.

One-click direct checkout:

```text
https://horsetruth.com.au/buy/starter
```

Programmatic checkout remains available:

```http
POST https://horsetruth.com.au/api/v1/machine/checkout
Content-Type: application/json

{"product_key":"AI_AGENT_TRIAL"}
```

After payment, claim the issued machine key at:

```text
POST https://horsetruth.com.au/api/v1/machine/claim
```

Apify marketplace:

```text
https://apify.com/crocheted_poacher/horse-truth-machine-intelligence
```

## Protocol surfaces

- MCP: `https://horsetruth.com.au/api/v1/mcp`
- A2A agent card: `https://horsetruth.com.au/.well-known/agent-card.json`
- A2A JSON-RPC: `https://horsetruth.com.au/api/v1/a2a`
- AI catalog: `https://horsetruth.com.au/.well-known/ai-catalog.json`
- OpenAPI: `https://horsetruth.com.au/api/v1/machine/openapi.json`

## Evidence boundary

Horse Truth exposes derived intelligence only. Raw provider records are not exposed through this MCP surface. Commercial and distribution code has production authority 0 over Race Day scientific selection.

## Status

Production endpoint:

```text
https://horsetruth.com.au/api/v1/health
```

Canonical production is deployed from the private Horse Truth source repository; this public repository exists for MCP discovery, interoperability, and directory indexing.
