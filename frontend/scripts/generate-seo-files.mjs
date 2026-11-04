// Génère public/robots.txt et public/sitemap.xml avant chaque build.
// Le sitemap liste l'accueil + toutes les fiches produits (via l'API).
import { mkdirSync, writeFileSync } from "node:fs"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const siteUrl = (process.env.URL || process.env.VITE_SITE_URL || "").replace(/\/$/, "")
const apiUrl = (process.env.VITE_API_URL || "").replace(/\/$/, "")
const storeSlug = process.env.VITE_STORE_SLUG

const publicDir = join(dirname(fileURLToPath(import.meta.url)), "..", "public")
mkdirSync(publicDir, { recursive: true })

if (!siteUrl) {
  console.warn("[seo] URL du site inconnue (URL / VITE_SITE_URL) : robots.txt et sitemap.xml non générés.")
  process.exit(0)
}

// Render (offre gratuite) peut dormir : on laisse du temps et on réessaie.
async function fetchJson(url, attempts = 3) {
  for (let i = 1; i <= attempts; i++) {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(60_000) })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      return await response.json()
    } catch (err) {
      console.warn(`[seo] tentative ${i}/${attempts} échouée pour ${url} : ${err.message}`)
      if (i === attempts) throw err
      await new Promise((resolve) => setTimeout(resolve, 5_000))
    }
  }
}

async function fetchAllProductIds() {
  const ids = []
  let url = `${apiUrl}/stores/${storeSlug}/products/`
  while (url) {
    const page = await fetchJson(url)
    for (const product of page.results) ids.push(product.id)
    url = page.next
  }
  return ids
}

let productUrls = []
if (apiUrl && storeSlug) {
  try {
    const ids = await fetchAllProductIds()
    productUrls = ids.map((id) => `${siteUrl}/products/${id}`)
    console.log(`[seo] ${ids.length} produit(s) ajouté(s) au sitemap.`)
  } catch (err) {
    // On ne casse pas le déploiement : sitemap limité à l'accueil.
    console.warn(`[seo] API injoignable, sitemap limité à l'accueil : ${err.message}`)
  }
} else {
  console.warn("[seo] VITE_API_URL ou VITE_STORE_SLUG manquant : sitemap limité à l'accueil.")
}

const urls = [`${siteUrl}/`, ...productUrls]
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((loc) => `  <url><loc>${loc}</loc></url>`).join("\n")}
</urlset>
`

const robots = `User-agent: *
Allow: /
Sitemap: ${siteUrl}/sitemap.xml
`

writeFileSync(join(publicDir, "sitemap.xml"), sitemap)
writeFileSync(join(publicDir, "robots.txt"), robots)
console.log(`[seo] sitemap.xml (${urls.length} URL) et robots.txt générés.`)