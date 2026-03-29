<template>
  <div class="auth-page">
    <h1>Register</h1>
    <form @submit.prevent="registerUser">
      <label>Email:</label>
      <input type="email" v-model="email" required />

      <label>Password:</label>
      <input type="password" v-model="password" required />

      <button type="submit">Register</button>
    </form>

    <p>
      Already have an account?
      <router-link to="/login">Login</router-link>
    </p>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const password = ref("");
const error = ref("");

async function registerUser() {
  error.value = "";
  try {
    const res = await fetch("http://localhost:8000/api/user/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value })
    });

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.detail || "Registration failed");
    }

    alert("Registration successful! Please login.");
    window.location.href = "/login";
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
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>