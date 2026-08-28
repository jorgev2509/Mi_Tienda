<script setup>
import { onMounted, ref } from 'vue'; import api from '../api'
const users=ref([]),roles=ref([]),error=ref(''),dialog=ref(false),form=ref({email:'',full_name:'',password:'',role_ids:[]})
async function load(){try{[users.value,roles.value]=await Promise.all([api.get('/users').then(r=>r.data),api.get('/roles').then(r=>r.data)])}catch(e){error.value=e.response?.data?.detail}}
async function save(){try{await api.post('/users',form.value);dialog.value=false;form.value={email:'',full_name:'',password:'',role_ids:[]};await load()}catch(e){error.value=e.response?.data?.detail}}
onMounted(load)
</script>
<template><div class="d-flex justify-space-between mb-5"><h1>Usuarios</h1><v-btn color="primary" prepend-icon="mdi-account-plus" @click="dialog=true">Nuevo usuario</v-btn></div><v-alert v-if="error" type="error" closable class="mb-4">{{error}}</v-alert><v-card><v-table><thead><tr><th>Nombre</th><th>Correo</th><th>Roles</th><th>Estado</th></tr></thead><tbody><tr v-for="u in users" :key="u.id"><td>{{u.full_name}}</td><td>{{u.email}}</td><td>{{u.roles.map(r=>r.name).join(', ')}}</td><td><v-chip color="success">Activo</v-chip></td></tr></tbody></v-table></v-card><v-dialog v-model="dialog" max-width="550"><v-card title="Nuevo usuario" class="pa-4"><v-card-text><v-text-field v-model="form.full_name" label="Nombre completo"/><v-text-field v-model="form.email" label="Correo"/><v-text-field v-model="form.password" type="password" label="Contraseña (mínimo 8 caracteres)"/><v-select v-model="form.role_ids" :items="roles" item-title="name" item-value="id" label="Roles" multiple chips/></v-card-text><v-card-actions><v-spacer/><v-btn @click="dialog=false">Cancelar</v-btn><v-btn color="primary" @click="save">Guardar</v-btn></v-card-actions></v-card></v-dialog></template>

