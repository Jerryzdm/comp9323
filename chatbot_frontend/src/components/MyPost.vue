<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Comments</h2>
    </div>
    <div style="margin-top: 20px;margin-bottom: 80px">
      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="postdata"
      >
        <a-list-item slot="renderItem" slot-scope="item, index" >
          <a slot="actions">details</a>
          <a slot="actions" @click="delete_comment(item)">delete</a>
          <a-list-item-meta
            :description="item.content"  >
          </a-list-item-meta>
          <div>{{item.date|dateformat('YYYY-MM-DD')}}</div>
        </a-list-item>
      </a-list>
    </div>

  </div>
</template>

<script>
  import Cookies from 'js-cookie'
  import LoginHeader from "./../components/LoginHeader"

  export default {
    components: {LoginHeader},
    data() {
      return {
        postdata: [],
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' posts' : 'Total ' + total + ' post'
        },
      }
    },
    methods: {
      /*delete de cpmment*/
      delete_comment(item) {
        this.axios.delete('/comments/' + item.commentId, {
          data: {
            'content': item.content,
            'reply_to': item.reply_to
          },
          headers: {
            'Authorization': Cookies.get('access_token')
          }
        }).then((res) => {
          this.axios.get("/comments/users/" + Cookies.get("uid"), {
            headers: {
              'Authorization': Cookies.get('access_token')
            }
          }).then((res_delete) => {
            this.postdata = res_delete.data
            console.log(res_delete.data)
          })
          this.$message.success('Deleting successfully!');
          console.log('delete successfully')
        })
      }
    },
    mounted() {
      this.axios.get("/comments/users/" + Cookies.get("uid"), {
        headers: {
          'Authorization': Cookies.get('access_token')
        }
      }).then((res) => {
        this.postdata = res.data
        console.log(res.data)
      })
    }
  }
</script>
