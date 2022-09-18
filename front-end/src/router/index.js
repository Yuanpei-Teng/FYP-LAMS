import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
  },

  {
    path: '/customer/add/course/:id',
    name: 'customerAddCourse',
    component: () => import(/* webpackChunkName: "customerAddCourse" */ '../views/student/emailAddCourse.vue')
  },

  {
    path: '/teacher/index',
    name: 'teacherIndex',
    component: () => import(/* webpackChunkName: "teacher" */ '../views/TIndex.vue')
  },

  {
    path: '/student/index',
    name: 'studentIndex',
    component: () => import(/* webpackChunkName: "teacher" */ '../views/SIndex.vue')
  },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
