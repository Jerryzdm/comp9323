<template>
  <!--loginhead component-->
  <div>
    <div style="margin-left: 5%;margin-right: 5%;margin-top: -50px">
      <login-header style="float: right;width: 50%;"></login-header>
      <!--to clear the float-->
      <div style="clear: both"></div>
    </div>

    <div style="padding: 20px 50px">
      <label style="font-size: 16px;font-weight: bold;">{{dataildata.title}}</label><br>
      <a-divider>Reply</a-divider>

      <!--list of reviews-->
      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="all_review"
        style="text-align: left;"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <p>{{item.date|dateformat('YYYY-MM-DD HH:mm')}}</p>
          <a-list-item-meta
            :description="item.content"
            style="width:500px"
          >
            <p slot="title" style="width:500px">{{item.authorName}}</p>
          </a-list-item-meta>

        </a-list-item>
      </a-list>

      <!--Add Comment-->
      <a-comment>
        <div slot="content">
          <a-form-item>
            <a-textarea :rows="4" @change="handleChange" v-model="review"></a-textarea>
          </a-form-item>
          <a-form-item>
            <a-button @click="handleSubmit(dataildata.postId)" type="primary">
              Add Comment
            </a-button>
          </a-form-item>
        </div>
      </a-comment>
    </div>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'
  import LoginHeader from "./../components/LoginHeader"

  export default {
    name: "DetailPage",
    components: {LoginHeader},
    data() {
      return {
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' posts' : 'Total ' + total + ' post'
        },
        dataildata: {},
        review: '',
        all_review: [],
        dataildata: []
      }
    },
    methods: {
      handleChange() {
      },
      /*submit comments*/
      handleSubmit(postId) {
        console.log(this.review)
        console.log(postId)
        this.axios.post("/comments", {
            "content": this.review,
            "reply_to": postId
          },
          {
            headers: {
              'Authorization': Cookies.get('access_token')
            }
          }).then((res) => {
          if (res.status === 201) {
            this.$message.success('Post successfully!');
            console.log("Add comments successfully")
            this.axios.get("/comments/" + this.$route.params.post_id).then((res) => {
              if (res.status === 200) {
                this.all_review = res.data
              }
              console.log(this.all_review)
            })
            this.review = ''
          } else {
            this.$message.error('Post failure!');
          }
        }).catch((e) => {
          this.$message.error('Post failure!You should login first.');
        })

      },
    },
    mounted() {

      /*Execute when the page loads*/
      /*get all comments by postId*/
      this.axios.get("/comments/" + this.$route.params.post_id).then((res) => {
        if (res.status === 200) {
          this.all_review = res.data
        }
        //console.log(this.all_review)
      })

      /*get post content by postId*/
      this.axios.get("/posts/" + this.$route.params.post_id).then((res) => {
        if (res.status === 200) {
          this.dataildata = res.data
        }
        console.log(this.dataildata)
      })
    }
  }
</script>

<style scoped>

</style>
