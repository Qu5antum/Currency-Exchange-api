<style scoped>
.page {
  min-height: 100vh;
  background-color: #030712;
  color: #fff;
  padding: 2.5rem 1rem;
  font-family: inherit;
}

/* ── Loading / Error ─────────────────────────── */

.state-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 16rem;
  gap: 1rem;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: #22c55e;
  border-bottom-color: #22c55e;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  color: #f87171;
  font-size: 0.875rem;
}

.retry-btn {
  padding: 0.375rem 1rem;
  font-size: 0.875rem;
  border: 0.5px solid #374151;
  color: #d1d5db;
  background: transparent;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}

.retry-btn:hover {
  border-color: #6b7280;
  color: #fff;
}

/* ── Layout ──────────────────────────────────── */

.container {
  max-width: 48rem;
  margin: 0 auto;
}

/* ── Header ──────────────────────────────────── */

.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.symbol-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.symbol {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0;
}

.rank-badge {
  font-size: 0.6875rem;
  font-weight: 500;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  background: #111827;
  color: #9ca3af;
  border: 0.5px solid #374151;
}

.crypto-name {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.header-right {
  text-align: right;
}

.price {
  font-size: 1.875rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  margin: 0 0 0.5rem;
}

.change-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  border: 0.5px solid;
}

.change-badge.up {
  background: #052e16;
  color: #4ade80;
  border-color: #14532d;
}

.change-badge.down {
  background: #1c0505;
  color: #f87171;
  border-color: #450a0a;
}

.change-badge .muted {
  opacity: 0.5;
  font-weight: 400;
}

/* ── Stats grid ──────────────────────────────── */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.625rem;
  margin-bottom: 1.5rem;
}

@media (min-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.stat-card {
  background: #111827;
  border: 0.5px solid rgba(31, 41, 55, 0.6);
  border-radius: 0.75rem;
  padding: 1rem;
}

.stat-label {
  font-size: 0.6875rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 0.5rem;
}

.stat-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  font-variant-numeric: tabular-nums;
  margin: 0;
}

/* ── Chart card ──────────────────────────────── */

