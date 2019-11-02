<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The Course-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Course</h2>
    </div>
    <a-list :grid="{ gutter: 16, column: 3 }" :dataSource="coursedata" :pagination="course_pagination" style="margin-top: 20px;margin-right: 20px;margin-left: 20px">
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a-card :title="item.courseCode">
          <p>{{item.courseCode}}</p>
          <p>{{item.courseName}}</p>
          <p>{{item.courseUOC}}</p>
          <a slot="actions" :href="item.courseUrl">Details</a>
          <a slot="actions" @click="show_reviews(item.title)">Review</a>
        </a-card>
      </a-list-item>
    </a-list>



    <!--  reviews pop up window-->
    <a-modal title="Reviews" v-model="course_visible" @ok="handleOk" okText="Close" >

      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="data1"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <p slot="actions">{{item.number}}</p>
          <a-list-item-meta
            :description="item.number"
          >
            <p slot="title">{{item.title}}&nbsp;&nbsp;{{item.time}}</p>
          </a-list-item-meta>

        </a-list-item>
      </a-list>

      <a-comment>
        <div slot="content">
          <a-form-item>
            <a-textarea :rows="4" @change="handleChange" :value="value"></a-textarea>
          </a-form-item>
          <a-form-item>
            <a-button  @click="handleSubmit" type="primary">
              Add Comment
            </a-button>
          </a-form-item>
        </div>
      </a-comment>
    </a-modal>
  </div>
</template>

<script>
  const data = [
    {
      title: 'COMP9021',
    },
    {
      title: 'COMP9020',
    },
    {
      title: 'COMP9311',
    },
    {
      title: 'COMP9331',
    },
  ];
  export default {
    data(){
      return{
        data,
        coursedata:[],
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' courses' : 'Total ' + total + ' course'
        },
        course_pagination: {
          pageSize: 6,
          showTotal: total => total > 1 ? 'Total ' + total + ' courses' : 'Total ' + total + ' course'
        },
        course_visible:false,
        value:'',
      }
    },
    methods:{
      show_reviews(title){
        console.log(title)
        this.course_visible = true
      },
      handleOk(){
        this.course_visible = false
      },
      handleChange(){

      },
      handleSubmit(){

      }
    },
    mounted() {
      this.axios.get("/course").then((res)=>{
        this.coursedata = res.data
        console.log(res.data)
      })
    }
  }
</script>
