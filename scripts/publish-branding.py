"""Render sharing PNGs and install metadata without changing page body/layout.
Requires Python 3 + CairoSVG 2.7.1. Run from any directory.
"""
from pathlib import Path
import re
import cairosvg
root = Path(__file__).resolve().parents[1]
for source, dest, width, height in [
    ('assets/social-card.svg', 'assets/social-card.png', 1200, 630),
    ('assets/favicon.svg', 'assets/favicon-32.png', 32, 32),
    ('assets/favicon.svg', 'assets/apple-touch-icon.png', 180, 180),
]:
    cairosvg.svg2png(url=str(root/source), write_to=str(root/dest), output_width=width, output_height=height)
page = root/'index.html'
html = page.read_text()
before_body = html.split('<body',1)[1]
html = re.sub(r'\s*<!-- Jocabe branding start -->.*?<!-- Jocabe branding end -->', '', html, flags=re.S)
html = re.sub(r'\s*<link\b(?=[^>]*\brel=[\"\']icon[\"\'])[^>]*>', '', html)
block = '''
    <!-- Jocabe branding start -->
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png?v=j1">
    <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg?v=j1">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png?v=j1">
    <meta name="description" content="Jose Carvajal-Beltran — Materials Science &amp; Engineering undergraduate at MIT. Research, hardware projects, and notes.">
    <link rel="canonical" href="https://jocabe.com/">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Jocabe">
    <meta property="og:title" content="Jose Carvajal-Beltran">
    <meta property="og:description" content="Materials Science &amp; Engineering at MIT. Research, hardware projects, and notes.">
    <meta property="og:url" content="https://jocabe.com/">
    <meta property="og:image" content="https://jocabe.com/assets/social-card.png?v=j1">
    <meta property="og:image:secure_url" content="https://jocabe.com/assets/social-card.png?v=j1">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Ivory J monogram on navy with Jose Carvajal-Beltran, Materials Science &amp; Engineering at MIT, and jocabe.com.">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Jose Carvajal-Beltran">
    <meta name="twitter:description" content="Materials Science &amp; Engineering at MIT. Research, hardware projects, and notes.">
    <meta name="twitter:image" content="https://jocabe.com/assets/social-card.png?v=j1">
    <meta name="twitter:image:alt" content="Jose Carvajal-Beltran — Materials Science &amp; Engineering at MIT.">
    <!-- Jocabe branding end -->'''
assert html.count('</title>') == 1, 'Expected exactly one title'
html = html.replace('</title>', '</title>'+block, 1)
assert html.split('<body',1)[1] == before_body, 'Page body must remain unchanged'
page.write_text(html)
print('Rendered PNG assets and installed static metadata; body unchanged.')
