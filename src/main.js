import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Importiere die einzelnen Seitenkomponenten
import VerlagList from './components/VerlagList.vue';
import VerlagForm from './components/VerlagForm.vue';
import AutorList from './components/AutorList.vue';
import AutorForm from './components/AutorForm.vue';
import BuchList from './components/BuchList.vue';
import BuchForm from './components/BuchForm.vue';
import BuchAutorList from './components/BuchAutorList.vue';
import BuchAutorForm from './components/BuchAutorForm.vue';



// Importiere die CSS-Dateien
import './assets/base.css';  // Basis-Styles wie Reset oder Grundlayout
import './assets/main.css';  // Haupt-Design-Styles



const routes = [
  { path: '/', component: VerlagList },
  { path: '/verlage', component: VerlagList },
  { path: '/verlage/new', component: VerlagForm },
  { path: '/verlage/:id/edit', component: VerlagForm },
  
  { path: '/autoren', component: AutorList },
  { path: '/autoren/new', component: AutorForm },
  { path: '/autoren/:id/edit', component: AutorForm },

  { path: '/buecher', component: BuchList },
  { path: '/buecher/new', component: BuchForm },
  { path: '/buecher/:id/edit', component: BuchForm },

  { path: '/buchautoren', component: BuchAutorList },
  { path: '/buchautoren/new', component: BuchAutorForm },
  { path: '/buchautoren/:id/edit', component: BuchAutorForm }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

const app = createApp(App);
app.use(router);
app.mount('#app');
