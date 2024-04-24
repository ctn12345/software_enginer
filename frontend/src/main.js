import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus' //全局引入
import 'element-plus/dist/index.css'


import * as ElementPlusIconsVue from '@element-plus/icons-vue'




const app = createApp(App)



for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(router).use(ElementPlus)
app.mount('#app')
// 1. 定义路由组件.
// 也可以从其他文件导入

// import VueRouter from 'vue-router'

// Vue.use(VueRouter)

// 现在，应用已经启动了！