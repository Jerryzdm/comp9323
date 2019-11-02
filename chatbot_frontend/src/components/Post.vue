<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The post-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848;width: 90%;float: left">Post</h2>
      <a-icon type="plus-circle" style="width: 10%;font-size: 40px" @click="addPost"/>
    </div>

    <div>
      <strong :style="{ marginRight: 8 }">Categories:</strong>
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
        :dataSource="data1"
      >
        <a-list-item slot="renderItem" slot-scope="item, index" @click="post_detail(item.postId)">
          <p slot="actions">{{item.date}}</p>

          <a-list-item-meta
            :description="item.title"
          >
          </a-list-item-meta>
          <div>{{item.content}}</div>
        </a-list-item>
      </a-list>
    </div>

    <a-modal title="Reviews" v-model="add_visible" @ok="handleaddOk" okText="Post" >
      <label>Title</label>
      <a-input size="large" placeholder="title" v-model="title"/>
      <label>Tag</label><br>
      <a-select defaultValue="Movies" size="large" @change="handleaddTagChange">
        <a-select-option value="Movies">Movies</a-select-option>
        <a-select-option value="Music">Music</a-select-option>
        <a-select-option value="Books">Books</a-select-option>
        <a-select-option value="Sports">Sports</a-select-option>
      </a-select><br>
      <label>Content</label>
      <a-textarea placeholder="content" :rows="4" v-model="content"/>
    </a-modal>

    <a-modal :title="dataildata.title" v-model="post_visible" @ok="handleOk" okText="Close" >
      <label>{{dataildata.title}}</label><br>
      <label>{{dataildata.content}}</label><br>
      <a-divider>Reply</a-divider>

      <a-list
        itemLayout="horizontal"
        size="large"
        :pagination="pagination"
        :dataSource="data1"
      >
        <a-list-item slot="renderItem" slot-scope="item, index">
          <p slot="actions">{{item.date}}</p>
          <a-list-item-meta
            :description="item.content"
          >
            <p slot="title">{{item.title}}&nbsp;&nbsp;{{item.authorName}}</p>
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
    </a-modal>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'
  import moment from 'moment'
  const data1 = []
  const dataildata = {}
  export default {
    data(){
      return{
        data1,
        dataildata,
        pagination: {
          pageSize: 5,
          showTotal: total => total > 1 ? 'Total ' + total + ' posts' : 'Total ' + total + ' post'
        },
        post_visible:false,
        add_visible:false,
        value: '',
        checked1: false,
        checked2: false,
        checked3: false,
        tags: ['Movies', 'Books', 'Music', 'Sports'],
        selectedTags: [],
        title:'' ,
        content:'',
        addtag:[],
        review:''
      }
    },
    methods:{
      post_detail(id){
        this.dataildata = this.data1[id-1]
        this.post_visible = true
      },


      handleOk(){
        this.post_visible = false
      },
      handleChange(){
      },

      handleTagChange(tag, checked) {
        const { selectedTags } = this;
        const nextSelectedTags = checked
          ? [...selectedTags, tag]
          : selectedTags.filter(t => t !== tag);
        //console.log('You are interested in: ', nextSelectedTags);
        this.selectedTags = nextSelectedTags;
      },
      handleaddTagChange(value) {
        this.addtag = [value]
        console.log(`selected ${value}`);
      },

      addPost(){
        this.add_visible = true
      },
      //todo
      handleaddOk(){
        console.log(this.title)
        console.log(this.content)
        this.axios.post('/posts',{
          "title":this.title,
          "tags":this.addtag,
          "content":this.content
        },{
          headers:{
            'Authorization':Cookies.get('access_token')
          }
        }).then((res)=>{
          if(res.status === 201){
            console.log("创建成功")
          }
        })
        this.add_visible = false
      },
      //todo
      handleSubmit(postId){
        console.log(value)
        console.log(postId)

      },
    },
    mounted() {
      this.axios.get("/posts/all").then((res)=>{
        console.log(res.status)
        console.log(res.data)
        if(res.status === 201){
          this.data1 = res.data
        }
      })
    }
  }
</script>
