const BASE_URL = "http://127.0.0.1:8000/api/crypto";

function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}

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