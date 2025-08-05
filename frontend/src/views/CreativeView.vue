<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Creative Management</h2>
    <CreativeTable />
  </div>
</template>

<script>
import CreativeTable from '../components/CreativeTable.vue'
import { useAdStore } from '../store'

export default {
  components: { CreativeTable },
  async mounted() {
    const store = useAdStore()
    await store.fetchCreatives()
  }
}
</script>