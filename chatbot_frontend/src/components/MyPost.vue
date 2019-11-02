<template>
  <div>

    <div style="margin-left: 5%;margin-right: 5%;margin-top: -50px">
      <login-header style="float: right;width: 50%;"></login-header>
      <!--to clear the float-->
      <div style="clear: both"></div>
    </div>


  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">News</h2>
    </div>
    <div style="margin-top: 20px;margin-bottom: 80px">
      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="postdata"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <a slot="actions">details</a>
          <a slot="actions">delete</a>

          <a-list-item-meta
            :description="item.content"
          >

          </a-list-item-meta>
          <div>{{item.date|dateformat('YYYY-MM-DD')}}</div>
        </a-list-item>
      </a-list>
    </div>

  </div>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'
  import LoginHeader from "./../components/LoginHeader"
  const data1 = [{id: '1', description: 'title', name: 'name', price: 'price', rating: 'rating'}]
  export default {
    components: {LoginHeader},
    data() {
      return {
        postdata:[],
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' news' : 'Total ' + total + ' news'
        },
      }
    },
    mounted() {
      this.axios.get("/comments/users/"+Cookies.get("uid"),{
        headers:{
          'Authorization':Cookies.get('access_token')
        }
      }).then((res)=>{
        this.postdata = res.data
        console.log(res.data)
      })
    }
  }
</script>
