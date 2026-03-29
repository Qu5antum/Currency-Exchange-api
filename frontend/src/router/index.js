import { createRouter, createWebHistory } from "vue-router";
import MainPage from "../pages/main.vue"; 
import RegisterPage from "@/pages/register.vue";
import LoginPage from "@/pages/login.vue";


const routes = [
  { path: "/", name: "Home", component: MainPage },
  { path: "/register", name: "Register", component: RegisterPage},
  { path: "/login", name: "Login", component: LoginPage}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;