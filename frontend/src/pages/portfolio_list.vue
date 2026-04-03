<template>
  <div class="page">

    <!-- Loading -->
    <div v-if="loading" class="state-center">
      <div class="spinner"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-center">
      <p class="error-message">{{ error }}</p>
      <button class="retry-btn" @click="load">Retry</button>
    </div>

    <!-- Content -->
    <template v-else>
      <div class="container">

        <!-- Header -->
        <div class="header">
          <div>
            <h1 class="page-title">My Portfolios</h1>
            <p class="page-sub">{{ portfolios.length }} portfolio{{ portfolios.length !== 1 ? 's' : '' }}</p>
          </div>
          <button class="create-btn" @click="showModal = true">
            <span class="plus">+</span> New Portfolio
          </button>
        </div>

        <!-- Empty state -->
        <div v-if="!portfolios.length" class="empty-state">
          <p class="empty-icon">₿</p>
          <p class="empty-title">No portfolios yet</p>
          <p class="empty-sub">Create your first portfolio to start tracking crypto</p>
          <button class="create-btn" @click="showModal = true">+ New Portfolio</button>
        </div>

        <!-- Portfolio cards -->
        <div v-else class="portfolio-grid">
          <div
            v-for="p in portfolios"
            :key="p.id"
            class="portfolio-card"
            @click="router.push(`/portfolio/${p.id}`)"
          >
            <div class="card-top">
              <div>
                <p class="portfolio-name">{{ p.name }}</p>
                <p class="portfolio-date">Created {{ formatDate(p.created_at) }}</p>
              </div>
              <span class="assets-badge">{{ p.assets.length }} asset{{ p.assets.length !== 1 ? 's' : '' }}</span>
            </div>

            <div class="card-bottom">
              <div class="asset-chips">
                <span
                  v-for="a in p.assets.slice(0, 4)"
                  :key="a.id"
                  class="chip"
                >
                  {{ a.symbol ?? '—' }}
                </span>
                <span v-if="p.assets.length > 4" class="chip chip-more">
                  +{{ p.assets.length - 4 }}
                </span>
              </div>
              <span class="arrow">→</span>
            </div>
          </div>
        </div>

      </div>
    </template>

    <!-- Create modal -->
    <Transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">New Portfolio</h2>
            <button class="close-btn" @click="closeModal">✕</button>
          </div>

          <div class="modal-body">
            <label class="field-label">Portfolio name</label>
            <input
              v-model="newName"
              class="field-input"
              placeholder="e.g. Bitcoin portfolio"
              maxlength="64"
              @keydown.enter="create"
              ref="nameInput"
            />
            <p v-if="createError" class="field-error">{{ createError }}</p>
          </div>

          <div class="modal-footer">
            <button class="cancel-btn" @click="closeModal">Cancel</button>
            <button class="confirm-btn" :disabled="creating || !newName.trim()" @click="create">
              <span v-if="creating" class="btn-spinner"/>
              <span v-else>Create</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import { getUserPortfolios, createPortfolio } from '../services/api.js'

const router = useRouter()

const portfolios  = ref([])
const loading     = ref(true)
const error       = ref(null)

const showModal   = ref(false)
const newName     = ref('')
const creating    = ref(false)
const createError = ref(null)
const nameInput   = ref(null)

function getUserId() {
  const token = localStorage.getItem('token')
  if (!token) return null
  try {
    return jwtDecode(token).sub   // поменяй 'sub' на нужное поле если отличается
  } catch {
    return null
  }
}

async function load() {
  loading.value = true
  error.value   = null
  try {
    const userId = getUserId()
    if (!userId) throw new Error('Not authenticated')
    portfolios.value = await getUserPortfolios(userId)
  } catch (e) {
    error.value = e?.message ?? 'Failed to load portfolios'
  } finally {
    loading.value = false
  }
}

async function create() {
  if (!newName.value.trim() || creating.value) return
  creating.value    = true
  createError.value = null
  try {
    const p = await createPortfolio(newName.value.trim())
    portfolios.value.push({ ...p, assets: [] })
    closeModal()
    router.push(`/portfolio/${p.id}`)
  } catch (e) {
    createError.value = e?.message ?? 'Failed to create portfolio'
  } finally {
    creating.value = false
  }
}

async function closeModal() {
  showModal.value   = false
  newName.value     = ''
  createError.value = null
}

watch(showModal, async (val) => {
  if (val) {
    await nextTick()
    nameInput.value?.focus()
  }
})

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', {
    year:  'numeric',
    month: 'short',
    day:   'numeric',
  })
}

onMounted(load)
</script>

<script>
import { watch } from 'vue'
export default { name: 'PortfolioList' }
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #030712;
  color: #fff;
  padding: 2.5rem 1rem;
  font-family: inherit;
}

