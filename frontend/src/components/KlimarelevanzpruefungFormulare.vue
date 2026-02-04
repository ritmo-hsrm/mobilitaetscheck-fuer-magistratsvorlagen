<template>
  <div>
    <ol class="grid grid-cols-[9fr_3fr] gap-2 items-center list-outside list-decimal ms-6">
      <Dialog
        v-model:visible="visibleF1"
        position="top"
        modal
        header="Fragebogen A"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb1
          :editMode="!!klimarelevanzpruefung.fb1Id"
          :item="klimarelevanzpruefung.fb1"
          @add-item="onSubmit"
          @update-item="onUpdate"
        />
      </Dialog>
      <li>
        Es handelt sich um eine <strong>physische Maßnahme oder eine Beschaffung </strong> oder um
        die <strong>konkrete Planung/Konzept derer</strong>.<br />
        <small
          >(z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von Maschinen, Abholzungen /
          Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)</small
        >
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF1 = true"
        :disabled="!klimarelevanzpruefung.f1"
        :severity="klimarelevanzpruefung.fb1Id ? 'success' : undefined"
      />
      <Divider class="col-span-2" />
      <Dialog
        v-model:visible="visibleF2"
        position="top"
        modal
        header="Fragebogen B"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb2
          :editMode="!!klimarelevanzpruefung.fb2Id"
          :item="klimarelevanzpruefung.fb2"
          @add-item="onSubmit"
          @update-item="onUpdate"
        />
      </Dialog>
      <li>
        Es handelt sich um eine Planung / ein Konzept , das<strong>
          indirekt physische Maßnahmen nach sich zieht.</strong
        ><br /><small> (z.B. Bebauungsplan)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF2 = true"
        :disabled="!klimarelevanzpruefung.f2"
        :severity="klimarelevanzpruefung.fb2Id ? 'success' : undefined"
      />

      <Divider class="col-span-2" />
      <Dialog
        v-model:visible="visibleF3"
        position="top"
        modal
        header="Fragebogen C"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb3
          :editMode="!!klimarelevanzpruefung.fb3Id"
          :item="klimarelevanzpruefung.fb3"
          @add-item="onSubmit"
          @update-item="onUpdate"
        />
      </Dialog>
      <li>
        Es handelt sich um eine Planung, ein Konzept, oder ein Vorhaben, die
        <strong
          >das Verhalten der Bevölkerung oder der kommunalen Mitarbeitenden in Bezug auf
          Klimaaspekte beeinflusst.</strong
        ><br />
        <small> (z.B. Klima-Bildungskampagne, Mobilitätsverhalten)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF3 = true"
        :disabled="!klimarelevanzpruefung.f3"
        :severity="klimarelevanzpruefung.fb3Id ? 'success' : undefined"
      />

      <Divider class="col-span-2" />
      <Dialog
        v-model:visible="visibleF4"
        position="top"
        modal
        header="Fragebogen D"
        :style="{ width: '50rem' }"
      >
        <KlimarelevanzpruefungFormularEingabeFb4
          :editMode="!!klimarelevanzpruefung.fb4Id"
          :item="klimarelevanzpruefung.fb4"
          @add-item="onSubmit"
          @update-item="onUpdate"
        />
      </Dialog>
      <li>
        Es handelt sich um ein Vorhaben, das
        <strong>nicht in eine der bisherigen Kategorien passt</strong>, aber dennoch klimawirksam
        ist.<br />
        <small>(z.B. Reisen)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF4 = true"
        :disabled="!klimarelevanzpruefung.f4"
        :severity="klimarelevanzpruefung.fb4Id ? 'success' : undefined"
      />

      <Divider class="col-span-2" />
      <li>
        Es handelt sich um eine Maßnahme, die <strong>in keiner Weise klimawirksam</strong> ist.
        <br />
        <small>
          (z.B. Personaleinstellung, Mitgliedschaft außerhalb von Klimaschutz- /Klimaanpassung,
          Beantwortung von Anfragen, Wahlen etc.)</small
        >
      </li>
      <Button label="Kein Fragebogen" :disabled="true" />
    </ol>
    <div class="mt-20 flex justify-end">
      <Button
        icon="pi pi-download"
        @click="onExport(route.params.klimarelevanzpruefungId)"
        label="PDF-Export"
        size="small"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { createItem, exportItem, fetchItem, updateItem, updateItemSilent } from '@/composables/crud'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Divider from 'primevue/divider'
import KlimarelevanzpruefungFormularEingabeFb1 from './KlimarelevanzpruefungFormularEingabeFb1.vue'
import KlimarelevanzpruefungFormularEingabeFb2 from './KlimarelevanzpruefungFormularEingabeFb2.vue'
import KlimarelevanzpruefungFormularEingabeFb3 from './KlimarelevanzpruefungFormularEingabeFb3.vue'
import KlimarelevanzpruefungFormularEingabeFb4 from './KlimarelevanzpruefungFormularEingabeFb4.vue'

const route = useRoute()

const isLoading = ref(false)
const klimarelevanzpruefung = ref({ f1: false, f2: false, f3: false, f4: false, f5: false })
const visibleF1 = ref(false)
const visibleF2 = ref(false)
const visibleF3 = ref(false)
const visibleF4 = ref(false)

const closeDialogs = () => {
  visibleF1.value = false
  visibleF2.value = false
  visibleF3.value = false
  visibleF4.value = false
}

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  klimarelevanzpruefung.value = await fetchItem(
    `/klimarelevanzpruefung/eingabe/${route.params.klimarelevanzpruefungId}`
  )
}

const onSubmit = async ({ fb, values }) => {
  const response = await createItem({
    model: `klimarelevanzpruefung/eingabe/fb${fb}`,
    values,
    detail: {
      success: `Fragebogen erfolgreich hinzugefügt`,
      error: `Fehler beim Hinzufügen des Fragebogens`
    }
  })
  await updateItemSilent({
    model: 'klimarelevanzpruefung/eingabe',
    modelId: route.params.klimarelevanzpruefungId,
    values: {
      [`f${fb}`]: true,
      [`fb${fb}Id`]: response.id
    }
  })
  klimarelevanzpruefung.value[`f${fb}`] = true
  klimarelevanzpruefung.value[`fb${fb}Id`] = response.id
  klimarelevanzpruefung.value[`fb${fb}`] = response
  closeDialogs()
}

const onUpdate = async ({ fb, modelId, values }) => {
  const response = await updateItem({
    model: `klimarelevanzpruefung/eingabe/fb${fb}`,
    modelId,
    values,
    detail: {
      success: `Fragebogen erfolgreich aktualisiert`,
      error: `Fehler beim Aktualisieren des Fragebogens`
    }
  })
  klimarelevanzpruefung.value[`fb${fb}`] = response
  closeDialogs()
}

const onExport = async (modelId) => {
  await exportItem({
    model: 'klimarelevanzpruefung',
    modelId,
    detail: {
      success: 'Klimarelevanzpruefung erfolgreich exportiert',
      error: 'Fehler beim Exportieren des Mobilitätschecks'
    }
  })
}
</script>

<style></style>
