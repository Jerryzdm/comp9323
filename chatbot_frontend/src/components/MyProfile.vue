<template>
  <div>
    <div style="margin-left: 5%;margin-right: 5%;margin-top: -50px">
      <login-header style="float: right;width: 50%;"></login-header>
      <!--to clear the float-->
      <div style="clear: both"></div>
    </div>
    <div style="margin-top: 20px">


      <a-layout>
        <a-layout-content style="padding: 50px 200px">
          <a-layout style="padding: 24px 0; background: #fff">
            <a-layout-sider width="200" style="background: #fff">
              <a-menu
                mode="inline"
                :defaultSelectedKeys="['1']"
                style="height: 100%"
                onclick={this.onclick.bind(this)}
              >
                <a-menu-item key="1" @click="changepage('MyPost')">MyComment</a-menu-item>
                <!--<a-menu-item key="2" @click="changepage('AdminCourse')">AdminCourse</a-menu-item>-->
                <a-menu-item key="3" @click="changepage('ChangePassword')">ChangePassword</a-menu-item>
              </a-menu>
            </a-layout-sider>
            <a-layout-content :style="{minHeight: '500px' }" :is="currentPage"></a-layout-content>
          </a-layout>
        </a-layout-content>

      </a-layout>
    </div>
  </div>
</template>

<script>
  import MyPost from "./MyPost"
  /*import AdminCourse from "./AdminCourse"*/
  import ChangePassword from "./ChangePassword"
  import LoginHeader from "./../components/LoginHeader"

  export default {
    components: {MyPost, ChangePassword, LoginHeader},
    methods: {
      changepage(page) {
        this.currentPage = page
      }
    },
    data() {
      return {
        currentPage: MyPost,
        AdminNews: MyPost,
        ChangePassword: ChangePassword,
      }
    }
  }
</script>
