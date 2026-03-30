<template>
  <div>
    <h1>Crypto Market</h1>

    <h2>Top Gainers</h2>
    <div class="grid">
      <CryptoCard v-for="c in gainers" :key="c.symbol" :crypto="c"/>
    </div>

    <h2>Top Losers</h2>
    <div class="grid">
      <CryptoCard v-for="c in losers" :key="c.symbol" :crypto="c"/>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getTopGainers, getTopLosers } from "../services/api.js";
import CryptoCard from "../components/crypto_card.vue";

const gainers = ref([]);
const losers = ref([]);

onMounted(async () => {
  gainers.value = await getTopGainers(10);
  losers.value = await getTopLosers(10);
});
</script>