<script setup>
defineProps({
  store: { type: Object, default: null },
})
</script>

<template>
  <header class="site-header">
    <div class="site-header__inner">
      <p class="site-header__eyebrow">Catalogue en ligne</p>
      <div class="site-header__row">
        <img
          v-if="store?.logo_url"
          :src="store.logo_url"
          :alt="`Logo ${store.name}`"
          class="site-header__logo"
        />
        <div>
          <h1 class="site-header__title">{{ store?.name || "Chargement…" }}</h1>
          <p class="site-header__subtitle">
            {{ store?.tagline || "Découvrez nos produits et contactez-nous directement sur WhatsApp." }}
          </p>
        </div>
      </div>
      <p v-if="store?.address" class="site-header__address">📍 {{ store.address }}</p>
    </div>
  </header>
</template>