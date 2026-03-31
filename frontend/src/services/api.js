const BASE_URL = "http://127.0.0.1:8000/api/crypto";
const PORTFOLIO_URL = "http://127.0.0.1:8000/api/portfolio/";

function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}

/* crypto routes from backend side */

export async function getAllCryptos() {
  return fetch(`${BASE_URL}`, {
    headers: getAuthHeaders()
  }).then(r => r.json());
}

export async function getCrypto(symbol) {
  return fetch(`${BASE_URL}/${symbol}`, {
    headers: getAuthHeaders()
  }).then(r => r.json());
}

const PERIOD_TO_DAYS = {
  "1d":  1,
  "7d":  7,
  "30d": 30,
};

export async function getCryptoHistory(symbol, period) {
  const days = PERIOD_TO_DAYS[period];
  return fetch(`${BASE_URL}/${symbol}/history/${days}`, {
    headers: getAuthHeaders()
  }).then(r => r.json());
}

export async function getTopLosers(limit) {
  return fetch(`${BASE_URL}/top_gainers/${limit}`, {
    headers: getAuthHeaders()
  }).then(r => r.json());
}

export async function getTopGainers(limit) {
  return fetch(`${BASE_URL}/top_losers/${limit}`, {
    headers: getAuthHeaders()
  }).then(r => r.json());
}

export async function searchCrypto(name) {
  return fetch(`${BASE_URL}/search/${name}`, {
    headers: getAuthHeaders()
  }).then(r => r.json());
}

/* portfolio endpoints from backend side */

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.detail ?? `HTTP ${res.status}`);
  }
  return res.json();
}
 
export async function createPortfolio(name) {
  return fetch(`${PORTFOLIO_URL}/portfolio/create`, {
    method:  "POST",
    headers: getAuthHeaders(),
    body:    JSON.stringify({ name }),
  }).then(handleResponse);
}
 
export async function buyCrypto(portfolioId, symbol, amount) {
  return fetch(`${PORTFOLIO_URL}/portfolio/${portfolioId}/buy`, {
    method:  "POST",
    headers: getAuthHeaders(),
    body:    JSON.stringify({ symbol, amount }),
  }).then(handleResponse);
}
 
export async function sellCrypto(portfolioId, symbol, amount) {
  return fetch(`${PORTFOLIO_URL}/portfolio/${portfolioId}/sell`, {
    method:  "POST",
    headers: getAuthHeaders(),
    body:    JSON.stringify({ symbol, amount }),
  }).then(handleResponse);
}
 
export async function getPortfolioOverview(portfolioId) {
  return fetch(`${PORTFOLIO_URL}/portfolio/${portfolioId}/overview`, {
    headers: getAuthHeaders(),
  }).then(handleResponse);
}
 
export async function getPortfolioDistribution(portfolioId) {
  return fetch(`${PORTFOLIO_URL}/portfolio/${portfolioId}/distribution`, {
    headers: getAuthHeaders(),
  }).then(handleResponse);
}
 
export async function getPortfolioHistory(portfolioId) {
  return fetch(`${PORTFOLIO_URL}/portfolio/${portfolioId}/history`, {
    headers: getAuthHeaders(),
  }).then(handleResponse);
}
 
export async function getTransactions(portfolioId) {
  return fetch(`${PORTFOLIO_URL}/portfolio/${portfolioId}/transactions`, {
    headers: getAuthHeaders(),
  }).then(handleResponse);
}