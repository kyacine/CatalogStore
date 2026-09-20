<script setup>
import { inject, onMounted, onUnmounted, ref } from "vue"
import CategoryFilter from "../components/CategoryFilter.vue"
import ProductCard from "../components/ProductCard.vue"
import StoreHeader from "../components/StoreHeader.vue"
import { fetchCategories, fetchProducts,fetchNextPage } from "../lib/api"

const store = inject("store")
const storeSlug = inject("storeSlug")
const storeError = inject("storeError")

const categories = ref([])
const products = ref([])
const nextPageUrl = ref(null)
const activeSlug = ref(null)
const searchQuery = ref("")
const loading = ref(true)
const loadingMore = ref(false)
const error = ref(null)

let debounceTimer = null

async function loadProducts() {
  loading.value = true
  error.value = null
  try {
    const data = await fetchProducts(storeSlug, {
      category: activeSlug.value,
      search: searchQuery.value.trim(),
    })
    products.value = data.results
    nextPageUrl.value = data.next
  } catch (err) {
    error.value = "Impossible de charger les produits pour le moment."
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  if (!nextPageUrl.value) return
  loadingMore.value = true
  try {
    const data = await fetchNextPage(nextPageUrl.value)
    products.value = [...products.value, ...data.results]
    nextPageUrl.value = data.next
  } catch (err) {
    // Un échec sur "charger plus" n'efface pas ce qui est déjà affiché.
  } finally {
    loadingMore.value = false
  }
}

async function selectCategory(slug) {
  activeSlug.value = slug
  await loadProducts()
}

function onSearchInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(loadProducts, 350)
}

onUnmounted(() => clearTimeout(debounceTimer))

onMounted(async () => {
  try {
    categories.value = await fetchCategories(storeSlug)
  } catch (err) {
    // Les catégories sont secondaires : on continue même si ça échoue.
  }
  await loadProducts()
})
</script>

<template>
  <StoreHeader :store="store" />

  <div v-if="storeError" class="state-message">
    <strong>Oups.</strong>
    {{ storeError }}
  </div>

  <template v-else>
    <div class="search-bar">
      <input
        v-model="searchQuery"
        @input="onSearchInput"
        type="search"
        class="search-input"
        placeholder="Rechercher un produit…"
        aria-label="Rechercher un produit"
      />
    </div>

    <CategoryFilter
      v-if="categories.length"
      :categories="categories"
      :active-slug="activeSlug"
      @select="selectCategory"
    />

    <main class="main">
      <div v-if="loading" class="product-grid" aria-busy="true">
        <div class="skeleton-card" v-for="n in 8" :key="n">
          <div class="skeleton-card__image"></div>
          <div class="skeleton-card__body">
            <div class="skeleton-line" style="width: 60%"></div>
            <div class="skeleton-line" style="width: 85%"></div>
            <div class="skeleton-line" style="width: 40%"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="state-message">
        <strong>Oups.</strong>
        {{ error }}
      </div>

      <div v-else-if="products.length === 0" class="state-message">
        <strong>Aucun produit ici pour l'instant.</strong>
        Essayez une autre recherche, ou ajoutez des produits depuis l'espace d'administration.
      </div>

      <div v-else class="product-grid">
        <ProductCard v-for="product in products" :key="product.id" :product="product" />
      </div>
      <div v-if="nextPageUrl" class="load-more">
        <button class="load-more-button" :disabled="loadingMore" @click="loadMore">
          {{ loadingMore ? "Chargement…" : "Charger plus de produits" }}
        </button>
      </div>
    </main>

    <footer class="site-footer">
      © {{ new Date().getFullYear() }} {{ store?.name }}
      <span v-if="store?.address"> · 📍 {{ store.address }}</span>
    </footer>
  </template>
</template>