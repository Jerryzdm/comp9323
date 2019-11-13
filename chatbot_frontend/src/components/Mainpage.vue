<template>
  <div><div style="margin-left: 5%;margin-right: 5%;margin-top: -50px">
    <login-header style="float: right;width: 50%;"></login-header>
    <!--to clear the float-->
    <div style="clear: both"></div>
  </div>

  <div style="margin-top: 20px">
    <a-layout>
      <a-layout-content style="padding: 50px 100px">
        <a-layout style="padding: 24px 0; background: #fff">
          <a-layout-sider width="200" style="background: #fff">
            <a-menu
              mode="inline"
              :defaultSelectedKeys="['1']"
              style="height: 100%"
              onclick={this.onclick.bind(this)}
            >
              <a-menu-item key="1" @click="changepage('News')">News</a-menu-item>
              <a-menu-item key="2" @click="changepage('Post')">Post</a-menu-item>
              <a-menu-item key="3" @click="changepage('Course')">Course</a-menu-item>
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
  import News from "./News"
  import Post from "./Post"
  import Course from "./Course"
  import LoginHeader from "./../components/LoginHeader"
  export default {
    components: {News,Post,Course,LoginHeader},
    methods: {
      changepage(page) {
        this.currentPage = page
      }
    },
    data(){
      return {
        currentPage: News,
        News: News,
        Post: Post,
        Course:Course,

      }
    },

  }
</script>

<style scoped>
</style>
