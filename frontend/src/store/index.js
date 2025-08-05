import { defineStore } from 'pinia'
import axios from 'axios'

export const useAdStore = defineStore('adStore', {
  state: () => ({
    creatives: [],
    metrics: {},
    audience: {},
    adLogs: [],
    budgetAllocations: [],
    abTestResults: []
  }),
  actions: {
    async fetchCreatives(query = 'skincare', limit = 10) {
      try {
        const response = await axios.get(`http://localhost:8000/data/tiktok/videos?query=${query}&limit=${limit}`)
        this.creatives = response.data
      } catch (error) {
        console.error('Error fetching creatives:', error)
      }
    },
    async fetchPerformance() {
      try {
        const response = await axios.post('http://localhost:8000/analysis/analyze', this.creatives)
        this.metrics = response.data
      } catch (error) {
        console.error('Error fetching performance:', error)
      }
    },
    async fetchAudience(data) {
      try {
        const response = await axios.post('http://localhost:8000/audience/analyze', data)
        this.audience = response.data
      } catch (error) {
        console.error('Error fetching audience:', error)
      }
    },
    async createAd(platform, campaign_id, creative) {
      try {
        const response = await axios.post('http://localhost:8000/ads/create', { platform, campaign_id, creative })
        this.adLogs.push(response.data)
        return response.data
      } catch (error) {
        console.error('Error creating ad:', error)
        throw error
      }
    },
    async fetchAdLogs() {
      try {
        const response = await axios.get('http://localhost:8000/ads/track/tiktok/123')
        this.adLogs = [response.data]
      } catch (error) {
        console.error('Error fetching ad logs:', error)
      }
    },
    async allocateBudget(campaigns, total_budget) {
      try {
        const response = await axios.post('http://localhost:8000/ads/allocate_budget', { campaigns, total_budget })
        this.budgetAllocations = response.data
        return response.data
      } catch (error) {
        console.error('Error allocating budget:', error)
        throw error
      }
    },
    async runABTest(platform, campaign_id, prompts, budget_per_variant) {
      try {
        const response = await axios.post('http://localhost:8000/ads/ab_test', { platform, campaign_id, prompts, budget_per_variant })
        this.abTestResults = response.data
        return response.data
      } catch (error) {
        console.error('Error running A/B test:', error)
        throw error
      }
    },
    async fetchABTestResults(ab_test_id) {
      try {
        const response = await axios.get(`http://localhost:8000/ads/ab_test/${ab_test_id}`)
        this.abTestResults = response.data.analysis
        return response.data
      } catch (error) {
        console.error('Error fetching A/B test results:', error)
        throw error
      }
    }
  }
})