<script setup>
import { ref } from 'vue'; import { useRouter } from 'vue-router'; import api from '../api'
const email=ref('admin@mitienda.local'), password=ref('Admin123!'), error=ref(''), loading=ref(false), router=useRouter()
async function login(){ loading.value=true; error.value=''; try { const body=new URLSearchParams({username:email.value,password:password.value}); const {data}=await api.post('/auth/login',body); localStorage.setItem('token',data.access_token); localStorage.setItem('user',JSON.stringify(data.user)); router.push('/pos') } catch(e){ error.value=e.response?.data?.detail || 'No fue posible ingresar' } finally { loading.value=false } }
</script>
<template><v-row justify="center" align="center" style="min-height:85vh"><v-col cols="12" sm="7" md="4"><v-card class="pa-7" elevation="8"><v-card-title class="text-h4 mb-4">Mi Tienda</v-card-title><v-card-subtitle class="mb-5">Ingresa al sistema de ventas</v-card-subtitle><v-alert v-if="error" type="error" class="mb-4">{{error}}</v-alert><v-form @submit.prevent="login"><v-text-field v-model="email" label="Correo" prepend-inner-icon="mdi-email"/><v-text-field v-model="password" label="Contraseña" type="password" prepend-inner-icon="mdi-lock"/><v-btn block size="large" color="primary" type="submit" :loading="loading">Ingresar</v-btn></v-form></v-card></v-col></v-row></template>

