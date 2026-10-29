# Approved branding — publishing pending

User approved the ivory italic J favicon. Source: assets/favicon.svg. Matching 1200x630 social-card source: assets/social-card.svg.

Ordinary content writes succeeded, but writing .github/workflows/publish-branding.yml returned 403 Resource not accessible by personal access token. No workflow was created, PNGs have NOT been generated, and index.html has NOT been changed. Do not claim the new branding is active yet.

## Finish via GitHub UI (no token changes needed)
1. Open maintenance/publish-branding.workflow.yml in the GitHub editor. Rename/move it to .github/workflows/publish-branding.yml and commit to main.
2. Under Actions choose Publish approved personal branding, Run workflow, main.
3. The workflow renders PNGs using pinned CairoSVG 2.7.1, adds static Open Graph/Twitter metadata, replaces the favicon link, commits the result, and requests a Pages rebuild. It uses only GitHub's temporary built-in token, not a custom secret. Check its run and Pages deployment for success.
4. Verify https://jocabe.com/ with cache bypass, all /assets/ image URLs, PNG dimensions and image/png content type; verify metadata in raw HTML and page body unchanged. Test desktop/mobile navigation. Actual third-party social preview caches may need refresh.

Alternatively grant the connected fine-grained token Workflows: Read and write for Jomcabe/jomcabe.github.io so the agent can install the workflow. Classic tokens need workflow scope. Never paste tokens into chat.

## Finish locally without Actions
With Python and Cairo installed: pip install CairoSVG==2.7.1; python3 scripts/publish-branding.py. Review diff, commit index.html and generated assets/*.png, push main, wait for Pages. Neither the site nor visitors need Python; these are one-time asset generation tools.