.chart-card {
  background: #111827;
  border: 0.5px solid rgba(31, 41, 55, 0.6);
  border-radius: 1rem;
  padding: 1.25rem;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.chart-title {
  font-size: 0.6875rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.period-selector {
  display: flex;
  gap: 0.25rem;
  background: rgba(31, 41, 55, 0.7);
  border-radius: 0.5rem;
  padding: 0.25rem;
}

.period-btn {
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  border: none;
  background: transparent;
  color: #6b7280;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.period-btn:hover {
  color: #d1d5db;
}

.period-btn.active {
  background: #1f2937;
  color: #fff;
  border: 0.5px solid #374151;
}

.chart-loading {
  height: 12rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: #4b5563;
  letter-spacing: 0.05em;
  animation: pulse 2s cubic-bezier(0.4,0,0.6,1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

/* ── Live indicator ──────────────────────────── */

.live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.live-dot {
  position: relative;
  display: flex;
  height: 0.375rem;
  width: 0.375rem;
}

.live-dot-ping {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  opacity: 0.75;
  animation: ping 1.5s cubic-bezier(0,0,0.2,1) infinite;
}

.live-dot-core {
  position: relative;
  border-radius: 50%;
  height: 0.375rem;
  width: 0.375rem;
}

.live-dot.ok .live-dot-ping { background: #4ade80; }
.live-dot.ok .live-dot-core { background: #22c55e; }
.live-dot.err .live-dot-ping { background: #f87171; }
.live-dot.err .live-dot-core { background: #ef4444; }

@keyframes ping {
  75%, 100% { transform: scale(2); opacity: 0; }
}

.live-text {
  font-size: 0.6875rem;
  color: #4b5563;
}

.live-text span {
  color: #6b7280;
}
</style>

<template>
  <div class="page">

    <!-- Loading -->
    <div v-if="loading" class="state-center">
      <div class="spinner"/>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-center">
      <p class="error-message">{{ error }}</p>
      <button class="retry-btn" @click="init">Retry</button>
    </div>

    <!-- Content -->
    <template v-else>

      <!-- Header -->
      <div class="container header">
        <div class="header-left">
          <div class="symbol-row">
            <h1 class="symbol">{{ crypto.symbol }}</h1>
            <span class="rank-badge">#1</span>
          </div>
          <p class="crypto-name">{{ crypto.name }}</p>
        </div>
        <div class="header-right">
          <p class="price">${{ formatPrice(crypto.price) }}</p>
          <span :class="['change-badge', priceChange >= 0 ? 'up' : 'down']">
            <span>{{ priceChange >= 0 ? '▲' : '▼' }}</span>
            <span>{{ Math.abs(priceChange).toFixed(2) }}%</span>
            <span class="muted">24h</span>
          </span>
        </div>
      </div>

      <!-- Stats -->
      <div class="container stats-grid">
        <div v-for="stat in stats" :key="stat.label" class="stat-card">
          <p class="stat-label">{{ stat.label }}</p>
          <p class="stat-value">{{ stat.value }}</p>
        </div>
      </div>

      <!-- Chart -->
      <div class="container chart-card">
        <div class="chart-header">
          <span class="chart-title">Price history</span>
          <div class="period-selector">
            <button
              v-for="p in periods"
              :key="p.value"
              :class="['period-btn', period === p.value ? 'active' : '']"
              @click="selectPeriod(p.value)"
            >
              {{ p.label }}
            </button>
          </div>
        </div>
        <div v-if="historyLoading" class="chart-loading">Loading chart...</div>
        <CryptoChart v-else :data="history" :trend="chartTrend"/>
      </div>

      <!-- Live indicator -->
      <div class="container live-indicator">
        <div :class="['live-dot', error ? 'err' : 'ok']">
          <span class="live-dot-ping"/>
          <span class="live-dot-core"/>
        </div>
        <p class="live-text">
          Live · updates every 30s · last updated <span>{{ lastUpdated }}</span>
        </p>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { getCrypto, getCryptoHistory } from "../services/api.js";
import CryptoChart from "../components/crypto_chart.vue";

const route = useRoute();
const symbol = route.params.symbol;

const crypto         = ref({});
const history        = ref([]);
const period         = ref("7d");
const loading        = ref(false);
const historyLoading = ref(false);
const error          = ref(null);
const lastUpdated    = ref("—");

let refreshTimer = null;

const periods = [
  { label: "1D", value: "1d"  },
  { label: "7D", value: "7d"  },
  { label: "30D", value: "30d" },
];

const priceChange = computed(() => crypto.value?.price_change_24h ?? 0);

const chartTrend = computed(() => {
  if (history.value.length < 2) return "up";
  return history.value.at(-1).price >= history.value[0].price ? "up" : "down";
});

const latest = computed(() => history.value.at(-1) ?? {});

const stats = computed(() => [
  { label: "Market Cap",  value: formatLarge(latest.value?.market_cap)   },
  { label: "Volume 24h",  value: formatLarge(latest.value?.volume_24h)   },
  { label: "Change 1h",   value: `${(latest.value?.percent_change_1h ?? 0).toFixed(2)}%` },
  { label: "Dominance",   value: `${(latest.value?.market_cap_dominance ?? 0).toFixed(2)}%` },
]);

function formatPrice(value) {
  if (!value) return "—";
  return Number(value).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatLarge(value) {
  if (!value) return "—";
  if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
  return `$${value.toLocaleString()}`;
}

function updateTimestamp() {
  lastUpdated.value = new Date().toLocaleTimeString();
}

async function fetchCrypto() {
  crypto.value = await getCrypto(symbol);
  updateTimestamp();
}

async function loadHistory() {
  historyLoading.value = true;
  try {
    history.value = await getCryptoHistory(symbol, period.value);
  } finally {
    historyLoading.value = false;
  }
}

async function selectPeriod(value) {
  period.value = value;
  await loadHistory();
}

async function init() {
  loading.value = true;
  error.value   = null;
  try {
    await Promise.all([fetchCrypto(), loadHistory()]);
  } catch (e) {
    error.value = e?.message ?? "Failed to load data";
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  init();
  refreshTimer = setInterval(fetchCrypto, 30_000);
});

onUnmounted(() => {
  clearInterval(refreshTimer);
});
</script>