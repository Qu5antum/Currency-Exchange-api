<template>
  <div>
    <h1>{{ crypto.symbol }}</h1>
    <p>Price: ${{ crypto.price }}</p>

    <select v-model="period" @change="loadHistory">
      <option value="1d">1 Day</option>
      <option value="7d">7 Days</option>
      <option value="30d">30 Days</option>
    </select>

    <CryptoChart :data="history"/>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { getCrypto, getCryptoHistory } from "../services/api.js";
import CryptoChart from "../components/crypto_chart.vue";

const route = useRoute();
const symbol = route.params.symbol;

const crypto = ref({});
const history = ref([]);
const period = ref("7d");

onMounted(async () => {
  crypto.value = await getCrypto(symbol);
  await loadHistory();
});

async function loadHistory() {
  history.value = await getCryptoHistory(symbol, period.value);
}
</script>