<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Budget Allocation</h2>
    <div class="space-y-4">
      <input v-model="totalBudget" type="number" placeholder="Total Budget" class="w-full p-2 border rounded">
      <button @click="allocateBudget" class="bg-blue-600 text-white p-2 rounded">Allocate Budget</button>
      <table class="w-full border">
        <thead>
          <tr class="bg-gray-200">
            <th class="p-2">Platform</th>
            <th class="p-2">Campaign ID</th>
            <th class="p-2">Allocated Budget</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="allocation in budgetAllocations" :key="allocation.campaign_id">
            <td class="p-2">{{ allocation.platform }}</td>
            <td class="p-2">{{ allocation.campaign_id }}</td>
            <td class="p-2">{{ allocation.allocated_budget.toFixed(2) }}</td>
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
      totalBudget: 1000
    }
  },
  computed: {
    budgetAllocations() {
      return useAdStore().budgetAllocations
    }
  },
  methods: {
    async allocateBudget() {
      const store = useAdStore()
      try {
        const campaigns = store.adLogs.map(log => ({
          platform: log.platform,
          campaign_id: log.campaign_id
        }))
        await store.allocateBudget(campaigns, this.totalBudget)
        alert('Budget allocated successfully!')
      } catch (error) {
        alert('Failed to allocate budget: ' + error.message)
      }
    }
  }
}
</script>