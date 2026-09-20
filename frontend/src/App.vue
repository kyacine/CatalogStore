<script setup>
import { onMounted, provide, ref } from "vue"
import FloatingWhatsAppButton from "./components/FloatingWhatsAppButton.vue"
import { fetchStore } from "./lib/api"
import { applyStoreColors } from "./lib/colors"

// Le frontend n'a besoin de connaître que le slug de la boutique à afficher :
// tout le reste (nom, tagline, numéro WhatsApp) vient de l'API.
const storeSlug = import.meta.env.VITE_STORE_SLUG
const store = ref(null)
const storeError = ref(null)

provide("store", store)
provide("storeSlug", storeSlug)
provide("storeError", storeError)

onMounted(async () => {
  if (!storeSlug) {
    storeError.value = "Aucune boutique configurée (VITE_STORE_SLUG manquant dans le fichier .env)."
    return
  }
  try {
    store.value = await fetchStore(storeSlug)
    applyStoreColors(store.value)

    if (store.value.logo_url) {
      const faviconLink = document.getElementById("favicon")
      if (faviconLink) faviconLink.href = store.value.logo_url
    }
  } catch (err) {
    storeError.value = "Boutique introuvable. Vérifiez le slug dans le fichier .env."
  }
})
</script>

<template>
  <router-view />
  <FloatingWhatsAppButton v-if="store?.whatsapp_number" :whatsapp-number="store.whatsapp_number" />
</template>