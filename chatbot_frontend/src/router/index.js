import Vue from 'vue'
import Router from 'vue-router'
import Mainpage from '@/components/Mainpage'
import AdminLogin from '@/components/AdminLogin'
import MyProfile from '@/components/MyProfile'
import DetailPage from '@/components/DetailPage'
Vue.use(Router)

export default new Router({
  mode:'history',//remove the '#' in the url
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
      component:MyProfile,
      meta:{
        isLogin:true//do not need login
      }
    },
    {
      path:'/detailpage/:post_id',
      name:'DetailPage',
      component:DetailPage
    }
  ]
})
