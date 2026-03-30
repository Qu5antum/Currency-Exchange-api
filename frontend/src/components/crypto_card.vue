<template>
  <div class="card" @click="goToDetail">
    <h3>{{ crypto.symbol }}</h3>
    <p>${{ crypto.price }}</p>
    <p :class="crypto.change >= 0 ? 'green' : 'red'">
      {{ crypto.change }}%
    </p>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const props = defineProps({ crypto: Object });
const router = useRouter();

function goToDetail() {
  router.push(`/crypto/${props.crypto.symbol}`);
}
</script>