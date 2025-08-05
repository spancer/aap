<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Performance Analysis</h2>
    <PlatformChart />
  </div>
</template>

<script>
import PlatformChart from '../components/PlatformChart.vue'

export default {
  components: { PlatformChart }
}
</script>