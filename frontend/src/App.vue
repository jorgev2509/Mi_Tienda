<script setup>
import { useRoute, useRouter } from 'vue-router'
const route = useRoute(), router = useRouter()
const logout = () => { localStorage.clear(); router.push('/login') }
</script>
<template>
  <v-app>
    <template v-if="route.path !== '/login'">
      <v-app-bar color="primary"><v-app-bar-title>Mi Tienda ERP</v-app-bar-title><v-btn to="/pos">POS</v-btn><v-btn to="/products">Productos</v-btn><v-btn to="/inventory">Inventario</v-btn><v-btn to="/users">Usuarios</v-btn><v-btn icon="mdi-logout" @click="logout" /></v-app-bar>
    </template>
    <v-main class="bg-grey-lighten-4"><v-container fluid class="pa-6"><router-view /></v-container></v-main>
  </v-app>
</template>

