<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-blue-600 text-white p-4">
      <div class="container mx-auto flex justify-between">
        <h1 class="text-2xl font-bold">Ad Automation Platform</h1>
        <div>
          <router-link to="/creatives" class="mr-4">Creatives</router-link>
          <router-link to="/performance" class="mr-4">Performance</router-link>
          <router-link to="/audience" class="mr-4">Audience</router-link>
          <router-link to="/ads" class="mr-4">Ads</router-link>
        </div>
      </div>
    </nav>
    <div class="container mx-auto p-4">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>