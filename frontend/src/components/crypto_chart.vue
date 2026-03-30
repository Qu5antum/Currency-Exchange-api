<template>
  <canvas ref="canvas"></canvas>
</template>

<script setup>
import { onMounted, watch, ref } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({ data: Array });
const canvas = ref(null);
let chart;

function render() {
  if (!props.data?.length) return;

  if (chart) chart.destroy();

  chart = new Chart(canvas.value, {
    type: "line",
    data: {
      labels: props.data.map(i => i.date),
      datasets: [{
        data: props.data.map(i => i.price)
      }]
    }
  });
}

onMounted(render);
watch(() => props.data, render);
</script>