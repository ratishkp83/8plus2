# 8plus2

Marketing site for **8plus2 Omnitech (OPC) Pvt Ltd** — makers of Turrigan (AI governance) and Sentinel PMO (project assurance).

Live at [8plus2.co.in](https://8plus2.co.in).

## What this is

A single, self-contained static page: [`index.html`](index.html). All CSS is inline; fonts load from Google Fonts. No build step.

## Hosting

Domain registered at GoDaddy, DNS + CDN on Cloudflare, page served by Cloudflare Pages. To change content, edit `index.html` and push to `main`; Cloudflare Pages redeploys automatically.

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python -m http.server 8080
```
