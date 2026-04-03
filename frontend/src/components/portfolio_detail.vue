<template>
  <div class="page">

    <div v-if="loading" class="state-center"><div class="spinner"/></div>

    <div v-else-if="error" class="state-center">
      <p class="error-message">{{ error }}</p>
      <button class="retry-btn" @click="load">Retry</button>
    </div>

    <template v-else>
      <div class="container">

        <!-- Header -->
        <div class="header">
          <div class="header-left">
            <button class="back-btn" @click="router.push('/portfolio')">← Portfolios</button>
            <h1 class="page-title">{{ portfolioName }}</h1>
          </div>
          <button class="tx-btn" @click="router.push(`/portfolio/${id}/transactions`)">
            Transactions →
          </button>
        </div>

        <!-- Overview cards -->
        <div class="stats-grid">
          <div class="stat-card">
            <p class="stat-label">Total Value</p>
            <p class="stat-value">${{ formatPrice(overview.total_value) }}</p>
          </div>
          <div class="stat-card">
            <p class="stat-label">Total Profit</p>
            <p class="stat-value" :class="overview.total_profit >= 0 ? 'pos' : 'neg'">
              {{ overview.total_profit >= 0 ? '+' : '' }}${{ formatPrice(Math.abs(overview.total_profit)) }}
            </p>
          </div>
          <div class="stat-card">
            <p class="stat-label">Assets</p>
            <p class="stat-value">{{ overview.assets?.length ?? 0 }}</p>
          </div>
          <div class="stat-card">
            <p class="stat-label">ROI</p>
            <p class="stat-value" :class="roi >= 0 ? 'pos' : 'neg'">
              {{ roi >= 0 ? '+' : '' }}{{ roi.toFixed(2) }}%
            </p>
          </div>
        </div>

        <!-- History chart -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">Portfolio Value</span>
            <div class="period-selector">
              <button
                v-for="p in periods" :key="p.value"
                :class="['period-btn', period === p.value ? 'active' : '']"
                @click="selectPeriod(p.value)"
              >{{ p.label }}</button>
            </div>
          </div>
          <div v-if="historyLoading" class="chart-loading">Loading chart…</div>
          <PortfolioChart v-else :data="history" :trend="chartTrend"/>
        </div>

        <!-- Assets + Distribution -->
        <div class="two-col">

          <div class="card">
            <div class="card-header">
              <span class="card-title">Assets</span>
              <button class="buy-trigger" @click="openBuy">+ Buy</button>
            </div>
            <div class="assets-list">
              <div v-if="!overview.assets?.length" class="empty-small">No assets yet</div>
              <div v-for="a in overview.assets" :key="a.symbol" class="asset-row">
                <div class="asset-left">
                  <span class="asset-symbol">{{ a.symbol }}</span>
                  <span class="asset-amount">{{ a.amount }}</span>
                </div>
                <div class="asset-right">
                  <p class="asset-value">${{ formatPrice(a.value) }}</p>
                  <p class="asset-profit" :class="a.profit >= 0 ? 'pos' : 'neg'">
                    {{ a.profit >= 0 ? '+' : '' }}${{ formatPrice(Math.abs(a.profit)) }}
                  </p>
                </div>
                <button class="sell-btn" @click="openSell(a)">Sell</button>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <span class="card-title">Distribution</span>
            </div>
            <div v-if="!distribution.length" class="empty-small">No data</div>
            <template v-else>
              <div class="dist-list">
                <div v-for="d in distribution" :key="d.symbol" class="dist-row">
                  <div class="dist-top">
                    <span class="dist-symbol">{{ d.symbol }}</span>
                    <span class="dist-pct">{{ d.distribution.toFixed(1) }}%</span>
                  </div>
                  <div class="dist-bar-bg">
                    <div
                      class="dist-bar-fill"
                      :style="{ width: d.distribution + '%', background: distColor(d.symbol) }"
                    />
                  </div>
                </div>
              </div>
            </template>
          </div>

        </div>
      </div>
    </template>

    <!-- Buy Modal -->
    <Transition name="fade">
      <div v-if="showBuyModal" class="modal-overlay" @click.self="showBuyModal = false">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">Buy Crypto</h2>
            <button class="close-btn" @click="showBuyModal = false">✕</button>
          </div>
          <div class="modal-body">
            <label class="field-label">Symbol</label>
            <input
              v-model="tradeSymbol"
              class="field-input"
              placeholder="BTC"
              @input="tradeSymbol = tradeSymbol.toUpperCase()"
            />
            <label class="field-label">Amount</label>
            <input v-model="tradeAmount" class="field-input" type="number" min="0" step="any" placeholder="0.00" />
            <label class="field-label">Price <span class="field-hint">(per coin, USD)</span></label>
            <input v-model="tradePrice" class="field-input" type="number" min="0" step="any" placeholder="0.00" />
            <p v-if="tradeError" class="field-error">{{ tradeError }}</p>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="showBuyModal = false">Cancel</button>
            <button
              class="confirm-btn confirm-buy"
              :disabled="trading || !tradeSymbol.trim() || !tradeAmount || !tradePrice"
              @click="executeBuy"
            >
              <span v-if="trading" class="btn-spinner"/>
              <span v-else>Buy</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Sell Modal -->
    <Transition name="fade">
      <div v-if="showSellModal" class="modal-overlay" @click.self="showSellModal = false">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">Sell {{ tradeSymbol }}</h2>
            <button class="close-btn" @click="showSellModal = false">✕</button>
          </div>
          <div class="modal-body">
            <label class="field-label">Amount <span class="field-hint">(max {{ maxSell }})</span></label>
            <input v-model="tradeAmount" class="field-input" type="number" min="0" :max="maxSell" step="any" placeholder="0.00" />
            <label class="field-label">Price <span class="field-hint">current ${{ formatPrice(tradePrice) }}</span></label>
            <input v-model="tradePrice" class="field-input" type="number" min="0" step="any" placeholder="0.00" />
            <p v-if="tradeError" class="field-error">{{ tradeError }}</p>
          </div>
          <div class="modal-footer">
            <button class="cancel-btn" @click="showSellModal = false">Cancel</button>
            <button
              class="confirm-btn confirm-sell"
              :disabled="trading || !tradeAmount || !tradePrice"
              @click="executeSell"
            >
              <span v-if="trading" class="btn-spinner"/>
              <span v-else>Sell</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  getPortfolioOverview,
  getPortfolioDistribution,
  getPortfolioHistory,
  getUserPortfolios,
  buyCrypto,
  sellCrypto,
} from '../services/api.js'
import PortfolioChart from '../components/portfolio_chart.vue'

