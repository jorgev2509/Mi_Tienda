import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import App from './App.vue'
import Login from './views/Login.vue'
import Products from './views/Products.vue'
import Inventory from './views/Inventory.vue'
import Pos from './views/Pos.vue'
import Users from './views/Users.vue'

const routes = [
  { path: '/login', component: Login }, { path: '/', redirect: '/pos' },
  { path: '/pos', component: Pos, meta: { auth: true } },
  { path: '/products', component: Products, meta: { auth: true } },
  { path: '/inventory', component: Inventory, meta: { auth: true } },
  { path: '/users', component: Users, meta: { auth: true } },
]
const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach(to => to.meta.auth && !localStorage.getItem('token') ? '/login' : true)
createApp(App).use(createPinia()).use(router).use(createVuetify({ theme: { defaultTheme: 'light', themes: { light: { colors: { primary: '#14532d', secondary: '#f59e0b' } } } } })).mount('#app')

