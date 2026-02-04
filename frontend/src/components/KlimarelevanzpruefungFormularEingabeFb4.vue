<template>
  <div>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Stepper value="1">
        <StepList>
          <Step value="1"></Step>
          <Step value="2"></Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <div>
              <p>
                Bitte begründen Sie im Folgenden, inwiefern Ihr Vorhaben eine positive Klimarelevanz
                hat.
              </p>
              <FloatLabel variant="on">
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
            </div>

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
            <div>
              <p>
                Bitte begründen Sie im Folgenden, inwiefern Ihr Vorhaben eine negative Klimarelevanz
                hat.
              </p>
              <FloatLabel variant="on">
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
            </div>
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
import { onMounted } from 'vue'
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

<style></style>
