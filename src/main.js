import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 导入字体图标库
import '@fortawesome/fontawesome-free/css/all.css'

createApp(App)
  .use(router)
  .mount('#app')