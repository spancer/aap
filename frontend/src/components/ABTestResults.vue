<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">A/B Test Results</h2>
    <div class="space-y-4">
      <input v-model="abTestId" type="text" placeholder="A/B Test ID" class="w-full p-2 border rounded">
      <button @click="fetchResults" class="bg-blue-600 text-white p-2 rounded">Fetch Results</button>
      <table class="w-full border">
        <thead>
          <tr class="bg-gray-200">
            <th class="p-2">Creative ID</th>
            <th class="p-2">Impressions</th>
            <th class="p-2">Clicks</th>
            <th class="p-2">CTR</th>
            <th class="p-2">Conversions</th>
            <th class="p-2">CVR</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in abTestResults" :key="result.creative_id">
            <td class="p-2">{{ result.creative_id }}</td>
            <td class="p-2">{{ result.impressions }}</td>
            <td class="p-2">{{ result.clicks }}</td>
            <td class="p-2">{{ (result.ctr * 100).toFixed(2) }}%</td>
            <td class="p-2">{{ result.conversions }}</td>
            <td class="p-2">{{ (result.cvr * 100).toFixed(2) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { useAdStore } from '../store'

export default {
  data() {
    return {
      abTestId: ''
    }
  },
  computed: {
    abTestResults() {
      return useAdStore().abTestResults
    }
  },
  methods: {
    async fetchResults() {
      const store = useAdStore()
      try {
        await store.fetchABTestResults(this.abTestId)
        alert('A/B test results fetched successfully!')
      } catch (error) {
        alert('Failed to fetch A/B test results: ' + error.message)
      }
    }
  }
}
</script>