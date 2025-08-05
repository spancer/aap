<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Ad Management</h2>
    <AdForm class="mb-8" />
    <BudgetDashboard class="mb-8" />
    <ABTestResults class="mb-8" />
    <AdLogTable />
  </div>
</template>

<script>
import AdForm from '../components/AdForm.vue'
import BudgetDashboard from '../components/BudgetDashboard.vue'
import ABTestResults from '../components/ABTestResults.vue'
import AdLogTable from '../components/AdLogTable.vue'

export default {
  components: { AdForm, BudgetDashboard, ABTestResults, AdLogTable }
}
</script>