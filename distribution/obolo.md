# Obolo marketplace distribution

Status: staged pending provider account activation.

Horse Truth can publish its derived machine-intelligence API through Obolo's paid reverse-proxy marketplace.

Commercial settings:
- Proposed launch price: US$0.02 per successful call.
- Published Obolo platform fee: 10%.
- Expected gross provider share: US$0.018 per successful paid call before payout, processor, and tax costs.
- Derived intelligence only; raw provider records are not included.

Billing rule:
- Obolo-routed purchases use Obolo as the billing authority.
- The same request must not also consume a Horse Truth direct credit.
- Production activation requires authenticated proof that the request came through the paid Obolo provider path.

Activation:
1. Create the Obolo provider account.
2. Add a dedicated Horse Truth marketplace endpoint.
3. Configure price, documentation, accepted chains, and payout preference.
4. Verify the Obolo payment-required flow.
5. Configure authenticated provider-to-origin access.
6. Map authenticated Obolo requests to the marketplace billing authority.
7. Run the existing derived-intelligence operation without a second charge.
8. Publish and verify marketplace and MCP discovery.

Production authority over Horse Truth scientific selection: 0.
