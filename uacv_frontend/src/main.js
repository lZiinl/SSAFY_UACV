/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
// import router from './router'
// import store from './store'
// import axios from './plugins/axios'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

const app = createApp(App)

registerPlugins(app)

// Use router and store
// app.use(router)
// app.use(store)

// Add axios to app config globalProperties
// app.config.globalProperties.$axios = axios

app.mount('#app')
