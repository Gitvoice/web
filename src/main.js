import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import installElementPlus from './plugins/element'
// import 'element-plus/lib/theme-chalk/index.css';
import './assets/css/style.css'

const app = createApp(App)
installElementPlus(app)
app.use(VueAxios, axios)
app.mount('#app')
