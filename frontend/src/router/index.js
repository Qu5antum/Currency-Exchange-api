import { createRouter, createWebHistory } from "vue-router";
import MainPage      from "../pages/main.vue";
import RegisterPage  from "@/pages/register.vue";
import LoginPage     from "@/pages/login.vue";
import CryptoList    from "../pages/crypto_list.vue";
import CryptoDetail  from "../pages/crypto_detail.vue";
import CryptoSearch  from "../pages/crypto_search.vue";
import PortfolioList     from "../pages/portfolio_list.vue";
import PortfolioDetail   from "../pages/portfolio_detail.vue";
import Transactions      from "../pages/transactions.vue";

const routes = [
  // ── Public ────────────────────────────────────────────────
  { path: "/",               name: "Home",        component: MainPage },
  { path: "/register",       name: "Register",    component: RegisterPage },
  { path: "/login",          name: "Login",       component: LoginPage },
  { path: "/crypto",         name: "CryptoList",  component: CryptoList },
  { path: "/crypto/search",  name: "CryptoSearch",component: CryptoSearch },
  { path: "/crypto/:symbol", name: "CryptoDetail",component: CryptoDetail, props: true },

  // ── Protected ─────────────────────────────────────────────
  {
    path: "/portfolio",
    name: "PortfolioList",
    component: PortfolioList,
    meta: { requiresAuth: true },
  },
  {
    path: "/portfolio/:id",
    name: "PortfolioDetail",
    component: PortfolioDetail,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/portfolio/:id/transactions",
    name: "Transactions",
    component: Transactions,
    props: true,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next({ name: "Login", query: { redirect: to.fullPath } });
    return;
  }

  // Если уже залогинен — не пускаем обратно на login/register
  if ((to.name === "Login" || to.name === "Register") && token) {
    next({ name: "PortfolioList" });
    return;
  }

  next();
});

export default router;