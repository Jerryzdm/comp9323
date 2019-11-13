<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The Course-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Course</h2>
    </div>
    <div style="padding: 10px 20px;text-align: center">

      <a-input placeholder="search course" v-model="search_course"
               style="float: left;width: 60%;margin-left: 15%"></a-input>
      <a-button style="float: left;margin-left: 5px">Search</a-button>
      <div style="clear: both"></div>
    </div>
    <a-list :grid="{ gutter: 16, column: 2 }" :dataSource="coursedata" :pagination="course_pagination"
            style="margin: 10px 20px;">
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a-card :title="item.courseCode" style="border-radius: 15px;">

          <!-- <p>{{item.courseCode}}</p>-->
          <div>
          <a-icon type="environment" style="float: left;"/><p style="float: left;margin-left: 20px">{{item.courseCampus}}</p>
            <div style="clear: left"></div>
          </div>
          <div>
          <a-icon type="cluster" style="float: left;"/><p style="float: left;margin-left: 20px">{{item.courseFaculty}}</p>
            <div style="clear: left"></div>
          </div>
          <div>
            <a-icon type="schedule" style="float: left;"/><p style="float: left;margin-left: 20px">{{item.courseTerms}}</p>
          <div style="clear: left"></div>
          </div>
          <div>
            <a-icon type="calculator" style="float: left;"/><p style="float: left;margin-left: 20px">{{item.courseUOC}} UOC</p>
            <div style="clear: left"></div>
          </div>
          <div>
          <a-icon type="read" style="float: left;"/>
            <p style="float: left;margin-left: 20px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;max-width: 250px; ">{{item.courseName}}</p>
          <div style="clear: left"></div>
  </div>
          <a slot="actions" :href="item.courseUrl" style="border-radius: 15px;">Details</a>
          <a slot="actions" @click="show_reviews(item.title)" style="border-radius: 15px;">Review</a>
          <a-switch slot="actions" checkedChildren="on" unCheckedChildren="off" :defaultChecked="false"/>
        </a-card>
      </a-list-item>
    </a-list>

    <!--  reviews pop up window-->
    <a-modal title="Reviews" v-model="course_visible" @ok="handleOk" okText="Close">

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
            <a-button @click="handleSubmit" type="primary">
              Add Review
            </a-button>
          </a-form-item>
        </div>
      </a-comment>
    </a-modal>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        coursedata: [],
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' reviews' : 'Total ' + total + ' review'
        },
        course_pagination: {
          pageSize: 6,
          showTotal: total => total > 1 ? 'Total ' + total + ' courses' : 'Total ' + total + ' course'
        },
        course_visible: false,
        value: '',
      }
    },
    methods: {
      show_reviews(title) {
        console.log(title)
        this.course_visible = true
      },
      handleOk() {
        this.course_visible = false
      },
      handleChange() {

      },
      handleSubmit() {

      }
    },
    mounted() {
      this.axios.get("/course").then((res) => {
        this.coursedata = res.data
        console.log(res.data)
      })
    }
  }
</script>
