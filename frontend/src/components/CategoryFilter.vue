<script setup>
defineProps({
  categories: { type: Array, required: true },
  activeSlug: { type: String, default: null },
})

const emit = defineEmits(["select"])
</script>

<template>
  <nav class="category-bar" aria-label="Filtrer par catégorie">
    <button
      class="category-chip"
      :class="{ 'category-chip--active': activeSlug === null }"
      @click="emit('select', null)"
    >
      Tout voir
    </button>
    <button
      v-for="category in categories"
      :key="category.id"
      class="category-chip"
      :class="{ 'category-chip--active': activeSlug === category.slug }"
      @click="emit('select', category.slug)"
    >
      {{ category.name }}
    </button>
  </nav>
</template>