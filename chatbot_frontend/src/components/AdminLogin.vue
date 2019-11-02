<template>
  <div style="padding: 100px;background: #ececec">
    <div style="background: #fff;padding: 50px;height:300px">
      <label>Email address</label>
      <a-input size="large" v-model="email"></a-input>
      <label>Password</label>
      <a-input size="large" v-model="password"></a-input>
      <a-button type="primary" icon="login" style="margin-top: 20px" @click="login">Search</a-button>
    </div>

  </div>
</template>

<script>
  export default {
    name: "AdminLogin",
    data(){
      return{
        email:'',
        password:''
      }
    },
    methods:{
      login(){
        if(this.email === "123@qq.com" && this.password ==='123'){
          this.$router.push('/adminhome')
        }
      }
    }
  }
</script>

<style scoped>

</style>
