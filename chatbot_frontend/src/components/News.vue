<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">News</h2>
    </div>



    <a-list itemLayout="horizontal" :dataSource="data1" :pagination="pagination">
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a-list-item-meta
          description="Ant Design, a design language for background applications, is refined by Ant UED Team"
        >
          <a slot="title">{{item.description}}</a>
          <a-avatar
            slot="avatar"
            src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png"
          />
        </a-list-item-meta>
      </a-list-item>
    </a-list>
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
