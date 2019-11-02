import Vue from 'vue'
import Router from 'vue-router'
import Mainpage from '@/components/Mainpage'
import AdminLogin from '@/components/AdminLogin'
import MyProfile from '@/components/MyProfile'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Mainpage',
      component: Mainpage
    },
    {
      path:'/adminlogin',
      name:'AdminLogin',
      component:AdminLogin
    },
    {
      path:'/myprofile',
      name:'MyProfile',
      component:MyProfile
    },
  ]
})
