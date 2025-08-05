<template>
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Create Ad or A/B Test</h2>
    <div class="space-y-4">
      <select v-model="form.mode" class="w-full p-2 border rounded">
        <option value="single">Single Ad</option>
        <option value="ab_test">A/B Test</option>
      </select>
      <select v-model="form.platform" class="w-full p-2 border rounded">
        <option value="tiktok">TikTok</option>
        <option value="facebook">Facebook</option>
        <option value="google">Google Ads</option>
      </select>
      <input v-model="form.campaign_id" type="text" placeholder="Campaign ID" class="w-full p-2 border rounded">
      <div v-if="form.mode === 'single'">
        <input v-model="form.creative.name" type="text" placeholder="Ad Name" class="w-full p-2 border rounded">
        <input v-model="form.creative.video_id" type="text" placeholder="Video ID" class="w-full p-2 border rounded">
        <input v-model="form.creative.landing_page" type="text" placeholder="Landing Page" class="w-full p-2 border rounded">
      </div>
      <div v-else>
        <textarea v-model="form.prompts" placeholder="Enter prompts for A/B test (one per line)" class="w-full p-2 border rounded"></textarea>
        <input v-model="form.budget_per_variant" type="number" placeholder="Budget per Variant" class="w-full p-2 border rounded">
      </div>
      <button @click="submitForm" class="bg-blue-600 text-white p-2 rounded">Submit</button>
    </div>
  </div>
</template>

<script>
import { useAdStore } from '../store'

export default {
  data() {
    return {
      form: {
        mode: 'single',
        platform: 'tiktok',
        campaign_id: '',
        creative: {
          name: '',
          video_id: '',
          landing_page: ''
        },
        prompts: '',
        budget_per_variant: 100
      }
    }
  },
  methods: {
    async submitForm() {
      const store = useAdStore()
      try {
        if (this.form.mode === 'single') {
          await store.createAd(this.form.platform, this.form.campaign_id, this.form.creative)
          alert('Ad created successfully!')
        } else {
          const prompts = this.form.prompts.split('\n').filter(p => p.trim())
          await store.runABTest(this.form.platform, this.form.campaign_id, prompts, this.form.budget_per_variant)
          alert('A/B test created successfully!')
        }
        this.form = {
          mode: 'single',
          platform: 'tiktok',
          campaign_id: '',
          creative: { name: '', video_id: '', landing_page: '' },
          prompts: '',
          budget_per_variant: 100
        }
      } catch (error) {
        alert('Failed to submit: ' + error.message)
      }
    }
  }
}
</script>