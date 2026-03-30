import { createRouter, createWebHistory } from "vue-router";
import MainPage from "../pages/main.vue"; 
import RegisterPage from "@/pages/register.vue";
import LoginPage from "@/pages/login.vue";
import CryptoList from "../pages/crypto_list.vue";
import CryptoDetail from "../pages/crypto_detail.vue";
import CryptoSearch from "../pages/crypto_search.vue";


const routes = [
  { path: "/", name: "Home", component: MainPage },
  { path: "/register", name: "Register", component: RegisterPage},
  { path: "/login", name: "Login", component: LoginPage},
  { path: "/crypto", component: CryptoList },
  { path: "/crypto/search", component: CryptoSearch },
  { path: "/crypto/:symbol", component: CryptoDetail, props: true }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;