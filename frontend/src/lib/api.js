const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api"

async function getJSON(path) {
  const response = await fetch(`${API_URL}${path}`)
  if (!response.ok) {
    throw new Error(`Erreur API (${response.status}) sur ${path}`)
  }
  return response.json()
}

export function fetchStore(storeSlug) {
  return getJSON(`/stores/${storeSlug}/`)
}

export function fetchCategories(storeSlug) {
  return getJSON(`/stores/${storeSlug}/categories/`)
}

export function fetchProducts(storeSlug, { category, search } = {}) {
  const params = new URLSearchParams()
  if (category) params.set("category", category)
  if (search) params.set("search", search)
  const query = params.toString() ? `?${params.toString()}` : ""
  return getJSON(`/stores/${storeSlug}/products/${query}`)
}

export async function fetchNextPage(url) {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`Erreur API (${response.status}) sur ${url}`)
  }
  return response.json()
}

export function fetchProduct(storeSlug, productId) {
  return getJSON(`/stores/${storeSlug}/products/${productId}/`)
}

export function trackProductClick(storeSlug, productId) {
  return fetch(`${API_URL}/stores/${storeSlug}/products/${productId}/track-click/`, {
    method: "POST",
  }).catch(() => {
    // Le suivi est secondaire : s'il échoue, on ne bloque jamais le client
    // qui essaie de contacter la boutique.
  })
}