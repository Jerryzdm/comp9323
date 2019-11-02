<template>
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
              <a-menu-item key="1" @click="changepage('MyPost')">MyPost</a-menu-item>
              <a-menu-item key="2" @click="changepage('AdminCourse')">AdminCourse</a-menu-item>
              <a-menu-item key="3" @click="changepage('ChangePassword')">ChangePassword</a-menu-item>
            </a-menu>
          </a-layout-sider>
          <a-layout-content :style="{minHeight: '500px' }" :is="currentPage"></a-layout-content>
        </a-layout>
      </a-layout-content>

    </a-layout>
  </div>
</template>

<script>
  import MyPost from "./MyPost"
  import AdminCourse from "./AdminCourse"
  import ChangePassword from "./ChangePassword"
  export default {
    components: {MyPost,AdminCourse,ChangePassword},
    methods: {
      changepage(page) {
        this.currentPage = page
      }
    },
    data(){
      return {
        currentPage: MyPost,
        AdminNews: MyPost,
        AdminCourse:AdminCourse,
        ChangePassword:ChangePassword,
      }
    }
  }
</script>
