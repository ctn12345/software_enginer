<script setup>
      import PopOut from "./common/popout.vue"
</script>
<style>
  body, html {
      height: 100%;
      margin: 0;
      font-family: Arial, sans-serif;
    }
  .centered {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh; 
}

.container {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      width: 100vh;
      size:0cqmax
    }
.horizon{
    /* display: contents;
    flex-direction: column; */
    display: flex;
    margin-bottom: 20px;
    flex-direction: row;
    max-width: 800px;
    width: 100%;
  }
.font{
    display: flex;
    align-items: center;

  }
.middle{
    display: flex;
  }
.total_layout{
    background-color: rgb(246, 241, 241);
    width: 500px;
    border: 1px solid rgb(94, 242, 94);
    padding: 55px;
    margin: 6%;
    border-style:dotted;
    margin-left: 30%;
    margin-top: 10%;
  }
  button{
  margin-top: 20%;
  margin-right: 60%;
}
.component_lay{
  margin-top: 10%;
  margin-left:30%;
  width: 500px;
}
</style>


<template>
  <div>
      <div class="total_layout" id="container">
        <div class="component_lay">
        <header>
          <!-- <div v-if="state"><PopOut isVisible=false @close="handle_failure"></PopOut> </div> -->
          <h1 style="display: block;">机票预订系统</h1>
        </header>
        <div>
            <div class="horizon">
            <label class="font" id="account"> 账号</label>
            <input v-model="user" placeholder="account"/>
            </div>
            <div class="horizon">
              <label class="font" id="password"> 密码</label>
              <input v-model="pwd"  placeholder="password" type="password"/>
            </div>
            <el-checkbox v-model="is_admin" label="是否为管理员" size="large" />
            <div class="horizon">
              <div class="bref">
                <a href="/register" target="_blank" r="l">有账号吗?没有点击注册</a>
              </div>
              <el-button class="button" @click="login" type="primary">登录</el-button>
            </div>
        </div>
      </div>     
      </div>
  </div>
</template>

<script>
    import axios from "axios"
    import {store} from "../store/index.js"
    import { ElMessage } from 'element-plus'

    export default{
      name:"LoginUi",
      data(){
        return{
        user:12312412,
        pwd:"123",
        state:false,
        is_admin:false,
        }
      },
    methods: {
        // Boolean is_submitting = falses
        handle_failure(){
          console.log("it is error!");
          this.state=false
        },
        login() {
          // Create form data
          console.log("login ",this.user);
          const formData = new FormData();
          formData.append('username', this.user);
          formData.append('password', this.pwd);
          formData.append('is_root',this.is_admin)
          console.log("login ",formData);
          // Send login request to the backend
          axios.post("http://127.0.0.1:8000/api/login/", formData,{
            headers:{
              'Content-Type': 'application/json',
            }
            // 其他必要的请求头
        })
            .then(response => {
              // Handle successful login logic
              console.log(response.data)
              if (response.data['status'] === "success") {
                ElMessage.success('登录成功');
                console.log("Login successful:", response.data);
                if(this.is_admin == false)
                {
                  sessionStorage.setItem('travel_name', response.data.travel_name);
                  // store.travel_name = response.data.travel_name
                  this.$router.push({path:'/query',
                query:{
                  jsonData: JSON.stringify(response.data)
                }})
                }
                else{
                  this.$router.push({path:'/queryRoot',
                query:{
                  jsonData: JSON.stringify(response.data)
                }})
                }
                
              }
              else if (response.data['status'] == 'failed'){
                this.state=true;
                ElMessage.error(response.data['message']);
              }
            })
            .catch(error => {
              // Handle login failure logic
              console.error("Login failed:", error);
            });
        },
      },
    };
    </script>