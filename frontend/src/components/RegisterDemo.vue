
<template>
<div>
    <h1 class="layout_head"> 注册界面</h1>
</div>
<div class="column side"></div>
<div>
    <div class="column middle">
        <div class="vertical">
            <div class="horizon">
                <p>旅行社:</p>
                <input class="label_beauty" v-model="travelagency" />
                <p>账号:</p>
                <input class="label_beauty" v-model="account" />
            </div>
            <div class="horizon">
                <p>手机号:</p>
                <input class="label_beauty" v-model="phonenumber" />
            </div>
            <div>
                <div class="vertical">
                    <div class="horizon">
                        <p>密码:</p>
                        <input class="label_beauty" v-model="password" type="password"/>
                    </div>
                    <div class="horizon">
                        <p>请再次输入密码:</p>
                        <input class="label_beauty" v-model="password_sec" type="password" />
                    </div>
                    <button class="button_beauty" @click="register">注册</button>
            </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
    import { ElMessage } from 'element-plus'
    import axios from "axios"
    export default{
        
        name:"RegisterDemo",
        data()
        {
            return {
                travelagency:"",
                account:"",
                phonenumber:"",
                password:"",
                password_sec:"",
            }
        },
        methods: {
        register(){
            var Array = ["travel_name", "account", "phone_number", "password", "password_sec"];
            const formData = new FormData();
            if (this.travelagency == "" || this.account == "" || this.phonenumber == "" || this.password == ""){
                ElMessage.warning('请把表单填写完整');
                return;
            }
            formData.append(Array[0],this.travelagency);
            formData.append(Array[1],this.account);
            formData.append(Array[2],this.phonenumber);
            formData.append(Array[3],this.password);
            if (this.password != this.password_sec){
                ElMessage.warning('输入密码应该一致');
                return
            }
            axios.post("http://127.0.0.1:8000/api/register/", formData,{
            headers:{
              'Content-Type': 'application/json',
            }
            // 其他必要的请求头
        })
            .then(response => {
              // Handle successful login logic
              console.log(response.data)
              if (response.data['status'] === "success") {
                ElMessage.success('注册成功');
                console.log("Login successful:", response.data);
                this.$router.push('/')
              }
              else if (response.data['status'] == 'failed'){
                this.state=true;
                ElMessage.error('注册失败');
                console.log("Login failure:", response.data);
              }
              else if(response.data['status'] == 'Incomplete data')
              {
                ElMessage.warning('请对表单填充完整');
              }
              else if(response.data['status'] == 'Account already exists')
              {
                ElMessage.error('账号已存在');
              }
            }
            )
            .catch(error => {
              // Handle login failure logic
              console.error("Login failed:", error);
            });
        }
    }
    }
</script>