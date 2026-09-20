<script setup>
import { computed, inject, onMounted, ref, watch } from "vue"
import { useRoute } from "vue-router"
import StoreHeader from "../components/StoreHeader.vue"
import { fetchProduct } from "../lib/api"
import { buildWhatsAppLink } from "../lib/whatsapp"
import { trackProductClick } from "../lib/api"

const route = useRoute()
const store = inject("store")
const storeSlug = inject("storeSlug")

const product = ref(null)
const loading = ref(true)
const error = ref(null)
const activeImageIndex = ref(0)

const activeImage = computed(() => product.value?.images?.[activeImageIndex.value] || null)
const whatsappLink = computed(() => (product.value ? buildWhatsAppLink(product.value) : "#"))

async function loadProduct() {
  loading.value = true
  error.value = null
  activeImageIndex.value = 0
  try {
    product.value = await fetchProduct(storeSlug, route.params.id)
  } catch (err) {
    error.value = "Ce produit est introuvable ou n'est plus disponible."
  } finally {
    loading.value = false
  }
}

function handleWhatsAppClick() {
  trackProductClick(storeSlug, route.params.id)
}

onMounted(loadProduct)
// Si on navigue d'une fiche produit à une autre (ex: produits liés plus tard),
// on recharge sans devoir démonter/remonter le composant.
watch(() => route.params.id, loadProduct)
</script>

<template>
  <StoreHeader :store="store" />

  <main class="main product-detail">
    <router-link to="/" class="back-link">&larr; Retour au catalogue</router-link>

    <div v-if="loading" class="state-message">Chargement…</div>

    <div v-else-if="error" class="state-message">
      <strong>Oups.</strong>
      {{ error }}
    </div>

    <div v-else-if="product" class="product-detail__layout">
      <div class="product-detail__gallery">
        <div class="product-detail__main-image">
          <img v-if="activeImage" :src="activeImage.url" :alt="product.name" />
          <span v-else class="product-card__placeholder">{{ product.name.charAt(0).toUpperCase() }}</span>
        </div>
        <div v-if="product.images.length > 1" class="product-detail__thumbnails">
          <button
            v-for="(image, index) in product.images"
            :key="image.id"
            class="product-detail__thumb"
            :class="{ 'product-detail__thumb--active': index === activeImageIndex }"
            @click="activeImageIndex = index"
          >
            <img :src="image.url" :alt="`${product.name} photo ${index + 1}`" />
          </button>
        </div>
      </div>

      <div class="product-detail__info">
        <p v-if="product.category" class="product-card__category">{{ product.category.name }}</p>
        <h1 class="product-detail__name">{{ product.name }}</h1>
        <p v-if="product.price !== null" class="product-detail__price">
          {{ Number(product.price).toFixed(2) }} {{ product.currency }}
        </p>
        <p v-else class="product-card__price--on-request">Prix sur demande</p>

        <p v-if="product.description" class="product-detail__description">{{ product.description }}</p>

        <a :href="whatsappLink" target="_blank" rel="noopener" class="whatsapp-button whatsapp-button--large"
                  @click="handleWhatsAppClick">
          <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path
              d="M12 2C6.48 2 2 6.48 2 12c0 1.85.5 3.58 1.36 5.07L2 22l5.11-1.34A9.94 9.94 0 0 0 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm5.2 14.2c-.22.62-1.28 1.18-1.77 1.24-.45.06-1.01.08-1.63-.1-.38-.11-.86-.27-1.48-.53-2.6-1.12-4.3-3.74-4.43-3.92-.13-.18-1.06-1.41-1.06-2.69 0-1.28.67-1.9.9-2.16.23-.26.5-.32.67-.32.17 0 .34 0 .49.01.16.01.37-.06.58.44.22.52.74 1.8.8 1.93.06.13.1.29.02.47-.08.18-.13.29-.25.44-.13.16-.27.35-.38.47-.13.13-.26.27-.11.53.15.26.67 1.1 1.43 1.78.98.88 1.81 1.15 2.07 1.28.26.13.41.11.56-.06.15-.18.64-.75.81-1.01.17-.26.34-.21.57-.13.23.09 1.46.69 1.72.82.26.13.43.19.49.3.06.11.06.62-.16 1.24z"
            />
          </svg>
          Demander via WhatsApp
        </a>
      </div>
    </div>
  </main>
</template>