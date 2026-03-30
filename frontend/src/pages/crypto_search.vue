<template>
  <div>
    <input v-model="query" placeholder="Search crypto..." />
    <button @click="search">Search</button>

    <div class="grid">
      <CryptoCard v-for="c in results" :key="c.symbol" :crypto="c"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { searchCrypto } from "../services/api.js";
import CryptoCard from "../components/crypto_card.vue";

const query = ref("");
const results = ref([]);

async function search() {
  results.value = await searchCrypto(query.value);
}
</script>