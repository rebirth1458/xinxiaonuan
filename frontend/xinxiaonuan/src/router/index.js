import { createRouter, createWebHistory } from 'vue-router'
import home from '../view/index.vue'
import test from '../view/test/test.vue'
import chat from '../view/chat/chat.vue'
import login from '../view/login/login.vue'
import register from '../view/register/register.vue'
const routes = [
  {
    path:'/xiaonuan',
    name:'xiaonuan',
    component:home,
    children:[
     {
      path:'test',
      name:'test',
      component:test
     },
     {
      path:'chat',
      name:'chat',
      component:chat
     }
    ]
  },
  {
    path:'/login',
    name:'login',
    component:login
  },
  {
    path:"/register",
    component:register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router