const router = useRouter()
const route  = useRoute()
const id     = route.params.id

const portfolioName  = ref('Portfolio')
const overview       = ref({ total_value: 0, total_profit: 0, assets: [] })
const distribution   = ref([])
const history        = ref([])
const loading        = ref(true)
const historyLoading = ref(false)
const error          = ref(null)
const period         = ref('7')

const showBuyModal  = ref(false)
const showSellModal = ref(false)
const tradeSymbol   = ref('')
const tradeAmount   = ref('')
const tradePrice    = ref('')   
const tradeError    = ref(null)
const trading       = ref(false)
const maxSell       = ref(0)

const periods = [
  { label: '1D',  value: '1'  },
  { label: '7D',  value: '7'  },
  { label: '30D', value: '30' },
]

const roi = computed(() => {
  const cost = (overview.value.total_value ?? 0) - (overview.value.total_profit ?? 0)
  if (!cost) return 0
  return (overview.value.total_profit / cost) * 100
})

const chartTrend = computed(() => {
  if (history.value.length < 2) return 'up'
  const first = history.value[0]['value: ']
  const last  = history.value.at(-1)['value: ']
  return last >= first ? 'up' : 'down'
})

const COLORS = ['#22c55e', '#3b82f6', '#f59e0b', '#a855f7', '#ef4444', '#06b6d4']
const colorMap = {}
function distColor(symbol) {
  if (!colorMap[symbol]) colorMap[symbol] = COLORS[Object.keys(colorMap).length % COLORS.length]
  return colorMap[symbol]
}

async function loadHistory() {
  historyLoading.value = true
  try { history.value = await getPortfolioHistory(id, period.value) }
  finally { historyLoading.value = false }
}

async function selectPeriod(val) {
  period.value = val
  await loadHistory()
}

async function load() {
  loading.value = true
  error.value   = null
  try {
    const [ov, dist] = await Promise.all([
      getPortfolioOverview(id),
      getPortfolioDistribution(id),
      loadHistory(),
    ])
    overview.value     = ov
    distribution.value = dist
    try {
      const token = localStorage.getItem('token')
      if (token) {
        const { jwtDecode } = await import('jwt-decode')
        const userId = jwtDecode(token).sub
        const list   = await getUserPortfolios(userId)
        const found  = list.find(p => String(p.id) === String(id))
        if (found) portfolioName.value = found.name
      }
    } catch {}
  } catch (e) {
    error.value = e?.message ?? 'Failed to load portfolio'
  } finally {
    loading.value = false
  }
}

