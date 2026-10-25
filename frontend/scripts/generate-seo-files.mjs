import { mkdirSync, writeFileSync } from "node:fs"

// Netlify fournit URL automatiquement ; VITE_SITE_URL sert de secours.
const siteUrl = (process.env.URL || process.env.VITE_SITE_URL || "").replace(/\/$/, "")

if (!siteUrl) {
  console.warn("Aucune URL de site trouvée (URL / VITE_SITE_URL) : robots.txt et sitemap.xml non générés.")
  process.exit(0)
}

mkdirSync("public", { recursive: true })

writeFileSync(
  "public/robots.txt",
  `User-agent: *\nAllow: /\nSitemap: ${siteUrl}/sitemap.xml\n`
)

writeFileSync(
  "public/sitemap.xml",
  `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>${siteUrl}/</loc></url>
</urlset>
`
)

console.log(`robots.txt et sitemap.xml générés pour ${siteUrl}`)