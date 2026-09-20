/**
 * Assombrit une couleur hexadécimale d'un certain pourcentage.
 * Sert à générer automatiquement une variante "hover"/"dark" à partir
 * d'une seule couleur choisie par le commerçant.
 */
function darken(hex, amount = 0.18) {
  const clean = hex.replace("#", "")
  const num = parseInt(clean, 16)
  const r = Math.max(0, Math.floor(((num >> 16) & 255) * (1 - amount)))
  const g = Math.max(0, Math.floor(((num >> 8) & 255) * (1 - amount)))
  const b = Math.max(0, Math.floor((num & 255) * (1 - amount)))
  return `#${[r, g, b].map((c) => c.toString(16).padStart(2, "0")).join("")}`
}

/**
 * Applique les couleurs d'une boutique aux variables CSS du site,
 * pour que chaque boutique ait son propre bandeau/accent sans dupliquer le CSS.
 */
export function applyStoreColors(store) {
  const root = document.documentElement.style
  const primary = store?.primary_color || "#2f4b3c"
  const accent = store?.accent_color || "#e2a13a"

  root.setProperty("--awning", primary)
  root.setProperty("--awning-dark", darken(primary))
  root.setProperty("--marigold", accent)
  root.setProperty("--marigold-dark", darken(accent))
}