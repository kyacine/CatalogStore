<script setup>
import { computed } from "vue"
import { buildGeneralInquiryLink } from "../lib/whatsapp"

const props = defineProps({
  whatsappNumber: { type: String, required: true },
})

const link = computed(() => buildGeneralInquiryLink(props.whatsappNumber))
</script>

<template>

  <a
    :href="link"
    target="_blank"
    rel="noopener"
    class="whatsapp-float"
    aria-label="Nous contacter sur WhatsApp"
  >
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path
        d="M12 2C6.48 2 2 6.48 2 12c0 1.85.5 3.58 1.36 5.07L2 22l5.11-1.34A9.94 9.94 0 0 0 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm5.2 14.2c-.22.62-1.28 1.18-1.77 1.24-.45.06-1.01.08-1.63-.1-.38-.11-.86-.27-1.48-.53-2.6-1.12-4.3-3.74-4.43-3.92-.13-.18-1.06-1.41-1.06-2.69 0-1.28.67-1.9.9-2.16.23-.26.5-.32.67-.32.17 0 .34 0 .49.01.16.01.37-.06.58.44.22.52.74 1.8.8 1.93.06.13.1.29.02.47-.08.18-.13.29-.25.44-.13.16-.27.35-.38.47-.13.13-.26.27-.11.53.15.26.67 1.1 1.43 1.78.98.88 1.81 1.15 2.07 1.28.26.13.41.11.56-.06.15-.18.64-.75.81-1.01.17-.26.34-.21.57-.13.23.09 1.46.69 1.72.82.26.13.43.19.49.3.06.11.06.62-.16 1.24z"
      />
    </svg>
  </a>
</template>