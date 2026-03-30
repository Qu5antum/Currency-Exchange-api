<template>
  <div class="crypto-list-page">
    <div class="page-header">
      <div class="header-top">
        <h1 class="page-title">Crypto Market</h1>
        <div class="live-dot"><span class="dot-pulse"></span>Live</div>
      </div>

      <div class="controls">
        <div class="search-wrap">
          <span class="search-icon">⌕</span>
          <input
            v-model="search"
            placeholder="Search by name or symbol…"
            class="search-input"
          />
          <button v-if="search" class="clear-btn" @click="search = ''">✕</button>
        </div>

        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            class="tab"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="sort-wrap">
          <label class="sort-label">Sort by</label>
          <select v-model="sortKey" class="sort-select">
            <option value="rank">Rank</option>
            <option value="price">Price</option>
            <option value="change24h">24h Change</option>
            <option value="marketcap">Market Cap</option>
            <option value="volume">Volume 24h</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid">
      <div v-for="n in 10" :key="n" class="skeleton-card"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error-state">
      <span class="error-icon">⚠</span>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="load">Retry</button>
    </div>

    <!-- Empty -->
    <div v-else-if="!displayList.length" class="empty-state">
      <p>No results for <strong>"{{ search }}"</strong></p>
    </div>

    <!-- Grid -->
    <div v-else class="grid">
      <CryptoCard
        v-for="c in displayList"
        :key="c.symbol"
        :crypto="c"
        class="card-animate"
        :style="{ animationDelay: displayList.indexOf(c) * 30 + 'ms' }"
      />
    </div>

    <p v-if="!loading && displayList.length" class="count-label">
      Showing {{ displayList.length }} of {{ allCoins.length }} assets
    </p>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getTopGainers, getTopLosers, getAllCryptos } from '../services/api.js'
import CryptoCard from '../components/crypto_card.vue'

const gainers   = ref([])
const losers    = ref([])
const allCoins  = ref([])
const loading   = ref(true)
const error     = ref(null)
const search    = ref('')
const sortKey   = ref('rank')
const activeTab = ref('all')

const tabs = [
  { key: 'all',     label: 'All' },
  { key: 'gainers', label: '▲ Top Gainers' },
  { key: 'losers',  label: '▼ Top Losers' },
]

function lastSnapshot(coin) {
  const s = coin.snapshots
  return s && s.length ? s[s.length - 1] : {}
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const [g, l, all] = await Promise.all([
      getTopGainers(10),
      getTopLosers(10),
      getAllCryptos(),         
    ])
    gainers.value  = g
    losers.value   = l
    allCoins.value = all
  } catch (e) {
    error.value = e?.message || 'Failed to load market data'
  } finally {
    loading.value = false
  }
}

const sourceList = computed(() => {
  if (activeTab.value === 'gainers') return gainers.value
  if (activeTab.value === 'losers')  return losers.value
  return allCoins.value
})

const displayList = computed(() => {
  let list = sourceList.value

  // Search filter
  const q = search.value.trim().toLowerCase()
  if (q) {
    list = list.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.symbol.toLowerCase().includes(q)
    )
  }

  // Sort
  return [...list].sort((a, b) => {
    const sa = lastSnapshot(a)
    const sb = lastSnapshot(b)
    if (sortKey.value === 'rank')      return (a.cmc_rank || 0) - (b.cmc_rank || 0)
    if (sortKey.value === 'price')     return (sb.price || 0) - (sa.price || 0)
    if (sortKey.value === 'change24h') return (sb.percent_change_24h || 0) - (sa.percent_change_24h || 0)
    if (sortKey.value === 'marketcap') return (sb.market_cap || 0) - (sa.market_cap || 0)
    if (sortKey.value === 'volume')    return (sb.volume_24h || 0) - (sa.volume_24h || 0)
    return 0
  })
})

onMounted(load)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@600;700;800&display=swap');

.crypto-list-page {
  min-height: 100vh;
  background: #08080c;
  padding: 40px 32px 80px;
  font-family: 'Syne', sans-serif;
}

/* ── Header ── */
.page-header {
  margin-bottom: 36px;
}

.header-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.page-title {
  font-size: 32px;
  font-weight: 800;
  color: #f0f0fa;
  letter-spacing: -0.04em;
  line-height: 1;
}

.live-dot {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #34d399;
  font-family: 'DM Mono', monospace;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border: 1px solid rgba(52,211,153,0.2);
  border-radius: 999px;
  background: rgba(52,211,153,0.06);
}

.dot-pulse {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #34d399;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%,100% { opacity: 1; transform: scale(1); }
  50%      { opacity: 0.4; transform: scale(0.8); }
}

/* ── Controls ── */
.controls {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.search-wrap {
  position: relative;
  flex: 1;
  min-width: 200px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: #444458;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: #0d0d12;
  border: 1px solid #1e1e28;
  border-radius: 10px;
  color: #e0e0f0;
  font-size: 14px;
  font-family: 'DM Mono', monospace;
  padding: 10px 36px 10px 38px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input::placeholder { color: #333345; }
.search-input:focus { border-color: #6366f1; }

.clear-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #444458;
  font-size: 12px;
  cursor: pointer;
  padding: 4px;
}

.tabs {
  display: flex;
  gap: 4px;
  background: #0d0d12;
  border: 1px solid #1e1e28;
  border-radius: 10px;
  padding: 4px;
}

.tab {
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'DM Mono', monospace;
  border: none;
  border-radius: 7px;
  background: none;
  color: #555568;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s, color 0.15s;
}

.tab.active {
  background: #1a1a28;
  color: #c8c8e8;
}

.tab:hover:not(.active) { color: #8888a0; }

.sort-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 11px;
  color: #444458;
  font-family: 'DM Mono', monospace;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

.sort-select {
  background: #0d0d12;
  border: 1px solid #1e1e28;
  border-radius: 8px;
  color: #c8c8e8;
  font-size: 12px;
  font-family: 'DM Mono', monospace;
  padding: 7px 10px;
  outline: none;
  cursor: pointer;
  appearance: none;
}

/* ── Grid ── */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* ── Card entrance animation ── */
.card-animate {
  animation: fadeSlide 0.4s ease both;
}

@keyframes fadeSlide {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Skeleton ── */
.skeleton-card {
  height: 190px;
  background: #0d0d12;
  border: 1px solid #1a1a22;
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}

.skeleton-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.03) 50%, transparent 100%);
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  from { transform: translateX(-100%); }
  to   { transform: translateX(100%); }
}

/* ── States ── */
.error-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #555568;
  font-family: 'DM Mono', monospace;
}

.error-icon { font-size: 32px; display: block; margin-bottom: 12px; }
.error-state p { font-size: 14px; margin-bottom: 20px; }

.retry-btn {
  background: none;
  border: 1px solid #3a3a50;
  color: #9090b0;
  font-family: 'DM Mono', monospace;
  font-size: 12px;
  padding: 8px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
}

.retry-btn:hover { border-color: #6366f1; color: #a0a0f0; }

.empty-state strong { color: #7070a0; }

/* ── Footer count ── */
.count-label {
  text-align: center;
  font-size: 11px;
  color: #333345;
  font-family: 'DM Mono', monospace;
  margin-top: 32px;
  letter-spacing: 0.06em;
}
</style>