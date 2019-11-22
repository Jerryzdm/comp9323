<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The post-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848;width: 90%;float: left">Post</h2>
      <a-icon type="plus-circle" style="width: 10%;font-size: 40px" @click="addPost"/>
    </div>
    <div style="clear: both;"></div>


    <!--search component-->
    <div style="padding: 10px 20px;text-align: center">
      <a-input placeholder="search post" v-model="search_post"
               style="float: left;width: 60%;margin-left: 15%"></a-input>
      <a-button style="float: left;margin-left: 5px" @click="searchPost">Search</a-button>
      <div style="clear: both"></div>
    </div>
    <div style="margin: 20px">
      <template v-for=" tag in tags">
        <a-checkable-tag
          :key="tag"
          :checked="selectedTags.indexOf(tag) > -1"
          @change="(checked) => handleTagChange(tag, checked)"
        >
          {{tag}}
        </a-checkable-tag>
      </template>
    </div>

    <div style="margin-top: 20px;margin-bottom: 80px">
      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="postdata"
      >
        <a-list-item slot="renderItem" slot-scope="item, index" style="text-align: left;padding: 0 10px">
          <p>{{item.date|dateformat('YYYY-MM-DD HH:mm')}}</p>
          <p slot='actions' @click="post_detail(item.postId)">Details</p>
          <a-list-item-meta style="width: 500px">
            <p slot="title" style="font-size: 16px;font-weight: bold;width: 500px">{{item.title}}</p>
          </a-list-item-meta>

        </a-list-item>
      </a-list>
    </div>

    <a-modal title="Reviews" v-model="add_visible" @ok="handleaddOk" okText="Post">
      <label>Title</label>
      <a-input size="large" placeholder="title" v-model="title"/>
      <label>Tag</label><br>
      <a-select defaultValue="food" size="large" @change="handleaddTagChange">
        <a-select-option value="food">food</a-select-option>
        <a-select-option value="living">living</a-select-option>
        <a-select-option value="event">event</a-select-option>
      </a-select>
      <br>
      <label>Content</label>
      <a-textarea placeholder="content" :rows="4" v-model="content"/>
    </a-modal>

    <!--<a-modal :title="dataildata.title" v-model="post_visible" @ok="handleOk" okText="Close" >
      <label>{{dataildata.title}}</label><br>
      <label>{{dataildata.content}}</label><br>
      <a-divider>Reply</a-divider>

      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="all_review"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <p >{{item.date|dateformat('YYYY-MM-DD HH:mm')}}</p>
          <a-list-item-meta
            :description="item.content"
          >
            <p slot="title">{{item.authorName}}</p>
          </a-list-item-meta>

        </a-list-item>
      </a-list>

      <a-comment>
        <div slot="content">
          <a-form-item>
            <a-textarea :rows="4" @change="handleChange" v-model="review"></a-textarea>
          </a-form-item>
          <a-form-item>
            <a-button  @click="handleSubmit(dataildata.postId)" type="primary">
              Add Comment
            </a-button>
          </a-form-item>
        </div>
      </a-comment>
    </a-modal>-->
  </div>
</template>

<script>
  import Cookies from 'js-cookie'

  const postdata = []
  const dataildata = {}

  export default {
    data() {
      return {
        postdata,
        postdata_tmp: [],
        dataildata,
        pagination: {
          pageSize: 10,
          showTotal: total => total > 1 ? 'Total ' + total + ' posts' : 'Total ' + total + ' post'
        },
        post_visible: false,
        add_visible: false,
        value: '',
        checked1: false,
        checked2: false,
        checked3: false,
        tags: ['food', 'living','event'],
        selectedTags: [],
        title: '',
        content: '',
        addtag: ['food'],
        review: '',
        all_review: [],
        search_post:''

      }
    },
    methods: {
      /*go to post detail page*/
      post_detail(id) {
        //this.dataildata = this.postdata[index]
        /*this.axios.get("/comments/"+this.dataildata.postId).then((res)=>{
          if(res.status === 200){
            this.all_review = res.data
          }
          console.log(this.all_review)
        })*/
        this.$router.push({name: 'DetailPage', params: {post_id: id}})
      },
      searchPost(){
        if (this.search_post !== '') {
          this.axios.get('/posts/search/' + this.search_post).then((res) => {
            this.postdata = res.data
          })
        } else {
          this.allPost()
        }
      },
      allPost(){
        /*get all the post*/
        this.axios.get("/posts/all").then((res) => {
          if (res.status === 201) {
            this.postdata = res.data
            this.postdata_tmp = res.data
            console.log(res)
          }
        })
      },
      handleOk() {
        this.post_visible = false
      },
      handleChange() {
      },
      /*change selected tag*/
      handleTagChange(tag, checked) {
        const {selectedTags} = this;
        const nextSelectedTags = checked
          ? [...selectedTags, tag]
          : selectedTags.filter(t => t !== tag);
        //console.log('You are interested in: ', nextSelectedTags);
        this.selectedTags = nextSelectedTags;
        if (this.selectedTags.length === 0) {
          this.postdata = this.postdata_tmp
        } else {
          this.axios.post("/posts/tags", {
            "tags": this.selectedTags
          }).then((res) => {
            if (res.status === 201) {
              this.postdata = res.data
              console.log(this.postdata)
              console.log(this.postdata_tmp)
              console.log(this.selectedTags.length)
            }
          })
        }
      },
      handleaddTagChange(value) {
        this.addtag = [value]
        console.log(`selected ${value}`);
      },
      /*show the add post window*/
      addPost() {
        if (Cookies.get('access_token')) {
          this.add_visible = true
        } else {
          this.$message.warning('You haven\'t logged in yet!Please log in!');
        }
      },
      //todo
      /*add new post */
      handleaddOk() {
        this.axios.post('/posts', {
          "title": this.title,
          "tags": this.addtag,
          "content": this.content
        }, {
          headers: {
            'Authorization': Cookies.get('access_token')
          }
        }).then((res) => {
          if (res.status === 201) {
            this.axios.get("/posts/all").then((res) => {
              console.log(res.status)
              console.log(res.data)
              if (res.status === 201) {
                this.postdata = res.data
                this.postdata_tmp = res.data
                this.add_visible = false
              }
            })
          }
        })
      },

    },
    mounted() {
      this.allPost()
    }
  }
</script>
