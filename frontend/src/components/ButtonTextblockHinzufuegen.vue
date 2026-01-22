<template>
  <div class="relative inline-block max-w-5xl flex flex-nowrap">
    <Button icon="pi pi-plus" aria-label="Textbaustein" label="Textbaustein" :raised="showList" @click="toggleList"  />
    <transition name="fade">
      <div v-if="showList" class="dropdown">
        <div class="flex">
          <InputText
            type="text"
            v-model="searchQuery"
            placeholder="Textbausteine suchen"
            class="w-full"
          />
        </div>
        <ul class="textblocks-list mt-4">
          <li
            v-for="block in filteredTextblocks"
            :key="block.name"
            @click="addTextblock(block)"
            class="textblock-item"
          >
            {{ block.name }}
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import { fetchItems } from '@/composables/crud'

const textblocks = ref([])

onMounted(async () => {
  await fetchTextblocks()
})

const showList = ref(false)
const searchQuery = ref('')

const toggleList = () => {
  showList.value = !showList.value
}

const emit = defineEmits(['textblock-hinzufuegen'])

const addTextblock = (block) => {
  emit('textblock-hinzufuegen', block.name)
}

const fetchTextblocks = async () => {
  textblocks.value = await fetchItems('/einstellungen/textblock')
}

const filteredTextblocks = computed(() => {
  let filteredTextblocks = textblocks.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filteredTextblocks = filteredTextblocks.filter(
      (block) =>
        block.name.toLowerCase().includes(query) ||
        block.tags.some((tag) => tag.name?.toLowerCase().includes(query.toLowerCase()))
    )
  }

  return filteredTextblocks
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  @apply transition-opacity duration-300;
}

.fade-enter-from,
.fade-leave-to {
  @apply opacity-0;
}

.dropdown {
  @apply absolute top-full left-0 mt-2 bg-white border rounded-lg border-gray-300 shadow-xl w-11/12 p-4 z-50;
}

.search-input {
  @apply w-full p-2 border border-gray-300 rounded;
}

.textblocks-list {
  @apply max-h-48 overflow-y-auto mt-2;
}

.textblock-item {
  @apply p-2 cursor-pointer hover:bg-gray-200 hover:rounded-lg;
}
</style>
