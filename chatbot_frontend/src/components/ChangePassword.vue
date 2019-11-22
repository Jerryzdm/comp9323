<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">

    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Change Your Password</h2>
    </div>
    <a-spin :spinning="spinning" tip="Loading...">
      <!--username-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Username</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" v-model="username" disabled></input>
        </div>
        <div style="clear: left"></div>

      </div>

      <!--new password-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Password</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right"  type="password" v-model="newPassword"></input>
        </div>

        <div style="clear: left"></div>
      </div>

      <!--Faculty-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Faculty</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right"  v-model="faculty"></input>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--User type-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">User type</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right"  v-model="user_type"></input>
        </div>
        <div style="clear: left"></div>
      </div>

      <!--Email-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Email</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right"  v-model="email"></input>
        </div>
        <div style="clear: left"></div>
      </div>


      <a-divider></a-divider>
      <div style="text-align: right;margin-right: 20px">
        <a-button type="danger" :size="size" v-on:click="update_profile">Update profile</a-button>
      </div>
    </a-spin>
    <!--modal to give show wrong message-->
    <a-modal
      title="Wrong message"
      v-model="visible"
      @ok="handleOk">
      <p>{{wrong_msg}}</p>
    </a-modal>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'

  export default {

    data() {
      return {
        newPassword: '',
        username:'',
        faculty:'',
        user_type:'',
        email:'',
        size: 'large',
        visible: false,
        wrong_msg: "",
        spinning: false,
      }
    },
    methods: {
      /*make the modal unvisible*/
      handleOk(e) {
        //console.log(e);
        this.visible = false
      },
      /*update password*/
      update_profile() {
        this.axios.post('/auth/update',{
          'username':this.username,
          'password':this.newPassword,
          'faculty':this.faculty,
          'user_type':this.user_type,
          'email':this.email
        },{
          headers: {
            'Authorization': Cookies.get('access_token')
          }
        }).then((res)=>{
          this.$message.success('Update successfully.')
        })
      },
      get_info(){

        this.axios.get('/auth/users/'+Cookies.get('uid')).then((res)=>{
          let data = res.data
          this.username = data.username
          this.faculty = data.faculty
          this.user_type = data.user_type
          this.email = data.email
          this.newPassword = '123456'
        })
      }
    },
    mounted() {
      this.get_info()
    }
  }
</script>

<style scoped>
  .text-left {
    padding: 0 20px;
    font-size: 16px
  }

  .text-right {
    width: 50%;
    margin-top: 30px;
    height: 40px;
    padding: 8px 10px;
    border: 1px solid #aaa;
    font-size: 16px;
    border-radius: 4px;
  }
</style>
