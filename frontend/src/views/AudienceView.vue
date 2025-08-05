<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Audience Insights</h2>
    <AudienceHeatmap />
  </div>
</template>

<script>
import AudienceHeatmap from '../components/AudienceHeatmap.vue'

export default {
  components: { AudienceHeatmap }
}
</script>