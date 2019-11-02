// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Antd from 'ant-design-vue'
import axios from 'axios'
import Cookies from 'js-cookie'

import 'ant-design-vue/dist/antd.css'

Vue.config.productionTip = false

axios.defaults.baseURL = "http://127.0.0.1:5000"
Vue.prototype.axios = axios
Vue.use(Antd)
Vue.use(Cookies)
Vue.prototype.axios = axios
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
