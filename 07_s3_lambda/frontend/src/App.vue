<script setup lang="ts">
import axios from 'axios'
import { ref } from "vue";

const msg = ref("")

async function fetchData() {
    try {
      const response = await axios.get(import.meta.env.VITE_API_URL)
      msg.value = response.data.msg
    } catch (error) {
      msg.value = "ERROR"
      console.error('データの取得に失敗しました', error)
    }
  }

fetchData()
</script>

<template>
  <h1> Hello, World </h1>
  <p> {{ msg }} </p>
</template>