// ── Trade ─────────────────────────────────────────────────────────────────────

function openBuy() {
  tradeSymbol.value  = ''
  tradeAmount.value  = ''
  tradePrice.value   = ''
  tradeError.value   = null
  showBuyModal.value = true
}

function openSell(asset) {
  tradeSymbol.value   = asset.symbol
  tradeAmount.value   = ''
  tradePrice.value    = asset.current_price  // подставляем текущую цену из overview
  tradeError.value    = null
  maxSell.value       = asset.amount
  showSellModal.value = true
}

async function executeBuy() {
  trading.value    = true
  tradeError.value = null
  try {
    await buyCrypto(id, {
      symbol: tradeSymbol.value.trim().toUpperCase(),
      amount: Number(tradeAmount.value),
      price:  Number(tradePrice.value),
    })
    showBuyModal.value = false
    await load()
  } catch (e) {
    tradeError.value = e?.message ?? 'Buy failed'
  } finally {
    trading.value = false
  }
}

async function executeSell() {
  trading.value    = true
  tradeError.value = null
  try {
    await sellCrypto(id, {
      symbol: tradeSymbol.value,
      amount: Number(tradeAmount.value),
      price:  Number(tradePrice.value),
    })
    showSellModal.value = false
    await load()
  } catch (e) {
    tradeError.value = e?.message ?? 'Sell failed'
  } finally {
    trading.value = false
  }
}

