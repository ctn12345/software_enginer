<template>
  <div class="container">
    <!-- 航班信息部分 -->
    <div class="flight-info">
      <h2>航班信息</h2>
      <div class="flight-detail">
        <p>航班号: {{ flightNumber }} 起飞时间: {{ departureTime }} 到达时间: {{ arrivalTime }}</p>
      </div>
    </div>
    
    <!-- 乘客信息部分 -->
    <div class="contacts">
      <h2>乘客信息</h2>
      <form>
        <div class="horizon">
          <label for="name">名字：</label>
          <input type="text" id="name" v-model="newContact.name" required>
          <label for="idNumber">身份证号：</label>
          <input type="text" id="idNumber" v-model="newContact.idNumber" required>
          <label for="phone_number">电话号码：</label>
          <input type="text" id="phone_number" v-model="newContact.phone_number" required>
        </div>
        <div class="horizon">
          <label for="sex">性别:</label>
          <input type="text" id="sex" v-model="newContact.sex" required>
          <label for="work">工作单位:</label>
          <input type="text" id="work" v-model="newContact.work" required>
        </div>
        <button @click.prevent="addContact" type="button" class="addbutton">添加乘客信息</button>
      </form>
      <!-- 乘客列表 -->
      <h2>乘客列表</h2>
      <select v-model="selectedContacts" size="6" multiple class="contact-list">
        <option v-for="(contact, index) in contacts" :key="index" :value="index">
          {{ contact.name }} - {{ contact.idNumber }} - {{contact.phone_number}}
        </option>
      </select>
      <button @click="bookTickets" class="buttonlay">订票</button>
      
    </div>
    
  </div>
</template>

<script>
import axios from "axios"
import { ElMessage } from 'element-plus'
export default {
  name:"CustomerTicket",
  data() {
    return {
      travel_name: "",
      flightNumber: 'ABC123',
      departureTime: '08:00',
      arrivalTime: '10:00',
      contacts: [],
      flag:false,
      flag_1:false,
      selectedContacts: [], // 存储选中联系人的索引
      newContact: {
        name: '',
        idNumber: '',
        phone_number: '',
        sex: '',
        work:'',
        count:0,
      },
    };
  },
  methods: {
    //加号
    addContact() {
      this.travel_name = sessionStorage.getItem('travel_name');
      // 检查乘客姓名是否已存在于已订票乘客列表中
      console.log("newcontact ",this.travel_name)
      if(this.newContact.name == "" || this.newContact.idNumber == "" || this.newContact.phone_number=="" || this.newContact.sex=="" || this.newContact.work==""){
        ElMessage.error("请将表单填充完整!")
        return;
      }
      this.flag = true
      if(this.flag)
      {
         axios.post("http://127.0.0.1:8000/api/is_ticket_simple/", {
        flight_number:this.flightNumber,
       identify_card:this.newContact.idNumber,
      }, {
          headers: {
      'Content-Type': 'application/json',
              },
      })
      .then(response => {
        if (response.data.status=='success'){
          const isPassengerAdded = this.contacts.some(contact => contact.idNumber === this.newContact.idNumber);
          if ( isPassengerAdded) {
            alert('该乘客已经添加了！');
            this.newContact.name = '';
            this.newContact.idNumber = '';
            this.newContact.phone_number = '';
            this.newContact.work = '';
            this.newContact.sex = '';
            return;
          }
          // 添加联系人信息到联系人列表
          

            axios.post("http://127.0.0.1:8000/api/insert_customer/", {
                        name:this.newContact.name,
                        identify_card:this.newContact.idNumber,
                        phone_number:this.newContact.phone_number,
                        sex:this.newContact.sex,
                        work:this.newContact.work,
                        travel_name:this.travel_name
                },{
                  headers:{
                    'Content-Type': 'application/json',
                  }
                  // 其他必要的请求头
                    })
              .then(response => {
              if (response.data.status == 'success'){
                ElMessage.success("您已经成功添加上!")
                this.contacts.push({ ...this.newContact });
                // 清空表单
                this.newContact.name = '';
                this.newContact.idNumber = '';
                this.newContact.phone_number = '';
                this.newContact.sex = '';
                this.newContact.work = '';
              }else{
                ElMessage.error(response.data.status)
                this.newContact.name = '';
                this.newContact.idNumber = '';
                this.newContact.phone_number = '';
                this.newContact.sex = '';
                this.newContact.work = '';
                return
              }
          })
          .catch(error => {
            console.error("Login failed:", error);
          });
          
        }
        else{
          console.log("failed")
          alert('该乘客已经购买票了！');
          this.newContact.name = '';
          this.newContact.idNumber = '';
          this.newContact.phone_number = '';
          this.newContact.sex = '';
          this.newContact.work = '';
          return;
        }
        console.log("thanks god")
      })
      .catch(error => {
        // 处理登录失败的逻辑，例如显示错误信息
        console.error("Login failed:", error);
      });
      }
     
      // 如果乘客姓名已存在于已订票乘客列表中，则不添加乘客信息
    },
    bookTickets() {
      // 根据选中的联系人进行订票操作
      const selectedPassengers = this.selectedContacts.map(index => this.contacts[index]);
      console.log("selected  ", selectedPassengers)
      if(selectedPassengers.length == 0)
      {
        console.log("kkkk")
        ElMessage.error("你还没选择乘客!")
        return;
      }
      this.flag = true;
        if(this.flag)
      {
        this.flag = false
        for (var choice = 0;choice < selectedPassengers.length; choice += 1)
        {
          axios.post("http://127.0.0.1:8000/api/is_ticket/", {
            flight_number:this.flightNumber,
            identify_card:selectedPassengers[choice].idNumber,
                }, {
                    headers: {
                  'Content-Type': 'application/json',
                    },
          })
          .then(response => {
              if (response.data['status'] == 'success'){
                console.log("selected ",selectedPassengers)
                var newdata = []
                var tem = 0
                for (var contact_index = 0; contact_index < this.contacts.length ; contact_index += 1)
                {
                  for(var choice=0;choice<selectedPassengers.length;choice+=1)
                  {
                    if(this.contacts[contact_index].idNumber == selectedPassengers[choice].idNumber)
                    {
                      tem = 1
                      break
                    }
                  }
                  if (tem == 0)
                  {
                   newdata.push({
                    'name':this.contacts[contact_index].name,
                    'idNumber':this.contacts[contact_index].idNumber,
                    'phone_number':this.contacts[contact_index].phone_number,
                   })
                  }
                  tem = 0
                }
                this.contacts = newdata
                 ElMessage.success("恭喜你订购成功!")
              }
              else{
                console.log('2123000')
                ElMessage.error(response.data['message'])
              }
          })
          .catch(error => {
            // 处理登录失败的逻辑，例如显示错误信息
            console.error("Login failed:", error);
          });
        }
          console.log('选中的乘客信息：', selectedPassengers);
      }
      
      // 执行订票操作，使用 selectedPassengers
     
      // 在这里执行实际的订票操作
      // ...
    },
  },
  mounted(){
    // 航班框 
    const value = sessionStorage.getItem('travel_name');
    this.travel_name = value
    let initalize = this.$route.query.jsonData
    initalize = JSON.parse(initalize)
    this.flightNumber = initalize.flightNumber
    this.departureTime = initalize.from_date + " " + initalize.departureTime
    this.arrivalTime = initalize.arrivalTime
    this.travel_name = initalize.travel_name
    this.flag_1 = true
    if(this.flag_1)
    {
      this.flag_1 = false
      axios.post("http://127.0.0.1:8000/api/get_customers_info/", {
        travel_name:value,
        flight_number:this.flightNumber,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        })
      .then(response => {

        for (var i=0;i<response.data.length;i+=1){
          this.contacts.push({
            'name':response.data[i].name,
            'idNumber':response.data[i].identify_card,
            'phone_number':response.data[i].phone_number,
          })
        }
      })
      .catch(error => {
        // 处理登录失败的逻辑，例如显示错误信息
        console.error("Login failed:", error);
      });
    }
    
}
};
</script>

