function formatPrice(price) {
  const value = Number(price)
  if (Number.isNaN(value)) return price
  return value.toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

/**
 * Construit un lien wa.me qui ouvre WhatsApp avec un message pré-rempli
 * décrivant le produit demandé.
 */
export function buildWhatsAppLink(product) {
  const lines = [`Bonjour, je suis intéressé(e) par ce produit :`]

  if (product.price !== null) {
    lines.push(`• ${product.name} - ${formatPrice(product.price)} ${product.currency}`)
  } else {
    lines.push(`• ${product.name} (prix sur demande)`)
  }

  if (product.category?.name) {
    lines.push(`Catégorie : ${product.category.name}`)
  }

  const message = encodeURIComponent(lines.join("\n"))
  return `https://wa.me/${product.whatsapp_number}?text=${message}`
}

/**
 * Lien WhatsApp générique (pas lié à un produit précis), pour le bouton
 * flottant - utile pour une question, ou un produit absent du catalogue.
 */
export function buildGeneralInquiryLink(whatsappNumber) {
  const message = encodeURIComponent(
    "Bonjour, j'ai une question sur vos produits."
  )
  return `https://wa.me/${whatsappNumber}?text=${message}`
}