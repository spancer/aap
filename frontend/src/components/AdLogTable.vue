<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Ad Logs</h2>
    <table class="w-full border">
      <thead>
        <tr class="bg-gray-200">
          <th class="p-2">Platform</th>
          <th class="p-2">Ad ID</th>
          <th class="p-2">Campaign ID</th>
          <th class="p-2">Status</th>
          <th class="p-2">Impressions</th>
          <th class="p-2">Clicks</th>
          <th class="p-2">Conversions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in adLogs" :key="log.ad_id">
          <td class="p-2">{{ log.platform }}</td>
          <td class="p-2">{{ log.ad_id }}</td>
          <td class="p-2">{{ log.campaign_id }}</td>
          <td class="p-2">{{ log.status }}</td>
          <td class="p-2">{{ log.impressions || 0 }}</td>
          <td class="p-2">{{ log.clicks || 0 }}</td>
          <td class="p-2">{{ log.conversions || 0 }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { useAdStore } from '../store'

export default {
  computed: {
    adLogs() {
      return useAdStore().adLogs
    }
  },
  async mounted() {
    const store = useAdStore()
    await store.fetchAdLogs()
  }
}
</script>