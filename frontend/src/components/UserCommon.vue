<!-- UserProfile.vue -->
<template>
  <el-container>
    <el-aside width="150px"><MenuB/></el-aside>
    <el-main>
      <div>
        <div class="header">
          <div class="page-title">我的主页</div>
        </div>
        
        <div class="user-info">
          <!-- <img src="@/assets/avatar.jpg" alt="Avatar" class="avatar" /> -->
          <div class="welcome-message">
            <p class="greeting">尊敬的{{this.travel_name}}旅行社用户，您好！</p>
          </div>
        </div>
    
        <div class="section-title">我的旅客最近订票信息</div>
        <!-- 在这里添加最近订票信息的内容 -->
        
    
        <div class="input-container">
          <label for="datepicker" class="right-aligned-input">选择日期：</label>
          <input type="date" id="datepicker" v-model="selectedDate">
        </div>
        <!-- <input type="date" v-model="selectedDate" class="right-aligned-input"> -->
        <div v-if="selectedDate" class="right-aligned-input">
          <h2>航班信息 - {{ selectedDate }}</h2>
          <table class="mytable">
            <thead>
              <tr>
                <th>姓名</th>
                <th>身份证号</th>
                <th>航班号</th>
                <th>是否确认订单</th>
              </tr>
            </thead>
            <tbody>
              <!-- 获取的数据 -->
              <!-- <tr v-for="flight in getprofile" :key="flight.flightNumber" @click="buyTicket(flight)" class="flight-row" >  -->
                <tr v-for="info in infos" :key="info.name">
                <td>{{ info.name }}</td>
                <td>{{ info.identify_card }}</td>
                <td>{{ info.flight_number }}</td>
                <td>{{ info.is_ticket }}</td>
                <td>
                  <div v-if="is_delay">
                    <button  @click="showOrders(info) " class="action-button">提醒</button>
                  </div>
                  <div v-else>
                    <button  @click="showOrders(info) " class="action-button">查看购票通知</button>
                  </div>
                </td>
                <td>
                  <button  @click="showBill(info) " class="action-button">查看账单</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
    
        <div class="second-section">
          <div class="section-title">我的常用旅客信息</div>
        </div>
        <div class="right-aligned-input">
          <table class="mytable">
            <thead>
              <tr>
                <th>姓名</th>
                <th>身份证号</th>
                <th>手机号</th>
                <th>性别</th>
                <th>工作单位</th>
              </tr>
            </thead>
            <tbody>
              <!-- 获取的数据 -->
              <!-- <tr v-for="flight in getprofile" :key="flight.flightNumber" @click="buyTicket(flight)" class="flight-row" >  -->
              <tr v-for="personinfo in personinfos" :key="personinfo.name">
                <td>{{ personinfo.name }}</td>
                <td>{{ personinfo.identify_card }}</td>
                <td>{{ personinfo.phone_number }}</td>
                <td>{{ personinfo.sex }}</td>
                <td>{{ personinfo.work }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="showModal" class="modal">
            <div class="modal-content">
              <div class="modal-center">
                <div class="ticket-notification">
                  <div v-if="is_delay">
                    <h3>提示</h3>
                  <p>
                    亲爱的乘客，您的订单已经过期，需要在航班出发前一天取票
                  </p>
                  <!-- <p>
                    取票地点：机场柜台 X 号柜台
                  </p>
                  <p>
                    取票时间：{{ getPreviousDay(selectedDate) }} 航班起飞前 1 天
                  </p> -->
                  </div>
                  <div v-else>
                    <h3>取票通知</h3>
                  <p>
                    亲爱的乘客，您的订单购买成功！请记得在航班起飞前前往取票处取票。
                  </p>
                  <p>
                    取票地点：机场柜台 X 号柜台
                  </p>
                  <p>
                    取票时间：{{ getPreviousDay(selectedDate) }} 航班起飞前 1 天
                  </p>
                  <p class="text-align">
                    您的座位号是 {{selectedInfo.seat_number}}
                  </p>
                  </div>
                  
                </div>
                <div class="modal-buttons">
              
                <button @click="closeModal" class="modal-button confirm-button">确定</button>
                </div>   
              </div>      
            </div>
          </div>
          <div v-if="showModalBill" class="modal">
            <div class="modal-content">
              <div class="modal-center">
                <div class="ticket-bill">
                  <h3>账单</h3>
                  <div class="bill-details">
                    <p><strong>乘客姓名:</strong> {{ selectedInfo.name }}</p>
                    <p><strong>身份证号:</strong> {{ selectedInfo.identify_card }}</p>
                    <p><strong>航班号:</strong> {{ selectedInfo.flight_number }}</p>
                    <p><strong>支付机票金额:</strong> {{ selectedInfo.price }}</p>
                  </div>
                </div>
                <div class="modal-buttons">
                  <button @click="closeModalBill" class="modal-button confirm-button">确定</button>
                </div>   
              </div>      
            </div>
          </div>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
  import MenuB from "./common/MenuB.vue"
  import axios from "axios"
export default {
  name:"UserCommon",
  components:{
    MenuB
  },
  mounted(){
    this.infos = []
    const value = sessionStorage.getItem('travel_name');
    this.travel_name = value
    this.is_delay = true
    axios.post("http://127.0.0.1:8000/api/search_order/", {
                  travel_name:this.travel_name,
                  selectdate:this.selectedDate
                },{
                  headers:{
                    'Content-Type': 'application/json',
                  }
                  // 其他必要的请求头
                    })
      .then(response => {
        for (var i=0;i<response.data.length;i+=1){
          var is_ticket_log = "是"
          if (response.data[i].is_ticket == 'False')
          {
            is_ticket_log = "否"
          }
          this.infos.push({name:response.data[i].name,
            identify_card:response.data[i].identify_card,
            phone_number:response.data[i].phone_number,
            flight_number:response.data[i].flight_number,
            price:response.data[i].price,
            is_ticket:is_ticket_log,
            seat_number:response.data[i].seat_number,
          })
        }
        console.log('this.infps ',this.infos)
        // Handle successful login logic
        
      })
      .catch(error => {
        // Handle login failure logic
        console.error("Login failed:", error);
      });
  },
  data() {
    return {
      nowdate:new Date().toISOString().substr(0, 10),
      is_delay:false,
      selectedDate: new Date().toISOString().substr(0, 10),
      flight:{'travel_name':'2'},
      travel_name:"",
      infos: [ // 航班信息数据
        { name: 'ctn', identify_card: '22221220', flight_number: 'K3208', is_ticket: '是', price: '1000' },
        { name: 'wyt', identify_card: '20230505', flight_number: 'K3208', is_ticket: '否', price: '2000' },
        { name: 'zkr', identify_card: '20231107', flight_number: 'K1478', is_ticket: '是', price: '1500' },
        // 更多航班信息...
      ],
      personinfos: [ // 航班信息数据
        { name: 'ctn', identify_card: '22221220', phone_number: '18888883208', sex: '男' ,work: "学生"},
        { name: 'wyt', identify_card: '20230505', phone_number: '18833333208', sex: '男' ,work: "学生" },
        { name: 'yy', identify_card: '20231109', phone_number: '18866663208', sex: '女' ,work: "学生" },
        // 更多航班信息...
      ],
      showModal: false,
      showModalBill: false,
      selectedInfo: null,
      temp:JSON
    };
  },
  methods: {
    showOrders(info) {
      this.selectedInfo = info;
      this.showModal = true;
    },
    showBill(info) {
      this.selectedInfo = info;
      this.showModalBill = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedInfo = null;
    },
    closeModalBill() {
      this.showModalBill = false;
      this.selectedInfo = null;
    },
    getPreviousDay(dateString) {
      const currentDate = new Date(dateString);
      const previousDay = new Date(currentDate);
      previousDay.setDate(currentDate.getDate() - 1);
      // Format the date to match your requirements
      const formattedDate = this.selectedDate.substr(0, 10);
      return formattedDate;
    },
  },
  computed: {
    getprofile() {
      // 根据选中的日期和旅行社得到姓名、身份证号、航班号、是否确认订单
      return this.flights.filter(flight => flight.from_date === this.selectedDate);
    },
  },
  watch:{
    selectedDate(newdate,olddate){
      axios.post("http://127.0.0.1:8000/api/search_order/", {
                  travel_name:this.travel_name,
                  selectdate:newdate
                },{
                  headers:{
                    'Content-Type': 'application/json',
                  }
                  // 其他必要的请求头
                    })
      .then(response => {
        console.log("search order ",response.data)
        console.log("this.nowdate  ",this.nowdate)
        console.log("this.newdate ",newdate)
        if(newdate>this.nowdate)
        {
          this.is_delay=false;
        }
        else{
          this.is_delay=true;
        }
        this.infos = []
        for (var i=0;i<response.data.length;i+=1){
          var is_ticket_log = "是"
          if (response.data[i].is_ticket == 'False')
          {
            is_ticket_log = "否"
          }
          this.infos.push({name:response.data[i].name,
            identify_card:response.data[i].identify_card,
            phone_number:response.data[i].phone_number,
            flight_number:response.data[i].flight_number,
            is_ticket:is_ticket_log,
            price:response.data[i].price,
            seat_number:response.data[i].seat_number,
          })
        }
        // Handle successful login logic
        
      })
      .catch(error => {
        // Handle login failure logic
        console.error("Login failed:", error);
      });
    }

  }

};
</script>

<style scoped>
/* 在这里添加组件的样式 */
.action-button {
  white-space: nowrap;
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  cursor: pointer;
  border-radius: 10px;
  transform: scale(1); /* Initial scale */
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}
.action-button:hover {
  background-color: #08750e; /* Change the background color on hover */
}
/* 样式化模态框 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

/* 隐藏模态框 */
.modal[style*="display: none"] {
  display: none;
}

.modal-buttons {
  display: flex;
  justify-content: space-between; /* Position buttons at each end */

}
.modal-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%; /* Ensure full height */
}
.modal-button {
  white-space: nowrap;
  margin: 8px;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.3s ease; /* Add a smooth transition effect */
}

