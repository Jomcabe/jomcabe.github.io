# Approved personal branding — published

The owner approved the ivory italic J on navy. Activated in generated commit 7fad0d04eb98f4c538154b07b0f547e7a412df78.

- Site: https://jocabe.com/
- SVG favicon: /assets/favicon.svg?v=j1
- 32x32 fallback: /assets/favicon-32.png?v=j1
- 180x180 Apple touch icon: /assets/apple-touch-icon.png?v=j1
- 1200x630 PNG share image: https://jocabe.com/assets/social-card.png?v=j1
- Static Open Graph and Twitter large-image tags, description and canonical URL are in index.html. No page-body/layout/content changes.

Workflow Publish approved personal branding run 40809586064 succeeded; Pages deployment 40809677261 succeeded. The permission issue was resolved by the owner. Active workflow: .github/workflows/publish-branding.yml. maintenance/publish-branding.workflow.yml is the earlier inactive template, not required to run or move.

## Verified with Playwright
- Live cache-bypassed HTML contains new SVG favicon and static social metadata.
- All four image assets HTTPS 200; PNG Content-Type image/png; dimensions 32x32, 180x180, 1200x630.
- Compared source body before/after: byte-for-byte unchanged.
- Desktop navigation: Research, Academics, Projects, Future Projects, Resume, Log, Home.
- 390x844 Chromium viewport: academic Year 2 tab and Home navigation; no horizontal overflow.
- No page JavaScript errors in navigation test. Existing external embed/browser warnings not exhaustively audited.
- Actual Facebook/LinkedIn/X/iMessage preview rendering and caches not tested; metadata and public PNG delivery verified, not platform-specific behavior.

## Maintenance
Edit approved source SVGs or scripts/publish-branding.py and push main; path-filtered workflow renders PNGs, updates head metadata and requests Pages rebuild. Can also run through Actions > Publish approved personal branding > Run workflow. Python/CairoSVG are asset-generation tools only; site visitors need neither. Checkout action pinned by SHA; CairoSVG 2.7.1 pinned. Only built-in ephemeral GitHub token used; no custom secrets committed.

Share platforms may cache previous previews; request a re-scrape with their tools if needed. Browser favicon caches can persist; hard refresh/reopen tab or wait. Body remains intentionally unchanged.
