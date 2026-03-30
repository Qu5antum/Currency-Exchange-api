<template>
  <div class="auth-page">
    <h1>Login</h1>
    <form @submit.prevent="loginUser">
      <label>Username:</label>
      <input type="text" v-model="username" required />

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

const username = ref(""); 
const password = ref("");
const error = ref("");

async function loginUser() {
  error.value = "";
  try {
    const formData = new URLSearchParams();
    formData.append("username", username.value);
    formData.append("password", password.value);

    const res = await fetch("http://127.0.0.1:8000/api/user/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Login failed");
    }

    localStorage.setItem("token", data.access_token);
    window.location.href = "/crypto";
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