.modal-button:hover {
  background-color: #45a049; /* Change the background color on hover */
}

.ticket-notification {
  text-align: left;
}

.ticket-notification h3 {
  color: #4caf50;
  text-align: center
}

.ticket-notification p {
  margin-bottom: 10px;
}
.ticket-bill {
  text-align: left;
}

.ticket-bill h3 {
  color: #4caf50;
  text-align: center;
}

.bill-details {
  margin-top: 10px;
}

.bill-details p {
  margin-bottom: 5px;
}
.header {
  background-color: #4caf50; /* 绿色横条的背景颜色 */
  color: white; /* 绿色横条的文字颜色 */
  padding: 1rem;
}

.page-title {
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  margin-top: 1rem;
}
.mytable{
  border-collapse: collapse;
  width: 89%; 
  margin-top: 10px; 
  font-size: 25px; 
  /* margin-left: 20rem; */
}
.avatar {
  width: 60px;
  height: 60px;
  /* border-radius: 100%; 圆形头像 */
  margin-right: 1rem;
  margin-left: 20rem;
}
.input-container {
  display: flex;
  align-items: center;
}
.welcome-message {
  flex: 1;
  margin-left: 0rem;
}

.greeting {
  font-size: 1.5em; /* 调整字体大小为 1.2 倍（可根据实际需要调整） */
}


.section-title {
  background-color: #4caf50; /* 绿色横条的背景颜色 */
  color: white; /* 绿色横条的文字颜色 */
  padding: 0.5rem;
  margin-top: 1rem;
  margin-left: 20rem;
  font-size: 1.2rem;
}

.second-section .section-title {
  background-color: #4caf50; /* 绿色横条的背景颜色 */
  color: white; /* 绿色横条的文字颜色 */
  padding: 0.5rem;
  margin-top: 5rem; /* 为第二个横条设置较小的上边距 */
  margin-bottom: 3rem;
  font-size: 1.2rem;
}
main .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
    margin-left: 1rem;
  }
.mytable th,.mytable td{
  border: 1px solid #ddd;
  padding: 30px; 
  text-align: left;
}
.flight-row:hover {
  background-color: #f5f5f5; /* 悬停时的背景色 */
  cursor: pointer; /* 鼠标悬停样式为手型 */
}

.right-aligned-input {
  margin-top: 0rem;
  margin-left: 20rem; /* 调整适当的像素值来右移输入框 */
  
}
.right-select-input{
  margin-top: 0rem;
  margin-left: 1rem;
}
/* 其他样式规则... */
</style>
