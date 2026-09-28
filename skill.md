# Horse Truth Machine Intelligence

Derived Australian racehorse intelligence for autonomous agents and software.

## What this service does

- Resolve Australian racehorse identities.
- Return current derived horse intelligence, snapshots, explanations and named signals.
- Return material Horse Truth state changes.
- Return current derived rankings.
- Return comparison and provenance receipts.
- Raw provider records are not exposed.
- Commercial/distribution code has production authority 0 over Race Day scientific selection.

## Free discovery

- MCP: https://horse-truth-edge-production.up.railway.app/api/v1/mcp
- MCP server card: https://horsetruth.com.au/api/v1/mcp/server-card
- x402 manifest: https://horsetruth.com.au/.well-known/x402
- OpenAPI: https://horsetruth.com.au/openapi.json
- Machine discovery: https://horsetruth.com.au/api/v1/machine/discovery
- Products: https://horsetruth.com.au/api/v1/machine/products
- Sandbox: https://horsetruth.com.au/api/v1/sandbox/chance-with-wolves

## Preferred autonomous payment

- Protocol: x402 v2
- Network: Base (`eip155:8453`)
- Asset: USDC
- Atomic price: US$0.02 per successful result
- No Horse Truth account or API key is required for x402.
- Read `PAYMENT-REQUIRED`, authorize payment, retry with `PAYMENT-SIGNATURE`, and read `PAYMENT-RESPONSE`.

## Immediately executable examples

- Horse intelligence: https://horsetruth.com.au/api/v1/x402/horse-intelligence?horse=Chance%20With%20Wolves
- Rankings: https://horsetruth.com.au/api/v1/x402/rankings?limit=100
- Resolve identity: https://horsetruth.com.au/api/v1/x402/resolve-horse?q=Chance%20With%20Wolves
- Snapshot: https://horsetruth.com.au/api/v1/x402/horse-snapshot?horse=Chance%20With%20Wolves
- Explanation: https://horsetruth.com.au/api/v1/x402/horse-explanation?horse=Chance%20With%20Wolves

## Other purchase rails

- A$1 starter checkout: https://horsetruth.com.au/buy/starter
- A$1 starter pack includes 50 direct machine credits.
- Apify Pay-Per-Event fallback: https://apify.com/crocheted_poacher/horse-truth-machine-intelligence

## Integration

- MCP transport: https://horse-truth-edge-production.up.railway.app/api/v1/mcp
- A2A: https://horsetruth.com.au/api/v1/a2a
- Full machine guide: https://horsetruth.com.au/llms-full.txt

## Safety and evidence boundary

- Derived intelligence only.
- No wagering execution.
- No raw provider-data resale.
- Race Day chronology and scientific evidence are governed separately from commerce.
- production_authority: 0
