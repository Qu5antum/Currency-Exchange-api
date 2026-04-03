<template>
  <div class="page">
    <div class="container">

      <!-- Header -->
      <div class="header">
        <div class="header-left">
          <button class="back-btn" @click="router.push(`/portfolio/${id}`)">← Portfolio</button>
          <h1 class="page-title">Transactions</h1>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters">
        <div class="filter-group">
          <label class="filter-label">Type</label>
          <div class="type-tabs">
            <button
              v-for="t in typeOptions" :key="t.value"
              :class="['type-btn', filters.type === t.value ? 'active-' + t.value : '']"
              @click="setType(t.value)"
            >{{ t.label }}</button>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">Symbol</label>
          <input v-model="filters.symbol" class="filter-input" placeholder="BTC" @input="load" />
        </div>

        <div class="filter-group">
          <label class="filter-label">From</label>
          <input v-model="filters.date_from" class="filter-input" type="datetime-local" @change="load" />
        </div>

        <div class="filter-group">
          <label class="filter-label">To</label>
          <input v-model="filters.date_to" class="filter-input" type="datetime-local" @change="load" />
        </div>

        <button class="reset-btn" @click="resetFilters">Reset</button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="state-center"><div class="spinner"/></div>

      <!-- Error -->
      <div v-else-if="error" class="state-center">
        <p class="error-message">{{ error }}</p>
        <button class="retry-btn" @click="load">Retry</button>
      </div>

      <!-- Empty -->
      <div v-else-if="!transactions.length" class="empty-state">
        <p class="empty-title">No transactions found</p>
        <p class="empty-sub">Try changing the filters</p>
      </div>

      <!-- Table -->
      <div v-else class="tx-list">
        <div class="tx-list-header">
          <span>Type</span>
          <span>Symbol</span>
          <span>Amount</span>
          <span>Price</span>
          <span>Total</span>
          <span>Date</span>
        </div>

        <div
          v-for="tx in paginated" :key="tx.id"
          class="tx-row"
          :class="tx.type === 'BUY' ? 'tx-buy' : 'tx-sell'"
        >
          <span class="tx-type-badge" :class="tx.type === 'BUY' ? 'badge-buy' : 'badge-sell'">
            {{ tx.type }}
          </span>
          <span class="tx-symbol">{{ symbolMap[tx.crypto_currency_id] ?? '#' + tx.crypto_currency_id }}</span>
          <span class="tx-mono">{{ tx.amount }}</span>
          <span class="tx-mono">${{ formatPrice(tx.price) }}</span>
          <span class="tx-mono">${{ formatPrice(tx.amount * tx.price) }}</span>
          <span class="tx-date">{{ formatDate(tx.timestamp) }}</span>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination">
          <button class="page-btn" :disabled="page === 1" @click="page--">←</button>
          <span class="page-info">{{ page }} / {{ totalPages }}</span>
          <button class="page-btn" :disabled="page === totalPages" @click="page++">→</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getTransactions } from '../services/api.js'

const router = useRouter()
const route  = useRoute()
const id     = route.params.id

const transactions = ref([])
const loading      = ref(true)
const error        = ref(null)
const page         = ref(1)
const PER_PAGE     = 15

// symbol lookup — при необходимости подключи getCrypto по id
// пока показываем id, если маппинг не задан
const symbolMap = ref({})

const filters = ref({
  type:      '',
  symbol:    '',
  date_from: '',
  date_to:   '',
})

const typeOptions = [
  { label: 'All',  value: '' },
  { label: 'Buy',  value: 'BUY' },
  { label: 'Sell', value: 'SELL' },
]

const totalPages = computed(() => Math.max(1, Math.ceil(transactions.value.length / PER_PAGE)))

const paginated = computed(() => {
  const start = (page.value - 1) * PER_PAGE
  return transactions.value.slice(start, start + PER_PAGE)
})

function setType(val) {
  filters.value.type = val
  load()
}

function resetFilters() {
  filters.value = { type: '', symbol: '', date_from: '', date_to: '' }
  load()
}

async function load() {
  loading.value = true
  error.value   = null
  page.value    = 1
  try {
    const params = {}
    if (filters.value.type)      params.transaction_type = filters.value.type
    if (filters.value.symbol)    params.symbol           = filters.value.symbol.toUpperCase()
    if (filters.value.date_from) params.date_from        = new Date(filters.value.date_from).toISOString()
    if (filters.value.date_to)   params.date_to          = new Date(filters.value.date_to).toISOString()

    transactions.value = await getTransactions(id, params)
  } catch (e) {
    error.value = e?.message ?? 'Failed to load transactions'
  } finally {
    loading.value = false
  }
}

function formatPrice(val) {
  if (!val && val !== 0) return '—'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatDate(iso) {
  return new Date(iso).toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: false,
  })
}

// сбрасываем страницу при смене фильтров
watch(page, () => window.scrollTo({ top: 0, behavior: 'smooth' }))

onMounted(load)
</script>

<style scoped>
.page {
  min-height: 100vh; background: #030712;
  color: #fff; padding: 2.5rem 1rem; font-family: inherit;
}
.container { max-width: 56rem; margin: 0 auto; }

