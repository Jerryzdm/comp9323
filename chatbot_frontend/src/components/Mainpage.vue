<template>
  <div>
    <div style="margin-left: 5%;margin-right: 5%;margin-top: -50px">
      <login-header style="float: right;width: 50%;"></login-header>
      <!--to clear the float-->
      <div style="clear: both"></div>
    </div>

    <div style="margin-top: 20px">
      <a-layout>
        <a-layout-content style="padding: 50px 100px">
          <a-layout style="padding: 24px 0; background: #fff">
            <a-layout-sider width="200" style="background: #fff">
              <a-menu
                mode="inline"
                :defaultSelectedKeys="['1']"
                style="height: 100%"
                onclick={this.onclick.bind(this)}
              >
                <a-menu-item key="1" @click="changepage('News')">News</a-menu-item>
                <a-menu-item key="2" @click="changepage('Post')">Post</a-menu-item>
                <a-menu-item key="3" @click="changepage('Course')">Course</a-menu-item>
              </a-menu>
            </a-layout-sider>
            <a-layout-content :style="{minHeight: '500px' }" :is="currentPage"></a-layout-content>
          </a-layout>
        </a-layout-content>

      </a-layout>
    </div>
    <div class="float-button" @click="showchatbot">
      <img src="../assets/icon-chatbot.png">
    </div>

    <!--chatbot modal-->
    <a-modal v-model="chatbot_visible" @ok="handleClose" okText="Close" footer='' style="margin-top: 10px">
      <!--<iframe
        allow="microphone;"
        width="450px"
        height="450px"
        src="https://console.dialogflow.com/api-client/demo/embedded/bc743cc1-7917-475d-bd5e-8260fcf5e126">
      </iframe>-->
      <template>
      <div class="talk_con" style="overflow: auto;">
        <div class="talk_show" id="words" >
          <div class="atalk"><span id="asay">Hello</span></div>
        </div>
        <div class="talk_input">
          <input type="text" class="talk_word" id="talkwords" v-model="inputVal" @keyup.enter="send">
          <input type="button" value="send"  class="talk_sub" id="talksub" @click="send"  >
        </div>
      </div>
      </template>
    </a-modal>

  </div>
</template>

<script>
  import News from "./News"
  import Post from "./Post"
  import Course from "./Course"
  import LoginHeader from "./../components/LoginHeader"

  export default {
    components: {News, Post, Course, LoginHeader},
    methods: {
      changepage(page) {
        this.currentPage = page
      },
      showchatbot() {
        this.chatbot_visible = true
      },
      //close the chatbot
      handleClose() {
        this.chatbot_visible = false
      },
      send(){
        {

          var Words = document.getElementById("words");
          var Who = document.getElementById("who");
          var TalkWords = document.getElementById("talkwords");
          var TalkSub = document.getElementById("talksub");
          var str = "";
          var message = TalkWords.value
          if(message == ""){
            this.$message.warning("Message can not be empty");
            return;
          }

           /* str = '<div class="atalk"><span id="asay">A说 :' + message +'</span></div>';*/

          str = "<div class='btalk' style='margin:10px 10px 10px 50px;\n" +
            "    text-align:right;'><span id='bsay' style='display:inline-block;\n" +
            "    background:#ef8201;\n" +
            "    border-radius:10px;\n" +
            "    color:#fff;\n" +
            "    padding:5px 10px;'>" + message +"</span></div>" ;
          Words.innerHTML = Words.innerHTML + str;
          Words.scrollTop = Words.scrollHeight;
          this.axios.get('https://9323forward.localtunnel.me/forward',{
          //this.axios.get('http://127.0.0.1:4000/forward',{
            params:{
              'Text':message
            }
          }).then((res)=>{
            let responsemessage = res.data.fulfillment_text
            str = '<div class="atalk" style="margin:10px 50px 10px 10px;"><span id="asay" style="display:inline-block;\n' +
              '    background:#0181cc;\n' +
              '    border-radius:10px;\n' +
              '    color:#fff;\n' +
              '    padding:5px 10px;">' + responsemessage +'</span></div>';

            Words.innerHTML = Words.innerHTML + str;
            Words.scrollTop = Words.scrollHeight;
            this.inputVal = ''

          })
          this.inputVal = ''
        }
      }

    },

    data() {
      return {
        currentPage: News,
        News: News,
        Post: Post,
        Course: Course,
        chatbot_visible: false,
        inputVal:''

      }
    },

  }
</script>

<style scoped>
  .float-button {
    position: fixed;
    height: 90px;
    width: 40px;
    bottom: 90px;
    right: 50px;

  }
  .talk_con{
    width:450px;
    height:450px;
    border:1px solid #666;
    margin:50px auto 0;
    background:#f9f9f9;
  }
  .talk_show{
    width:430px;
    height:370px;
    border:1px solid #666;
    background:#fff;
    margin:10px auto 0;
    overflow:auto;
  }
  .talk_input{
    width:430px;
    margin:10px auto 0;
  }
  .whotalk{
    width:80px;
    height:30px;
    float:left;
    outline:none;
  }
  .talk_word{
    width:330px;
    height:26px;
    padding:0px;
    float:left;
    margin-left:10px;
    outline:none;
    text-indent:10px;
  }
  .talk_sub{
    width:56px;
    height:30px;
    float:left;
    margin-left:10px;
  }
  .atalk{
    margin:10px 50px 10px 10px;
    width:348px;
  }
  .atalk span{
    display:inline-block;
    background:#0181cc;
    border-radius:10px;
    color:#fff;
    padding:5px 10px;
  }
  .btalk{
    margin:10px 10px 10px 50px;
    text-align:right;
    width:348px;
  }
  .btalk span{
    display:inline-block;
    background:#ef8201;
    border-radius:10px;
    color:#fff;
    padding:5px 10px;
  }

</style>
