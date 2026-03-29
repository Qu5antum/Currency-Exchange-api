<template>
  <div class="auth-page">
    <h1>Login</h1>
    <form @submit.prevent="loginUser">
      <label>Email:</label>
      <input type="email" v-model="email" required />

      <label>Password:</label>
      <input type="password" v-model="password" required />

      <button type="submit">Login</button>
    </form>

    <p>
      Don't have an account?
      <router-link to="/register">Register</router-link>
    </p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const password = ref("");
const error = ref("");

async function loginUser() {
  error.value = "";
  try {
    const res = await fetch("http://localhost:8000/api/user/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // Сохраняем токен в localStorage
    localStorage.setItem("token", data.access_token);

    // Переходим на главную страницу или дашборд
    window.location.href = "/";
  } catch (err) {
    error.value = err.message;
  }
}
</script>

<style scoped>
.auth-page {
  max-width: 400px;
  margin: 4rem auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #1e88e5;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>