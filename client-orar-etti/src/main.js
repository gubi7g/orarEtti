import Vue from 'vue'
import OrarFull from './views/OrarFull.vue'
import Login from './views/Login.vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import { BootstrapVue } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from 'axios'

Vue.config.productionTip = false
Vue.prototype.$http = axios

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/orar',
      name: 'orar',
      component: OrarFull
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ],
  mode: 'history'
})



new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
