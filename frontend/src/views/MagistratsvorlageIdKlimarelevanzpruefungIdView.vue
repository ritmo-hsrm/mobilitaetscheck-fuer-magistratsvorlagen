<template>
  <div>
    <div class="flex items-center gap-3 mb-5 [&>h1]:m-0">
      <Button icon="pi pi-chevron-left" severity="secondary" @click="router.back()" />
      <BaseHeading>Klimarelevanzprüfung bearbeiten</BaseHeading>
    </div>
    <KlimarelevanzpruefungFormulare />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import KlimarelevanzpruefungFormulare from '@/components/KlimarelevanzpruefungFormulare.vue'

const router = useRouter()
</script>

<style></style>
