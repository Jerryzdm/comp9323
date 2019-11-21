<template>
  <div style="border: #ececec 1px solid;width: 100%;margin: 0 12px;">

    <!--title-->
    <div style="background-color: #ececec;width: 100%;text-align: left;height: 45px">
      <h2 style="padding: 6px 12px 0 12px;color: #484848">Change Your Password</h2>
    </div>
    <a-spin :spinning="spinning" tip="Loading...">
      <!--old password-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Old password</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" name="oldPassword" type="password" v-model="oldPassword"></input>
        </div>
        <div style="clear: left"></div>

      </div>

      <!--new password-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">New password</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" name="newPassword" type="password" v-model="newPassword"></input>
        </div>

        <div style="clear: left"></div>
      </div>

      <!--Confirm  password-->
      <div>
        <div style="width: 30%;float: left; margin-top: 30px;text-align: right;">
          <label class="text-left">Confirm password</label>
        </div>
        <div style="float:left;text-align: left;width: 60%">
          <input class="text-right" type="password" name="confirmPassword" v-model="confirmPassword"></input>
        </div>
        <div style="clear: left"></div>
      </div>


      <a-divider></a-divider>
      <div style="text-align: right;margin-right: 20px">
        <a-button type="danger" :size="size" v-on:click="update_pwd">Update password</a-button>
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
        confirmPassword: '',
        oldPassword: '',
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
      update_pwd() {
        //const userinfo1 = JSON.parse(sessionStorage.getItem('userinfo'))
        if (this.newPassword.length >= 8 && this.confirmPassword.length >= 8 && (this.newPassword === this.confirmPassword)) {
          this.spinning = true
          this.axios.put("/api/user/password", {
            token: Cookies.get('token'),
            old_password: this.oldPassword,
            new_password: this.newPassword,
          }).then((response) => {
            if (response.status === 200) {
              this.$notification["success"]({
                message: 'Success',
                description: 'Congratulations, change password successfully.Please login with new password.',
                duration: 2,
              });
              this.axios.post('/api/logout', {
                token: Cookies.get('token')
              }).then((response) => {
                if (response.status === 200) {
                  Cookies.remove('username')//remove cookies
                  Cookies.remove('user_id')
                  Cookies.remove('email')
                  Cookies.remove('token')
                  sessionStorage.removeItem('userinfo')//remove user information
                  this.username = ''
                  this.$router.push('/')
                } else {
                  console.log(response)
                }
              }).catch(function (e) {
                console.log(e)
              })
            }
            this.spinning = false
          }).catch((e) => {
            this.spinning = false
            this.visible = true
            if (e.response.data["msg"]) {
              this.wrong_msg = e.response.data["msg"]
            } else if (e.response.data['errors']) {
              this.wrong_msg = e.response.data["errors"]
            } else {
              this.wrong_msg = "Bad request"
            }
          })
        } else if (this.oldPassword === '') {
          this.visible = true
          this.wrong_msg = "Old password can not be empty"
        } else if (this.newPassword === '' || this.confirmPassword.length < 8) {
          this.visible = true
          this.wrong_msg = "New password can not be empty or less than 8 characters"
        } else if (this.confirmPassword === '' || this.confirmPassword.length < 8) {
          this.visible = true
          this.wrong_msg = "Confirm password can not be empty or less than 8 characters"
        } else if (this.newPassword !== this.confirmPassword) {
          this.visible = true
          this.wrong_msg = "New password is different from confirm password"
        }
      }
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
