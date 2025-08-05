<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Audience Heatmap</h2>
    <canvas id="audienceHeatmap"></canvas>
  </div>
</template>

<script>
import { useAdStore } from '../store'
import Chart from 'chart.js/auto'

export default {
  async mounted() {
    const store = useAdStore()
    await store.fetchAudience(store.creatives)
    const ctx = document.getElementById('audienceHeatmap').getContext('2d')
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(store.audience.sentiment_distribution || {}),
        datasets: [{
          label: 'Sentiment Distribution',
          data: Object.values(store.audience.sentiment_distribution || {}).map(b => b),
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
      }
    })
  }
}
</script>