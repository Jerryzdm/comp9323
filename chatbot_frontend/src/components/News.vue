<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">News</h2>
    </div>
    <!--list of news data-->
    <a-list itemLayout="horizontal" :dataSource="newsdata" :pagination="pagination"
            style="text-align: left;padding: 0 10px">
      <a-list-item slot="renderItem" slot-scope="item, index">
        <p slot="actions">{{item.newsDate}}</p>
        <a-list-item-meta
          :description="item.newsStandfirst"
        >
          <a slot="title" :href="item.newsUrl" style="font-size: 16px;font-weight: bold">{{item.newsTitle}}</a>
        </a-list-item-meta>
      </a-list-item>
    </a-list>


  </div>

</template>

<script>
  export default {
    data() {
      return {
        newsdata: [],
        pagination: {
          pageSize: 10,
          showTotal: total => total > 1 ? 'Total ' + total + ' news' : 'Total ' + total + ' news'
        },

      }
    },
    mounted() {
      this.axios.get("/news").then((res) => {
        this.newsdata = res.data
        console.log(this.newsdata)
      })
    }
  }
</script>
