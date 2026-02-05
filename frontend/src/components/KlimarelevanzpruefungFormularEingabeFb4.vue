<template>
  <div>
    <Message v-if="hasErrors" severity="error" class="mb-4">
      <ul class="list-disc list-inside">
        <li v-for="(error, field) in errors" :key="field">{{ error }}</li>
      </ul>
    </Message>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Stepper value="1">
        <StepList>
          <Step value="1"></Step>
          <Step value="2"></Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <ol>
              <li>
                <span>
                  Bitte begründen Sie im Folgenden, inwiefern Ihr Vorhaben eine positive Klimarelevanz
                  hat.
                </span>
                <FloatLabel variant="on" class="w-full">
                  <InputText
                    id="d1q1"
                    v-model="d1q1"
                    aria-describedby="d1q1-help"
                    :invalid="!!errors.d1q1"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="d1q1">Begründung</label>
                </FloatLabel>
              </li>
            </ol>

            <div class="flex pt-6 justify-end">
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('2')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="2">
            <ol>
              <li>
                <span>
                  Bitte begründen Sie im Folgenden, inwiefern Ihr Vorhaben eine negative Klimarelevanz
                  hat.
                </span>
                <FloatLabel variant="on" class="w-full">
                  <InputText
                    id="d2q1"
                    v-model="d2q1"
                    aria-describedby="d2q1-help"
                    :invalid="!!errors.d2q1"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="d2q1">Begründung</label>
                </FloatLabel>
              </li>
            </ol>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('1')"
              />
              <Button label="Speichern" type="submit" icon="pi pi-save" iconPos="right" />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb4'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Stepper from 'primevue/stepper'
import StepList from 'primevue/steplist'
import StepPanels from 'primevue/steppanels'
import Step from 'primevue/step'
import StepPanel from 'primevue/steppanel'
import Message from 'primevue/message'

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: null
  }
})

onMounted(() => {
  if (props.editMode && props.item) {
    setValues(props.item)
  }
})

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema
})

const hasErrors = computed(() => Object.keys(errors.value).length > 0)

const [d1q1] = defineField('d1q1')
const [d2q1] = defineField('d2q1')

const emit = defineEmits(['update-item', 'add-item'])

const onSubmit = handleSubmit(async (values) => {
  if (props.editMode) {
    emit('update-item', { fb: 4, modelId: props.item.id, values })
  } else {
    emit('add-item', { fb: 4, values })
  }
})
</script>

<style scoped>
ol {
  counter-reset: question;
  list-style: none;
  padding-left: 0;
}

ol > li {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  counter-increment: question;
  margin-bottom: 1rem;
}

ol > li > span:first-child::before {
  content: counter(question) '. ';
  font-weight: bold;
}
</style>
