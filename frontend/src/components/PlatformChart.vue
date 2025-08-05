<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Platform Performance</h2>
    <div class="space-y-4">
      <select v-model="chartType" class="w-full p-2 border rounded">
        <option value="platform">By Platform</option>
        <option value="creative_type">By Creative Type</option>
        <option value="marketing_goal">By Marketing Goal</option>
      </select>
      <canvas id="platformChart"></canvas>
    </div>
  </div>
</template>

<script>
import { useAdStore } from '../store'
import Chart from 'chart.js/auto'

export default {
  data() {
    return {
      chartType: 'platform'
    }
  },
  async mounted() {
    await this.updateChart()
  },
  watch: {
    chartType() {
      this.updateChart()
    }
  },
  methods: {
    async updateChart() {
      const store = useAdStore()
      await store.fetchPerformance()
      const ctx = document.getElementById('platformChart').getContext('2d')
      const dataMap = {
        platform: store.metrics.platform_performance,
        creative_type: store.metrics.creative_type_performance,
        marketing_goal: store.metrics.goal_performance
      }
      const data = dataMap[this.chartType] || { roi: {}, ctr: {} }
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(data.roi || {}),
          datasets: [
            {
              label: 'ROI',
              data: Object.values(data.roi || {}),
              backgroundColor: '#FF6384'
            },
            {
              label: 'CTR',
              data: Object.values(data.ctr || {}),
              backgroundColor: '#36A2EB'
            }
          ]
        },
        options: {
          scales: {
            y: { beginAtZero: true }
          }
        }
      })
    }
  }
}
</script>