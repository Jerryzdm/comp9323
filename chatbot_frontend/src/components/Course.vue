<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The Course-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Course</h2>
    </div>

    <!--search component-->
    <div style="padding: 10px 20px;text-align: center">
      <a-input placeholder="search course" v-model="search_course"
               style="float: left;width: 60%;margin-left: 15%"></a-input>
      <a-button style="float: left;margin-left: 5px" @click="searchCourse">Search</a-button>
      <div style="clear: both"></div>
    </div>
    <!--display course component-->
    <a-list :grid="{ gutter: 16, column: 2 }" :dataSource="coursedata" :pagination="course_pagination"
            style="margin: 10px 20px;">
      <a-list-item slot="renderItem" slot-scope="item, index">
        <a-card :title="item.courseCode" style="border-radius: 15px;">

          <!-- <p>{{item.courseCode}}</p>-->
          <div>
            <a-icon type="environment" style="float: left;"/>
            <p style="float: left;margin-left: 20px">{{item.courseCampus}}</p>
            <div style="clear: left"></div>
          </div>
          <div>
            <a-icon type="cluster" style="float: left;"/>
            <p style="float: left;margin-left: 20px">{{item.courseFaculty}}</p>
            <div style="clear: left"></div>
          </div>
          <div>
            <a-icon type="schedule" style="float: left;"/>
            <p style="float: left;margin-left: 20px">{{item.courseTerms}}</p>
            <div style="clear: left"></div>
          </div>
          <div>
            <a-icon type="calculator" style="float: left;"/>
            <p style="float: left;margin-left: 20px">{{item.courseUOC}} UOC</p>
            <div style="clear: left"></div>
          </div>
          <div>
            <a-icon type="read" style="float: left;"/>
            <p
              style="float: left;margin-left: 20px;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;max-width: 250px; ">
              {{item.courseName}}</p>
            <div style="clear: left"></div>
          </div>
          <a slot="actions" :href="item.courseUrl" style="border-radius: 15px;">Details</a>
          <a slot="actions" @click="show_reviews(item.courseId)" style="border-radius: 15px;">Review</a>
          <a-switch slot="actions" checkedChildren="Subscribed" unCheckedChildren="Unsubscribed" :defaultChecked="item.flag"
                    @change="onChange(item.courseId)"  :disabled="disabled"/>
        </a-card>
      </a-list-item>
    </a-list>

    <!--  reviews pop up window-->
    <a-modal title="Reviews" v-model="course_visible" @ok="handleOk" okText="Close">
      <div>

      </div>
      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="data1"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <p slot="actions" v-if="item.sentiment = 1"><a-icon type="like" /></p>
          <p slot="actions" v-else><a-icon type="dislike" /></p>
          <a-list-item-meta>
            <p slot="title"><a-icon type="user" />    {{item.authorName}}</p>
            <p slot="description"><a-icon type="file-word" />    {{item.content}}</p>
          </a-list-item-meta>

        </a-list-item>
      </a-list>

      <a-comment>
        <div slot="content">
          <a-form-item>
            <a-textarea :rows="4" @change="handleChange" v-model="review"></a-textarea>
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
  import Cookies from 'js-cookie'

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
        review: '',
        search_course: '',
        subscribedList: [],
        course_Id:'',
        data1:[],
        disabled:true
      }
    },
    methods: {
      show_reviews(courseId) {
        this.course_Id = courseId
        this.course_visible = true
        this.axios.get('/course/'+courseId+'/reviews').then((res)=>{
          this.data1 = res.data
          console.log(this.data1)
        })
      },
      handleOk() {
        this.course_visible = false
      },
      handleChange() {

      },
      handleSubmit() {
        if(this.review !== '' ){
          this.axios.post('/course/'+this.course_Id+'/reviews',{
            "content": this.review,
            "reply_to":this.course_Id
          },{
            headers: {
              'Authorization': Cookies.get('access_token')
            }
          }).then((res)=>{
            this.$message.success('Add review successfully.')
            this.course_visible = false
          }).catch((e)=>{
            this.$message.warning('You have not logged in.')
            this.review =  ''
          })
        }else{
          this.$message.warning('The review can not be empty.')
        }
      },
      /*Subscribe course*/
      onChange(courseId) {
        if (Cookies.get('access_token')) {
          this.axios.get('/course/subscribe/' + courseId, {
            headers: {
              'Authorization': Cookies.get('access_token')
            }
          }).then((res) => {
            console.log(res)
            this.$message.success('Subscribe successfully!');
          })
        } else {
          this.$message.warning('You haven\'t logged in yet!Please log in!');
        }

      },
      /*search course by name*/
      searchCourse() {
        if (this.search_course !== '') {
          this.axios.get('/course/' + this.search_course).then((res) => {
            this.coursedata = res.data
            this.subscribedCheck(this.coursedata)
          })
        } else {
          this.allCourse()
        }

      },
      /*get all course data*/
      allCourse() {
        this.axios.get("/course").then((res) => {
          this.coursedata = res.data
          this.subscribedCheck(this.coursedata)
          console.log(res.data)
        })
      },
      /*Check if the course is subscribed
      * if it is subscribed, set the flag true otherwise false
      * if not login in, set flag false*/
      subscribedCheck(courseData) {
        courseData.forEach((item) => {
          if (Cookies.get('access_token')) {
            if (this.subscribedList.indexOf(item.courseId) != -1) {
              console.log(item.courseId)
              console.log(item)
              item['flag'] = true
            } else {
              item['flag'] = false
            }
          } else {
            item['flag'] = false
          }
        })
      }
    },
    mounted() {
      /*Execute when the page loads*/
      if (Cookies.get('access_token')) {
        this.disabled = false
        this.axios.get('/course/subscribe', {
          headers: {
            'Authorization': Cookies.get('access_token')
          }
        }).then((res) => {
          this.subscribedList = res.data
          this.allCourse()
        })
      } else {
        this.allCourse()
      }

    }
  }
</script>
