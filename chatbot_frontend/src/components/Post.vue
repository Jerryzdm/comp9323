<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">
    <!--The post-->
    <div style="background-color: #ececec;height: 45px;width: 100%;text-align: left">
      <h2 style="padding: 6px 12px 0 12px;color: #484848;width: 90%;float: left">Post</h2>
      <a-icon type="plus-circle" style="width: 10%;font-size: 40px" @click="addPost"/>
    </div>

    <div style="text-align: left">
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
        :dataSource="postdata"
      >
        <a-list-item slot="renderItem" slot-scope="item, index" @click="post_detail(index)" style="text-align: left">
          <p slot="actions">{{item.date|dateformat('YYYY-MM-DD HH:mm')}}</p>
          <a-list-item-meta
            :description="item.content"
          >
            <a slot="title" style="font-size: 16px;font-weight: bold">{{item.title}}</a>
          </a-list-item-meta>

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
    </a-modal>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'
  const postdata = []
  const dataildata = {}

  export default {
    data(){
      return{
        postdata,
        postdata_tmp:[],
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
        addtag:['Movies'],
        review:'',
        all_review:[]

      }
    },
    methods:{
      post_detail(index){
        this.dataildata = this.postdata[index]
        this.axios.get("/comments/"+this.dataildata.postId).then((res)=>{
          if(res.status === 200){
            this.all_review = res.data
          }
          console.log(this.all_review)
        })
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
        if(this.selectedTags.length === 0){
          this.postdata = this.postdata_tmp
        }else{
          this.axios.post("/posts/tags",{
            "tags":this.selectedTags
          }).then((res)=>{
            if(res.status === 201){
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

      addPost(){
        if(Cookies.get('access_token')){
          this.add_visible = true
        }else {
          this.$message.warning('You haven\'t logged in yet!Please log in!');
        }
      },
      //todo
      handleaddOk(){
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
            this.axios.get("/posts/all").then((res)=>{
              console.log(res.status)
              console.log(res.data)
              if(res.status === 201){
                this.postdata = res.data
                this.postdata_tmp = res.data
                this.add_visible = false
              }
            })
          }
        })


      },
      //todo
      handleSubmit(postId){
        console.log(this.review)
        console.log(postId)
        this.axios.post("/comments",{
          "content":this.review,
          "reply_to":postId
        },
          {
            headers:{
              'Authorization':Cookies.get('access_token')
            }
          }).then((res)=>{
            if(res.status === 201){
              this.$message.success('Post successfully!');
              console.log("评论成功")
              this.review = ''
              this.post_visible = false
            }else {
              this.$message.error('Post failure!');
              this.post_visible = false
            }
        }).catch((e)=>{
          this.$message.error('Post failure!You should login first.');
          this.post_visible = false
        })

      },
    },
    mounted() {
      this.axios.get("/posts/all").then((res)=>{
        if(res.status === 201){
          this.postdata = res.data
          this.postdata_tmp = res.data
        }
      })
    }
  }
</script>