<style>
  .addbutton{
    margin-left: 20%;
    margin-top: 0%;
    font-size: medium;
    height: 40px;
  }
  .buttonlay{
    margin-left: 45%;
    margin-top: 6%;
    width: 60px;
    height: 40px;
    font-size: larger;
    margin-bottom: 100%;
  }
.flight-info h2,
.contacts h2 {
  text-align: center; /* 让标题居中对齐 */
}
.container {
  display: flex;
  flex-direction: column; /* 从上到下排列 */
  /* 居中对齐 */
  height: 100vh; /* 让容器铺满整个视口高度 */
  width: 500px;
  margin-left: 40%;
  margin-top: 20%;
  align-items: center;
  
  /* padding-top: 150px; */
}
.flight-detail {
  font-size: 30px; /* 修改字体大小 */
}
.contact-list {
  font-size: 24px; /* 调整字体大小 */
  padding: 8px; /* 调整内边距 */
  width: 800px; /* 调整宽度 */
}
.flight-info {
  border: 2px solid #000; /* 添加黑色边框 */
  padding: 20px; /* 添加内边距 */
  margin-bottom: 20px; /* 在航班信息部分底部留出一些空间 */
  border-radius: 10px; /* 添加圆角边框 */
}
.contacts label {
  font-size: 18px; /* 调整标签的字体大小 */
}
.contacts input[type="text"] {
  font-size: 16px; /* 调整输入框的字体大小 */
}
.infinite-list {
  height: 300px;
  padding: 0;
  margin: 0;
  list-style: none;
}
.infinite-list .infinite-list-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  background: var(--el-color-primary-light-9);
  margin: 10px;
  color: var(--el-color-primary);
}
.infinite-list .infinite-list-item + .list-item {
  margin-top: 10px;
}
</style>


