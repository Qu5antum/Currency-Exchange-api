<template>
  <div class="crypto-card" @click="goToDetail">
    <div class="card-header">
      <div class="symbol-block">
        <div class="symbol-badge">{{ crypto.symbol }}</div>
        <div class="rank">#{{ crypto.cmc_rank }}</div>
      </div>
      <div class="change-badge" :class="changeClass">
        <span class="change-arrow">{{ snapshot.percent_change_24h >= 0 ? '▲' : '▼' }}</span>
        {{ Math.abs(snapshot.percent_change_24h).toFixed(2) }}%
      </div>
    </div>

    <div class="name">{{ crypto.name }}</div>

    <div class="price">${{ formatPrice(snapshot.price) }}</div>

    <div class="meta-row">
      <div class="meta-item">
        <span class="meta-label">Market cap</span>
        <span class="meta-value">{{ formatLarge(snapshot.market_cap) }}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Vol 24h</span>
        <span class="meta-value">{{ formatLarge(snapshot.volume_24h) }}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">1h</span>
        <span class="meta-value" :class="snapshot.percent_change_1h >= 0 ? 'pos' : 'neg'">
          {{ snapshot.percent_change_1h >= 0 ? '+' : '' }}{{ snapshot.percent_change_1h.toFixed(2) }}%
        </span>
      </div>
    </div>

    <div class="dominance-bar" v-if="snapshot.market_cap_dominance">
      <div class="dominance-fill" :style="{ width: snapshot.market_cap_dominance + '%' }"></div>
      <span class="dominance-label">{{ snapshot.market_cap_dominance.toFixed(1) }}% dominance</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({ crypto: Object })
const router = useRouter()

const snapshot = computed(() => {
  const snaps = props.crypto.snapshots
  return snaps && snaps.length ? snaps[snaps.length - 1] : {}
})

const changeClass = computed(() =>
  snapshot.value.percent_change_24h >= 0 ? 'change-pos' : 'change-neg'
)

function goToDetail() {
  router.push(`/crypto/${props.crypto.symbol}`)
}

function formatPrice(val) {
  if (!val) return '—'
  if (val >= 1000) return val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  if (val >= 1) return val.toFixed(4)
  return val.toFixed(6)
}

function formatLarge(val) {
  if (!val) return '—'
  if (val >= 1e12) return '$' + (val / 1e12).toFixed(2) + 'T'
  if (val >= 1e9)  return '$' + (val / 1e9).toFixed(2) + 'B'
  if (val >= 1e6)  return '$' + (val / 1e6).toFixed(2) + 'M'
  return '$' + val.toFixed(0)
}
</script>

<style scoped>
.crypto-card {
  background: #0d0d0f;
  border: 1px solid #1e1e24;
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.15s;
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
  overflow: hidden;
}

.crypto-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at top left, rgba(99,102,241,0.04) 0%, transparent 60%);
  pointer-events: none;
}

.crypto-card:hover {
  border-color: #3d3d50;
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.symbol-block {
  display: flex;
  align-items: center;
  gap: 8px;
}

.symbol-badge {
  font-size: 13px;
  font-weight: 700;
  font-family: 'DM Mono', 'Fira Mono', monospace;
  color: #e8e8f0;
  background: #1a1a24;
  border: 1px solid #2a2a38;
  padding: 3px 10px;
  border-radius: 6px;
  letter-spacing: 0.06em;
}

.rank {
  font-size: 11px;
  color: #555568;
  font-family: 'DM Mono', monospace;
}

.change-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 8px;
  font-family: 'DM Mono', monospace;
  letter-spacing: 0.03em;
}

.change-pos {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  border: 1px solid rgba(52, 211, 153, 0.18);
}

.change-neg {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.18);
}

.change-arrow {
  font-size: 9px;
  margin-right: 2px;
}

.name {
  font-size: 15px;
  font-weight: 600;
  color: #c8c8d8;
  letter-spacing: -0.01em;
}

.price {
  font-size: 22px;
  font-weight: 700;
  color: #f0f0fa;
  letter-spacing: -0.03em;
  font-family: 'DM Mono', 'Fira Mono', monospace;
}

.meta-row {
  display: flex;
  gap: 16px;
  padding-top: 8px;
  border-top: 1px solid #1a1a24;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.meta-label {
  font-size: 10px;
  color: #444458;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.meta-value {
  font-size: 12px;
  color: #9090a8;
  font-family: 'DM Mono', monospace;
}

.pos { color: #34d399; }
.neg { color: #f87171; }

.dominance-bar {
  position: relative;
  height: 3px;
  background: #1a1a24;
  border-radius: 2px;
  overflow: visible;
  margin-top: 4px;
}

.dominance-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  border-radius: 2px;
  max-width: 100%;
  transition: width 0.5s ease;
}

.dominance-label {
  position: absolute;
  right: 0;
  top: 6px;
  font-size: 10px;
  color: #444458;
  font-family: 'DM Mono', monospace;
}
</style>