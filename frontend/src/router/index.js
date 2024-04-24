// import { createApp } from 'vue';
// import App from '../App.vue';
// import VueRouter from 'vue-router';
import { createRouter, createWebHistory } from 'vue-router';
import QueryFlight from '@/components/QueryFlight.vue'
import LoginUi from "../components/LoginUi.vue";
import RegisterTravel from "../components/RegisterTravel.vue"
import QueryShow from "../components/query_show.vue"
import CustomerTicket from "../components/CustomerTicket.vue"
import UserCommon from "../components/UserCommon.vue"

import QueryFlightRoot from "../components/root/QueryFlightRoot.vue"
import QueryShowRoot from "../components/root/query_showRoot.vue"
import UserProfile from "../components/root/UserProfile.vue"


// 创建应用实例
// const app = createApp(App);

// // 使用 VueRouter 插件
// app.use(VueRouter);

// 定义路由规则
const routes = [
  {
    path: '/',
    name: 'Home',
    component:LoginUi,  // 替换成实际的组件
  },
  {
    path:'/UserCommon',
    name:'UserCommon',
    component:UserCommon
  },
  { path: '/query',
  name: 'query',
  component:QueryFlight },
  {
    path:'/register',
    name:'register',
    component:RegisterTravel},
  { path: '/query/query_show',
  name: 'query_show',
  component:QueryShow },
  {
    path:'/queryRoot',
    name:'QueryFlightRoot',
    component:QueryFlightRoot
  },
  {
    path:'/queryRoot',
    name:'QueryFlightRoot',
    component:QueryFlightRoot
  },
  {
    path:'/queryRoot/query_showRoot',
    name:'QueryShowRoot',
    component:QueryShowRoot
  },
  {
    path:'/query/query_show/CustomerTicket',
    name:"CustomerTicket",
    component:CustomerTicket,
  },
  {
    path:'/UserProfile',
    name:"UserProfile",
    component:UserProfile,
  }
];

// 创建路由实例
const router = createRouter({
  history:createWebHistory(),
  routes,
});
export default router;
// 将路由实例添加到应用实例
// app.use(router);

// 挂载应用实例到页面上
// app.mount('#app');
