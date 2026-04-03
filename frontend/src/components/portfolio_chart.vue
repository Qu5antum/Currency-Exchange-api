<template>
  <div class="chart-wrapper">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  data:  { type: Array,  default: () => [] },
  trend: { type: String, default: 'up' },
})

const canvas = ref(null)
let chart = null

function formatLabel(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function render() {
  if (!canvas.value || !props.data?.length) return
  if (chart) { chart.destroy(); chart = null }

  const color     = props.trend === 'up' ? '#22c55e' : '#ef4444'
  const colorFade = props.trend === 'up' ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.10)'

  const ctx = canvas.value.getContext('2d')
  const gradient = ctx.createLinearGradient(0, 0, 0, 200)
  gradient.addColorStop(0, colorFade)
  gradient.addColorStop(1, 'rgba(0,0,0,0)')

  chart = new Chart(canvas.value, {
    type: 'line',
    data: {
      labels:   props.data.map(i => formatLabel(i.timestamp)),
      datasets: [{
        data:                      props.data.map(i => i.value),
        borderColor:               color,
        borderWidth:               1.5,
        backgroundColor:           gradient,
        fill:                      true,
        tension:                   0.4,
        pointRadius:               0,
        pointHitRadius:            16,
        pointHoverRadius:          4,
        pointHoverBackgroundColor: color,
        pointHoverBorderColor:     '#030712',
        pointHoverBorderWidth:     2,
      }],
    },
    options: {
      responsive:          true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#111827',
          borderColor:     'rgba(55,65,81,0.6)',
          borderWidth:     0.5,
          padding:         10,
          titleColor:      '#6b7280',
          titleFont:       { size: 11 },
          bodyColor:       '#fff',
          bodyFont:        { size: 13, weight: '600' },
          displayColors:   false,
          callbacks: {
            label: ctx => '$' + Number(ctx.parsed.y).toLocaleString('en-US', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            }),
          },
        },
      },
      scales: {
        x: {
          grid:   { display: false },
          border: { display: false },
          ticks:  { color: '#374151', font: { size: 10 }, maxTicksLimit: 6, maxRotation: 0 },
        },
        y: {
          position: 'right',
          grid:     { color: 'rgba(31,41,55,0.6)', lineWidth: 0.5 },
          border:   { display: false },
          ticks: {
            color: '#374151',
            font:  { size: 10 },
            callback: val => '$' + Number(val).toLocaleString('en-US', { maximumFractionDigits: 0 }),
          },
        },
      },
    },
  })
}

onMounted(render)
watch(() => props.data,  render, { deep: true })
watch(() => props.trend, render)
onUnmounted(() => { if (chart) chart.destroy() })
</script>

<style scoped>
.chart-wrapper { position: relative; height: 200px; width: 100%; }
</style>