.container {
  max-width: 48rem;
  margin: 0 auto;
}

/* ── State ── */
.state-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 16rem;
  gap: 1rem;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: #22c55e;
  border-bottom-color: #22c55e;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.error-message { color: #f87171; font-size: 0.875rem; }

.retry-btn {
  padding: 0.375rem 1rem;
  font-size: 0.875rem;
  border: 0.5px solid #374151;
  color: #d1d5db;
  background: transparent;
  border-radius: 0.5rem;
  cursor: pointer;
}
.retry-btn:hover { border-color: #6b7280; color: #fff; }

/* ── Header ── */
.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin: 0 0 0.25rem;
}

.page-sub {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1.125rem;
  font-size: 0.875rem;
  font-weight: 500;
  background: #22c55e;
  color: #030712;
  border: none;
  border-radius: 0.625rem;
  cursor: pointer;
  transition: background 0.15s, transform 0.1s;
}
.create-btn:hover  { background: #16a34a; }
.create-btn:active { transform: scale(0.97); }

.plus { font-size: 1.1rem; line-height: 1; }

/* ── Empty ── */
.empty-state {
  text-align: center;
  padding: 5rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.empty-icon  { font-size: 2.5rem; margin: 0; }
.empty-title { font-size: 1.125rem; font-weight: 600; margin: 0; color: #e5e7eb; }
.empty-sub   { font-size: 0.875rem; color: #6b7280; margin: 0 0 0.5rem; }

/* ── Grid ── */
.portfolio-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.portfolio-card {
  background: #111827;
  border: 0.5px solid #1f2937;
  border-radius: 1rem;
  padding: 1.25rem;
  cursor: pointer;
  transition: border-color 0.15s, transform 0.15s;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.portfolio-card:hover {
  border-color: #374151;
  transform: translateY(-1px);
}

.card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.portfolio-name {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.25rem;
  color: #f9fafb;
}

.portfolio-date {
  font-size: 0.75rem;
  color: #6b7280;
  margin: 0;
}

.assets-badge {
  font-size: 0.6875rem;
  padding: 0.125rem 0.625rem;
  border-radius: 9999px;
  background: #1f2937;
  color: #9ca3af;
  border: 0.5px solid #374151;
  white-space: nowrap;
}

.card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.asset-chips {
  display: flex;
  gap: 0.375rem;
  flex-wrap: wrap;
}

.chip {
  font-size: 0.6875rem;
  font-weight: 600;
  font-family: 'DM Mono', 'Fira Mono', monospace;
  padding: 0.2rem 0.625rem;
  border-radius: 0.375rem;
  background: #1f2937;
  color: #d1d5db;
  border: 0.5px solid #374151;
  letter-spacing: 0.04em;
}

.chip-more {
  color: #6b7280;
  background: transparent;
  border-color: #1f2937;
}

.arrow {
  color: #374151;
  font-size: 1rem;
  transition: color 0.15s, transform 0.15s;
}
.portfolio-card:hover .arrow {
  color: #22c55e;
  transform: translateX(3px);
}

/* ── Modal ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.modal {
  background: #111827;
  border: 0.5px solid #1f2937;
  border-radius: 1.125rem;
  width: 100%;
  max-width: 24rem;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.25rem 0;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #6b7280;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  transition: color 0.15s;
}
.close-btn:hover { color: #fff; }

.modal-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-label {
  font-size: 0.75rem;
  color: #9ca3af;
  letter-spacing: 0.05em;
}

.field-input {
  width: 100%;
  background: #030712;
  border: 0.5px solid #374151;
  border-radius: 0.625rem;
  color: #f9fafb;
  font-size: 0.9375rem;
  padding: 0.75rem 1rem;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}
.field-input::placeholder { color: #374151; }
.field-input:focus { border-color: #22c55e; }

.field-error {
  font-size: 0.75rem;
  color: #f87171;
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 0.625rem;
  padding: 0 1.25rem 1.25rem;
}

.cancel-btn {
  flex: 1;
  padding: 0.625rem;
  font-size: 0.875rem;
  background: transparent;
  border: 0.5px solid #374151;
  color: #9ca3af;
  border-radius: 0.625rem;
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}
.cancel-btn:hover { border-color: #6b7280; color: #fff; }

.confirm-btn {
  flex: 1;
  padding: 0.625rem;
  font-size: 0.875rem;
  font-weight: 600;
  background: #22c55e;
  color: #030712;
  border: none;
  border-radius: 0.625rem;
  cursor: pointer;
  transition: background 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 2.25rem;
}
.confirm-btn:hover:not(:disabled) { background: #16a34a; }
.confirm-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-spinner {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: #030712;
  animation: spin 0.7s linear infinite;
}

/* ── Transition ── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from,  .fade-leave-to      { opacity: 0; }
</style>