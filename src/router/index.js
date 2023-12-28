import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import UserListView from '../views/UserListView.vue'
import TestView from '../views/TestView.vue'
//import ElementView from '../views/ElementView.vue'
//import VantView from '../views/VantView.vue'
import UserListBootstrapView from '../views/UserListBootstrapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Main',
      component: UserListView
    },
    {
      path: '/users',
      name: 'userList',
      component: UserListView
    },
    {
      path: '/invoices',
      name: 'invoicesList',
      component: UserListView
    },
    {
      path: '/report',
      name: 'reports',
      component: TestView
    },
    {
      path: '/ulb',
      name: 'ULB',
      component: UserListBootstrapView
    }
    //,
    // {
    //   path: '/vant',
    //   name: 'vant',
    //   component: VantView
    // }
    //,
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ],
  linkExactActiveClass: 'active' // active class for *exact* links.
})

export default router
