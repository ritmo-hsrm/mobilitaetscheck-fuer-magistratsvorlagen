<template>
  <div class="flex items-start justify-center pt-12 px-4">
    <div class="w-full max-w-md">
      <BaseCard class="p-2">
        <div class="text-center mb-8">
          <div class="flex items-center justify-center gap-x-6 h-10 mx-auto mb-4">
            <img
              src="../assets/logos/HSRM_Unterzeile_farbig_RGB.png"
              alt="Logo Hochschule RheinMain"
              class="h-10"
            />
            <img src="../assets/logos/Pimoo-Logo-Primaer.png" alt="Logo pimoo" class="h-10" />
            <img
              src="../assets/logos/oberursel-logo.webp"
              alt="Logo Stadt Oberursel"
              class="h-11"
            />
          </div>
          <h1 class="text-xl font-bold text-gray-800">Registrieren</h1>
          <p class="text-sm text-gray-500">
            {{
              token
                ? 'Sie wurden eingeladen, einen Account zu erstellen.'
                : 'Diese Registrierung ist für Mitglieder der Politik.'
            }}
          </p>
          <Message v-if="!token" severity="info" class="mt-3 text-left">
            Sind Sie von der Verwaltung? Bitte kontaktieren Sie Ihren lokalen Administrator, um eine
            Einladung zu erhalten.
          </Message>
        </div>
        <AuthRegistrierenEinladungFormular v-if="token" />
        <AuthRegistrierenPolitikFormular v-else />
        <div class="border-t border-gray-100 mt-6 pt-4 text-sm">
          <RouterLink class="text-blue-600 hover:underline" :to="{ name: 'anmelden' }">
            Bereits registriert? Hier anmelden
          </RouterLink>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AuthRegistrierenPolitikFormular from '@/components/AuthRegistrierenPolitikFormular.vue'
import AuthRegistrierenEinladungFormular from '@/components/AuthRegistrierenEinladungFormular.vue'
import Message from 'primevue/message'

const route = useRoute()
const token = route.query.token
</script>
