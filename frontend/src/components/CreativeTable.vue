<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Creative Analysis</h2>
    <table class="w-full border">
      <thead>
        <tr class="bg-gray-200">
          <th class="p-2">Creative ID</th>
          <th class="p-2">Ad ID</th>
          <th class="p-2">Campaign ID</th>
          <th class="p-2">Impressions</th>
          <th class="p-2">Clicks</th>
          <th class="p-2">CTR</th>
          <th class="p-2">Conversions</th>
          <th class="p-2">CVR</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="creative in creatives" :key="creative.creative_id">
          <td class="p-2">{{ creative.creative_id }}</td>
          <td class="p-2">{{ creative.ad_id }}</td>
          <td class="p-2">{{ creative.campaign_id }}</td>
          <td class="p-2">{{ creative.impressions }}</td>
          <td class="p-2">{{ creative.clicks }}</td>
          <td class="p-2">{{ ((creative.clicks / creative.impressions) * 100).toFixed(2) }}%</td>
          <td class="p-2">{{ creative.conversions }}</td>
          <td class="p-2">{{ ((creative.conversions / creative.clicks) * 100).toFixed(2) }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { useAdStore } from '../store'

export default {
  computed: {
    creatives() {
      return useAdStore().creatives
    }
  }
}
</script>