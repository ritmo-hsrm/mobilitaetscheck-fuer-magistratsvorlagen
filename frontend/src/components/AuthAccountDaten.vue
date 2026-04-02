<template>
  <BaseCard>
    <h4 class="text-xl font-bold dark:text-white mb-4">Benutzerangaben</h4>
    <BaseSpinner v-if="isLoading" />
    <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4 max-w-md">
      <!-- Read-only info -->
      <div class="bg-gray-50 rounded-lg p-3 grid grid-cols-1 gap-y-1 text-sm">
        <div class="flex gap-2">
          <span class="text-gray-500 w-24 shrink-0">Kommune</span>
          <span class="font-medium">{{ gemeindeName }}</span>
        </div>
        <div class="flex gap-2">
          <span class="text-gray-500 w-24 shrink-0">Rolle</span>
          <span class="font-medium">{{ rolleName }}</span>
        </div>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <InputText id="vorname" v-model="vorname" class="w-full" :invalid="!!errors.vorname" />
          <label for="vorname">Vorname</label>
        </FloatLabel>
        <small v-if="errors.vorname" class="p-error block">{{ errors.vorname }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <InputText id="nachname" v-model="nachname" class="w-full" :invalid="!!errors.nachname" />
          <label for="nachname">Nachname</label>
        </FloatLabel>
        <small v-if="errors.nachname" class="p-error block">{{ errors.nachname }}</small>
      </div>

      <!-- Email: only for Politik and Admin -->
      <div v-if="canEditEmail" class="field">
        <FloatLabel variant="on">
          <InputText id="email" v-model="email" class="w-full" :invalid="!!errors.email" />
          <label for="email">E-Mail</label>
        </FloatLabel>
        <small v-if="errors.email" class="p-error block">{{ errors.email }}</small>
      </div>

      <!-- Gruppe: for Verwaltung and Politik -->
      <div v-if="canEditGruppe" class="field">
        <FloatLabel variant="on">
          <Select
            id="gruppeId"
            v-model="gruppeId"
            :options="gruppenOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            showClear
          />
          <label for="gruppeId">{{ gruppeLabel }}</label>
        </FloatLabel>
      </div>

      <ButtonSave type="submit" class="w-fit">Speichern</ButtonSave>
    </form>
  </BaseCard>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { schema } from '@/utils/schemas/accountDaten.js'
import { useForm } from 'vee-validate'
import { useToast } from 'primevue/usetoast'
import FloatLabel from 'primevue/floatlabel'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import { apiClient } from '@/services/axios'
import ButtonSave from './ButtonSpeichern.vue'

const isLoading = ref(true)
const gemeindeName = ref('')
const rolleName = ref('')
const userRolleName = ref('')
const gruppen = ref([])

const isVerwaltung = computed(() => userRolleName.value === 'Verwaltung')
const isPolitik = computed(() => userRolleName.value === 'Politik')
const canEditGruppe = computed(() => isVerwaltung.value || isPolitik.value)
const canEditEmail = computed(() => ['Politik', 'Admin'].includes(userRolleName.value))
const gruppeLabel = computed(() => (isPolitik.value ? 'Fraktion / Partei' : 'Gruppe'))
const gruppenOptions = computed(() => [
  { id: null, name: isPolitik.value ? 'Keine Fraktion' : 'Keine Gruppe' },
  ...gruppen.value
])

const { defineField, handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: schema
})

const [email] = defineField('email')
const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [gruppeId] = defineField('gruppeId')

const authStore = useAuthStore()

onMounted(async () => {
  try {
    const [userRes, gemeindenRes, rollenRes] = await Promise.all([
      authStore.getUser(),
      apiClient.get('/option/gemeinde'),
      apiClient.get('/option/user-rolle')
    ])
    setFieldValue('email', userRes.email)
    setFieldValue('vorname', userRes.vorname)
    setFieldValue('nachname', userRes.nachname)
    setFieldValue('gruppeId', userRes.gruppeId ?? null)

    const g = gemeindenRes.data.find((g) => g.id === userRes.gemeindeId)
    const r = rollenRes.data.find((r) => r.id === userRes.rolleId)
    gemeindeName.value = g?.name ?? '–'
    rolleName.value = r?.name ?? '–'
    userRolleName.value = r?.name ?? ''

    if (isVerwaltung.value) {
      const gruppenRes = await apiClient.get('/einstellungen/gruppe')
      gruppen.value = gruppenRes.data.filter((g) => g.rolleId === userRes.rolleId)
    } else if (isPolitik.value) {
      const gruppenRes = await apiClient.get('/public/gruppen', {
        params: { gemeinde_id: userRes.gemeindeId, rolle_id: userRes.rolleId }
      })
      gruppen.value = gruppenRes.data
    }
  } catch {
    /* */
  } finally {
    isLoading.value = false
  }
})

const toast = useToast()

const onSubmit = handleSubmit(async (values) => {
  try {
    const updateData = { vorname: values.vorname, nachname: values.nachname }
    if (canEditEmail.value) updateData.email = values.email
    await authStore.updateUser(updateData)

    if (canEditGruppe.value) {
      await apiClient.patch('/users/me/gruppe', { gruppe_id: values.gruppeId ?? null })
    }

    toast.add({ severity: 'success', summary: 'Profil aktualisiert', life: 3000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler beim Aktualisieren', life: 3000 })
  }
})
</script>
