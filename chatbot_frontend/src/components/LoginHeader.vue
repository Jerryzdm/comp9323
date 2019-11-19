<template>
  <div>
    <a-row class="btn-header" type="flex" justify="end">
      <a-button v-if="!user_show" class="btn-login" v-on:click="showlogin" :size="size">Log in</a-button>
      <a-button v-if="!user_show" v-on:click="showsignup" :size="size">Sign up</a-button>

      <a-dropdown v-if="user_show">
        <a class="ant-dropdown-link" href="#">
          <!---->
          <img src="../assets/User.png">
          <span v-text="show_username"/>
          <!--<a-icon type="down"/>-->
        </a>
        <a-menu slot="overlay">
          <a-menu-item>
            <a href="javascript:; " v-on:click="myprofile">My profile</a>
          </a-menu-item>
          <a-menu-item>
            <a href="javascript:;" v-on:click="homepage">Homepage</a>
          </a-menu-item>
          <a-menu-item>
            <a href="javascript:;" v-on:click="logout">Log out</a>
          </a-menu-item>
        </a-menu>
      </a-dropdown>
      <a-button  v-on:click="showchatbot" :size="size" style="margin-left: 20px">ChatBot</a-button>
    </a-row>

    <!--login pop-up windows-->
    <a-modal title="Login" v-model="login_visible" @ok="handleLogin" okText="Login" >
      <label>Username</label>
      <a-input size="large" v-model="username"></a-input>
      <label>Password</label>
      <a-input size="large" type="password" v-model="password"></a-input>
    </a-modal>
    <a-modal  v-model="chatbot_visible" @ok="handleClose" okText="Close" footer='' >
    <iframe
      allow="microphone;"
      width="450px"
      height="450px"
      src="https://console.dialogflow.com/api-client/demo/embedded/bc743cc1-7917-475d-bd5e-8260fcf5e126">
    </iframe>
    </a-modal>
    <!--sign up pop-up windows-->
    <a-modal title="Sign up" v-model="signup_visible" @ok="handleSignup" okText="Sign up" >
      <label>Email address</label>
      <a-input size="large" v-model="sign_email"></a-input>
      <label>Username</label>
      <a-input size="large" v-model="sign_username"></a-input>
      <label>Faculty</label>
      <a-input size="large" v-model="sign_faculty"></a-input>
      <label>User_type</label>
      <a-input size="large" v-model="sign_user_type"></a-input>
      <label>Password</label>
      <a-input size="large" type="password" v-model="sign_password"></a-input>
      <label>Confirm Password</label>
      <a-input size="large" type="password" v-model="sign_confirmpassword"></a-input>

    </a-modal>
  </div>
</template>

<script>

  import Cookies from 'js-cookie'

  export default {

    data() {
      return {
        size: 'large',
        username: '',
        show_username:Cookies.get('username'),
        password:'',
        user_show: false,
        login_visible:false,
        signup_visible:false,
        sign_email:'',
        sign_username:'',
        sign_faculty:'',
        sign_user_type:'',
        sign_password:'',
        sign_confirmpassword:'',
        chatbot_visible:false
      }
    },
    methods: {
      /*go to login*/
      showlogin() {
        this.login_visible = true;
      },

      /*go to sign up*/
      showsignup() {
        this.signup_visible = true;
      },

      /*go to home page*/
      homepage() {
        if(this.$route.path !== '/'){
          this.$router.push('/')
        }
      },
      /*logout and clear cookies*/
      logout() {

        Cookies.remove('access_token')//remove cookies
        Cookies.remove('username')
        Cookies.remove('uid')
        this.username = ''
        this.user_show = false
        //sessionStorage.removeItem('userinfo')//remove user information
        if(this.$route.path === '/myprofile'){
          this.$router.push('/')
        }
      },
      /*Determine if it's logged in*/
      isLogin() {
        if (Cookies.get('access_token') ) {
          this.user_show = true
          this.show_username = Cookies.get('username')
        } else {
          this.user_show = false
        }
      },
      /*go to profile page*/
      myprofile() {
        if(this.$route.path !== '/myprofile'){
          this.$router.push('/myprofile')
        }
      },
      showchatbot(){
        this.chatbot_visible = true
      },

      //todo
      handleLogin(){
        this.axios.post("/auth/login",{
          "username":this.username,
          "password":this.password
        }).then((response)=>{
          console.log(this.username)
          if(response.status === 200){
            Cookies.set("access_token",'Bearer '+response.data.access_token)
            Cookies.set("username",this.username)
            Cookies.set("uid",response.data.uid)
            console.log(Cookies.get("access_token"))
            console.log('登陆成功')
            this.user_show = true
            this.show_username = this.username
            this.username = ''
            this.password = ''
          }else{
            this.$message.error('Username or password is wrong!');
            this.username = ''
            this.password = ''
          }
          this.login_visible = false;
        }).catch((e)=>{
          this.$message.error('Username or password is wrong!');
          this.username = ''
          this.password = ''
        })

      },
      //todo
      handleSignup(){
        if(this.sign_password === this.sign_confirmpassword){
          this.axios.post("/auth/signup",{
            "email":this.sign_email,
            "username":this.sign_username,
            "password":this.sign_password,
            "faculty":this.sign_faculty,
            "user_type":this.sign_user_type,
          }).then((res)=>{
            if(res.status === 201){
              console.log("创建成功")
              this.user_show = true
            }
            this.signup_visible = false;
            this.sign_user_type = ''
            this.sign_email = ''
            this.sign_username = ''
            this.sign_password = ''
            this.sign_faculty = ''
            this.sign_confirmpassword = ''
          }).catch((e)=>{
            this.$message.error('Username has been used!');
            this.sign_user_type = ''
            this.sign_email = ''
            this.sign_username = ''
            this.sign_password = ''
            this.sign_faculty = ''
            this.sign_confirmpassword = ''
          })
        }else{
          this.$message.error('Passwords are not same!');
          console.log("password are not same")
          this.sign_user_type = ''
          this.sign_email = ''
          this.sign_username = ''
          this.sign_password = ''
          this.sign_faculty = ''
          this.sign_confirmpassword = ''
        }


      },
      handleClose(){
        this.chatbot_visible = false
      }

    },
    mounted: function () {
      this.isLogin();
      if (Cookies.get('access_token') ) {
        this.user_show = true
        this.show_username = Cookies.get('username')
        console.log('yonghuming'+Cookies.get('username'))
      } else {
        this.user_show = false
      }
    }
  }
</script>

<style scoped>
  .btn-login {
    margin-right: 10px;
  }
</style>
