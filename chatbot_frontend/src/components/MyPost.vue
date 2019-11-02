<template>
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
        :dataSource="data1"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <a slot="actions">details</a>
          <a slot="actions">delete</a>

          <a-list-item-meta
            :description="item.description"
          >

          </a-list-item-meta>
          <div>time</div>
        </a-list-item>
      </a-list>
    </div>

  </div>
</template>

<script>
  const data1 = [{id: '1', description: 'title', name: 'name', price: 'price', rating: 'rating'}]
  export default {
    data() {
      return {
        data1,
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' news' : 'Total ' + total + ' news'

        },
      }
    }
  }
</script>
