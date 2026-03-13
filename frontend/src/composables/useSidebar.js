import { ref, watch } from 'vue'

const isOpen = ref(true)

// Carica lo stato salvato da localStorage
const savedState = localStorage.getItem('sidebar-open')
if (savedState !== null) {
  isOpen.value = JSON.parse(savedState)
}

// Salva lo stato quando cambia
watch(isOpen, (newValue) => {
  localStorage.setItem('sidebar-open', JSON.stringify(newValue))
})

export function useSidebar() {
  const toggle = () => {
    isOpen.value = !isOpen.value
  }

  return {
    isOpen,
    toggle
  }
}