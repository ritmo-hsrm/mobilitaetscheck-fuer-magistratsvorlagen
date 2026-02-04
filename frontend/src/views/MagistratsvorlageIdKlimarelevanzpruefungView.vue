<template>
  <div>
    <div class="flex items-center gap-5">
      <BaseSubheading>Klimarelevanzprüfung</BaseSubheading>
      <RouterLink :to="`${route.fullPath}/neu`">
        <Button
          v-tooltip="'Klimarelevanzprüfung hinzufügen'"
          icon="pi pi-plus"
          rounded
          aria-label="Klimarelevanzprüfung hinzufügen"
        />
      </RouterLink>
    </div>
    <KlimarelevanzpruefungListe />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import Button from 'primevue/button'
import KlimarelevanzpruefungListe from '@/components/KlimarelevanzpruefungListe.vue'

const route = useRoute()
</script>

<style></style>