function formatPrice(val) {
  if (!val && val !== 0) return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

onMounted(load)
</script>

<style scoped>
.page { min-height: 100vh; background: #030712; color: #fff; padding: 2.5rem 1rem; font-family: inherit; }
.container { max-width: 52rem; margin: 0 auto; }

.state-center { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 16rem; gap: 1rem; }
.spinner { width: 2rem; height: 2rem; border-radius: 50%; border: 2px solid transparent; border-top-color: #22c55e; border-bottom-color: #22c55e; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-message { color: #f87171; font-size: 0.875rem; }
.retry-btn { padding: 0.375rem 1rem; font-size: 0.875rem; border: 0.5px solid #374151; color: #d1d5db; background: transparent; border-radius: 0.5rem; cursor: pointer; }

.header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1.75rem; }
.header-left { display: flex; flex-direction: column; gap: 0.375rem; }
.back-btn { font-size: 0.75rem; color: #6b7280; background: none; border: none; cursor: pointer; padding: 0; text-align: left; transition: color 0.15s; }
.back-btn:hover { color: #d1d5db; }
.page-title { font-size: 1.75rem; font-weight: 600; letter-spacing: -0.02em; margin: 0; }
.tx-btn { font-size: 0.8125rem; color: #9ca3af; background: none; border: 0.5px solid #374151; border-radius: 0.5rem; padding: 0.375rem 0.875rem; cursor: pointer; transition: color 0.15s, border-color 0.15s; white-space: nowrap; }
.tx-btn:hover { color: #fff; border-color: #6b7280; }

.stats-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 0.625rem; margin-bottom: 1.25rem; }
@media (min-width: 640px) { .stats-grid { grid-template-columns: repeat(4, minmax(0,1fr)); } }
.stat-card { background: #111827; border: 0.5px solid #1f2937; border-radius: 0.75rem; padding: 1rem; }
.stat-label { font-size: 0.6875rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 0.375rem; }
.stat-value { font-size: 1rem; font-weight: 600; margin: 0; }
.pos { color: #4ade80; }
.neg { color: #f87171; }

.card { background: #111827; border: 0.5px solid #1f2937; border-radius: 1rem; padding: 1.25rem; margin-bottom: 1rem; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem; }
.card-title { font-size: 0.6875rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; }

.period-selector { display: flex; gap: 0.25rem; background: rgba(31,41,55,0.7); border-radius: 0.5rem; padding: 0.25rem; }
.period-btn { padding: 0.25rem 0.75rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 500; border: none; background: transparent; color: #6b7280; cursor: pointer; transition: background 0.15s, color 0.15s; }
.period-btn.active { background: #1f2937; color: #fff; border: 0.5px solid #374151; }
.chart-loading { height: 10rem; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; color: #4b5563; letter-spacing: 0.05em; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

.two-col { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 640px) { .two-col { grid-template-columns: 1fr 1fr; } }

.buy-trigger { font-size: 0.75rem; font-weight: 600; background: rgba(34,197,94,0.1); color: #4ade80; border: 0.5px solid rgba(74,222,128,0.2); border-radius: 0.375rem; padding: 0.25rem 0.75rem; cursor: pointer; transition: background 0.15s; }
.buy-trigger:hover { background: rgba(34,197,94,0.18); }
.empty-small { font-size: 0.8125rem; color: #4b5563; text-align: center; padding: 1.5rem 0; }
.assets-list { display: flex; flex-direction: column; gap: 0.5rem; }
.asset-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: #0d1117; border: 0.5px solid #1f2937; border-radius: 0.625rem; }
.asset-left { display: flex; flex-direction: column; gap: 0.125rem; flex: 1; }
.asset-symbol { font-size: 0.875rem; font-weight: 600; font-family: 'DM Mono', monospace; color: #f9fafb; }
.asset-amount { font-size: 0.75rem; color: #6b7280; font-family: 'DM Mono', monospace; }
.asset-right { text-align: right; }
.asset-value { font-size: 0.875rem; font-weight: 500; margin: 0 0 0.125rem; }
.asset-profit { font-size: 0.75rem; margin: 0; }
.sell-btn { font-size: 0.6875rem; font-weight: 600; background: rgba(239,68,68,0.08); color: #f87171; border: 0.5px solid rgba(248,113,113,0.2); border-radius: 0.375rem; padding: 0.25rem 0.625rem; cursor: pointer; transition: background 0.15s; white-space: nowrap; }
.sell-btn:hover { background: rgba(239,68,68,0.15); }

.dist-list { display: flex; flex-direction: column; gap: 1rem; }
.dist-row { display: flex; flex-direction: column; gap: 0.375rem; }
.dist-top { display: flex; justify-content: space-between; align-items: center; }
.dist-symbol { font-size: 0.8125rem; font-weight: 600; font-family: 'DM Mono', monospace; }
.dist-pct { font-size: 0.8125rem; color: #9ca3af; font-family: 'DM Mono', monospace; }
.dist-bar-bg { height: 4px; background: #1f2937; border-radius: 2px; overflow: hidden; }
.dist-bar-fill { height: 100%; border-radius: 2px; transition: width 0.6s cubic-bezier(0.4,0,0.2,1); }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 50; padding: 1rem; }
.modal { background: #111827; border: 0.5px solid #1f2937; border-radius: 1.125rem; width: 100%; max-width: 22rem; overflow: hidden; }
.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 1.25rem 0; }
.modal-title { font-size: 1.125rem; font-weight: 600; margin: 0; }
.close-btn { background: none; border: none; color: #6b7280; font-size: 0.875rem; cursor: pointer; padding: 0.25rem; transition: color 0.15s; }
.close-btn:hover { color: #fff; }
.modal-body { padding: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem; }
.field-label { font-size: 0.75rem; color: #9ca3af; letter-spacing: 0.05em; }
.field-hint { color: #6b7280; font-weight: 400; font-size: 0.7rem; }
.field-input { width: 100%; background: #030712; border: 0.5px solid #374151; border-radius: 0.625rem; color: #f9fafb; font-size: 0.9375rem; padding: 0.75rem 1rem; outline: none; transition: border-color 0.15s; box-sizing: border-box; }
.field-input::placeholder { color: #374151; }
.field-input:focus { border-color: #22c55e; }
.field-error { font-size: 0.75rem; color: #f87171; margin: 0; }
.modal-footer { display: flex; gap: 0.625rem; padding: 0 1.25rem 1.25rem; }
.cancel-btn { flex: 1; padding: 0.625rem; font-size: 0.875rem; background: transparent; border: 0.5px solid #374151; color: #9ca3af; border-radius: 0.625rem; cursor: pointer; transition: border-color 0.15s, color 0.15s; }
.cancel-btn:hover { border-color: #6b7280; color: #fff; }
.confirm-btn { flex: 1; padding: 0.625rem; font-size: 0.875rem; font-weight: 600; border: none; border-radius: 0.625rem; cursor: pointer; display: flex; align-items: center; justify-content: center; min-height: 2.25rem; transition: background 0.15s; }
.confirm-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.confirm-buy  { background: #22c55e; color: #030712; }
.confirm-buy:hover:not(:disabled)  { background: #16a34a; }
.confirm-sell { background: #ef4444; color: #fff; }
.confirm-sell:hover:not(:disabled) { background: #dc2626; }
.btn-spinner { width: 1rem; height: 1rem; border-radius: 50%; border: 2px solid transparent; border-top-color: currentColor; animation: spin 0.7s linear infinite; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }
</style>