/* ── Header ── */
.header { margin-bottom: 1.75rem; }
.header-left { display: flex; flex-direction: column; gap: 0.375rem; }
.back-btn {
  font-size: 0.75rem; color: #6b7280; background: none;
  border: none; cursor: pointer; padding: 0; text-align: left;
  transition: color 0.15s; width: fit-content;
}
.back-btn:hover { color: #d1d5db; }
.page-title { font-size: 1.75rem; font-weight: 600; letter-spacing: -0.02em; margin: 0; }

/* ── Filters ── */
.filters {
  display: flex; flex-wrap: wrap; gap: 1rem;
  align-items: flex-end; margin-bottom: 1.5rem;
  padding: 1.125rem; background: #111827;
  border: 0.5px solid #1f2937; border-radius: 0.875rem;
}
.filter-group { display: flex; flex-direction: column; gap: 0.375rem; }
.filter-label { font-size: 0.6875rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; }

.type-tabs { display: flex; gap: 0.25rem; }
.type-btn {
  padding: 0.375rem 0.875rem; font-size: 0.8125rem; font-weight: 500;
  border: 0.5px solid #374151; border-radius: 0.5rem;
  background: transparent; color: #6b7280; cursor: pointer;
  transition: all 0.15s;
}
.type-btn:hover { color: #d1d5db; border-color: #6b7280; }
.active-     { background: #1f2937 !important; color: #fff !important; border-color: #374151 !important; }
.active-BUY  { background: rgba(34,197,94,0.1) !important; color: #4ade80 !important; border-color: rgba(74,222,128,0.25) !important; }
.active-SELL { background: rgba(239,68,68,0.1) !important; color: #f87171 !important; border-color: rgba(248,113,113,0.25) !important; }

.filter-input {
  background: #0d1117; border: 0.5px solid #374151;
  border-radius: 0.5rem; color: #f9fafb; font-size: 0.8125rem;
  padding: 0.5rem 0.75rem; outline: none;
  transition: border-color 0.15s; font-family: inherit;
}
.filter-input:focus { border-color: #22c55e; }
.filter-input[type="datetime-local"] { color-scheme: dark; }

.reset-btn {
  padding: 0.5rem 1rem; font-size: 0.8125rem;
  background: transparent; border: 0.5px solid #374151; color: #6b7280;
  border-radius: 0.5rem; cursor: pointer; transition: all 0.15s;
  align-self: flex-end;
}
.reset-btn:hover { border-color: #6b7280; color: #d1d5db; }

/* ── State ── */
.state-center {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 12rem; gap: 1rem;
}
.spinner {
  width: 2rem; height: 2rem; border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: #22c55e; border-bottom-color: #22c55e;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.error-message { color: #f87171; font-size: 0.875rem; }
.retry-btn {
  padding: 0.375rem 1rem; font-size: 0.875rem;
  border: 0.5px solid #374151; color: #d1d5db;
  background: transparent; border-radius: 0.5rem; cursor: pointer;
}
.empty-state { text-align: center; padding: 4rem 1rem; }
.empty-title { font-size: 1rem; font-weight: 500; color: #6b7280; margin: 0 0 0.5rem; }
.empty-sub { font-size: 0.875rem; color: #374151; margin: 0; }

/* ── Table ── */
.tx-list {
  background: #111827; border: 0.5px solid #1f2937;
  border-radius: 1rem; overflow: hidden;
}
.tx-list-header {
  display: grid;
  grid-template-columns: 70px 80px 1fr 1fr 1fr 1fr;
  gap: 0.5rem; padding: 0.75rem 1.25rem;
  font-size: 0.6875rem; color: #6b7280;
  text-transform: uppercase; letter-spacing: 0.08em;
  border-bottom: 0.5px solid #1f2937;
}
.tx-row {
  display: grid;
  grid-template-columns: 70px 80px 1fr 1fr 1fr 1fr;
  gap: 0.5rem; padding: 0.875rem 1.25rem;
  align-items: center; font-size: 0.875rem;
  border-bottom: 0.5px solid #0d1117;
  transition: background 0.1s;
}
.tx-row:last-of-type { border-bottom: none; }
.tx-row:hover { background: rgba(31,41,55,0.4); }

.tx-type-badge {
  font-size: 0.6875rem; font-weight: 700;
  padding: 0.2rem 0.625rem; border-radius: 0.375rem;
  letter-spacing: 0.06em; text-align: center; width: fit-content;
}
.badge-buy  { background: rgba(34,197,94,0.1);  color: #4ade80; border: 0.5px solid rgba(74,222,128,0.2); }
.badge-sell { background: rgba(239,68,68,0.08); color: #f87171; border: 0.5px solid rgba(248,113,113,0.2); }

.tx-symbol {
  font-size: 0.875rem; font-weight: 600;
  font-family: 'DM Mono', monospace; color: #f9fafb;
}
.tx-mono {
  font-family: 'DM Mono', monospace; color: #d1d5db;
  font-size: 0.8125rem; font-variant-numeric: tabular-nums;
}
.tx-date { font-size: 0.75rem; color: #6b7280; }

/* ── Pagination ── */
.pagination {
  display: flex; align-items: center; justify-content: center;
  gap: 1rem; padding: 1rem;
  border-top: 0.5px solid #1f2937;
}
.page-btn {
  width: 2rem; height: 2rem; border-radius: 0.5rem;
  background: transparent; border: 0.5px solid #374151;
  color: #9ca3af; cursor: pointer; font-size: 0.875rem;
  transition: all 0.15s; display: flex; align-items: center; justify-content: center;
}
.page-btn:hover:not(:disabled) { border-color: #6b7280; color: #fff; }
.page-btn:disabled { opacity: 0.3; cursor: not-allowed; }
.page-info { font-size: 0.8125rem; color: #6b7280; font-family: 'DM Mono', monospace; }
</style>