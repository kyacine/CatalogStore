import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import ProductDetailView from "../views/ProductDetailView.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/products/:id", name: "product-detail", component: ProductDetailView },
  ],
})

export default router