<!-- UserProfile.vue -->
<template>
  <el-container>
    <el-aside width="150px"><MenuRoot/></el-aside>
    <el-main>
      <div class="tolay">
        <div class="header">
          <div class="page-title">我的主页</div>
        </div>
        
        <div class="user-info">
          <img src="@/assets/avatar.jpg" alt="Avatar" class="avatar" />
          <div class="welcome-message">
            <p class="greeting">尊敬的超级用户，您好！</p>
          </div>
        </div>

        <div class="section-title">最近订票信息</div>
        <!-- 在这里添加最近订票信息的内容 -->
        

        <div class="input-container">
          <label for="datepicker" class="right-aligned-input">选择日期：</label>
          <input type="date" id="datepicker" v-model="selectedDate">
          <p>请选择旅行社名称</p>
          <select v-model="selectedName" class="right-select-input">
            <option v-for="name in statictravelname " :key="name.travel_name"  >{{ name.travel_name }}</option>
            <!-- <option v-for="flight in filteredFlights" :key="flight.travel_name"  >{{ filght.travel_name }}</option> -->
          </select>  
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
                <tr v-for="info in infos" :key="info.identify_card">
                <td>{{ info.name }}</td>
                <td>{{ info.identify_card }}</td>
                <td>{{ info.flight_number }}</td>
                <td>{{ info.is_ticket }}</td>
                <td>
                <!-- 添加按钮，并为按钮绑定点击事件处理函数 -->
                  <button v-if="info.is_ticket === '否'" @click="showConfirmationModal(info) " class="action-button">设置订单</button>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="showModal" class="modal">
            <div class="modal-content">
              <p>{{choose_prompt()}}</p>
              <div class="modal-buttons">
              <button @click="markAsCompleted" class="modal-button confirm-button">是</button>
              <button @click="closeModal" class="modal-button confirm-button">取消</button>
              </div>
            </div>
          </div>
        </div>

        <!-- <div class="second-section">
          <div class="section-title">我的常用旅客信息</div>

        </div> -->
      </div>
</el-main>
</el-container>
</template>

<script>
  import axios from "axios"
  import MenuRoot from './MenuRoot.vue';
export default {
  name:"UserProfile",
  components:{
    MenuRoot,
  },

  data() {
    return {
      selectedDate: new Date().toISOString().substr(0, 10),
      selectedName: null,
      statictravelname:[{travel_name:'黑虎旅行'},{travel_name:'乌喵才旅行'}],
      flight:{'travel_name':'2'},
      infos: [ // 航班信息数据
        // { name: 'ctn', identify_card: '22221220', flight_number: 'K3208', is_ticket: '是' },
        // { name: 'wyt', identify_card: '20230505', flight_number: 'K3208', is_ticket: '否' },
        // { name: 'zkr', identify_card: '20231107', flight_number: 'K1478', is_ticket: '是' },
        // 更多航班信息...
      ],
      showModal: false,
      selectedInfo: null,
      temp:JSON,
      flag:false,
      is_delayed:false
    };
  },
  methods: {
    choose_prompt(){
      if(this.is_delayed)
      {
        return "对不起，请在航班起飞前一天确定订单"
      }
      else{
        return "是否将订单标记为已完成？"
      }
    },
    showConfirmationModal(info) {
      this.selectedInfo = info;
      

      this.showModal = true;
    },
    markAsCompleted() {
      if(this.is_delayed){
        this.closeModal();
        return 
      }
      if (this.selectedInfo) {
        // 在这里执行将订单标记为已完成的操作
        this.selectedInfo.is_ticket = '是';
        

        axios.post("http://127.0.0.1:8000/api/update_is_ticket/",{
                        flight_number:this.selectedInfo.flight_number,
                        identify_card:this.selectedInfo.identify_card,
                        },
                      {headers: {
                                'Content-Type': 'application/json',
                    }})
            .then(response => {
                 console.log('why 0 ',response.data)
            }
            )
            .catch(error => {
              // Handle login failure logic
              console.error("Login failed:", error);
            });

        // 关闭模态框
        this.closeModal();
      }
    },
    closeModal() {
      this.showModal = false;
      this.selectedInfo = null;
    },
  },
  computed: {
    getprofile() {
      // 根据选中的日期和旅行社得到姓名、身份证号、航班号、是否确认订单
      return this.flights.filter(flight => flight.from_date === this.selectedDate);
    },
  },
  mounted(){
   axios.post("http://127.0.0.1:8000/api/get_all_travelname/",{
        })
            .then(response => {
              this.statictravelname = JSON.parse(JSON.stringify(response.data));
              try{
                this.selectedName = this.statictravelname[0]['travel_name'];
              }
              catch(error){
                this.selectedName = []
              }
              // const today = new Date();
              // this.from_date = today;
              var currentTime =new Date().toISOString().substr(0, 10)
              // 使用适当的方法获取年、月、日等信息
              this.flag = true
              if(this.flag)
              {
                console.log(this.selectedName)
                
                console.log("currentTime ",currentTime)
                this.is_delayed = true
                // console.log("this.from_date  ", this.from_date)
                // if (this.from_date <= currentTime){
                //   console.log("enyer  sss")
                //   this.is_delayed = true
                // }
                // else{
                //   this.is_delayed = false
                // }
                axios.post("http://127.0.0.1:8000/api/select_date_travelname/",{
                          from_date:this.from_date,
                          travel_agency_name:this.selectedName
                          },
                        {headers: {
                                  'Content-Type': 'application/json',
                      }})
              .then(response => {
                console.log(response.data)
                this.infos = JSON.parse(JSON.stringify(response.data.data))
                for(var info = 0;info < this.infos.length;info += 1){
                  if (this.infos[info].is_ticket == 0)
                  this.infos[info].is_ticket = "否";
                else
                  this.infos[info].is_ticket = "是"
                }
                this.flag = false;
              }
              )
              .catch(error => {
                console.error("Login failed:", error);
              });
              }
            }
            )
            .catch(error => {
              console.error("Login failed:", error);
            });
          },
    watch: {
      selectedName(newname,oldname){
        axios.post("http://127.0.0.1:8000/api/select_date_travelname/",{
                        from_date:this.selectedDate,
                        travel_agency_name:newname,
                        },
                      {headers: {
                                'Content-Type': 'application/json',
                    }})
            .then(response => {
              console.log('goodluck ',response.data)
              this.infos = JSON.parse(JSON.stringify(response.data.data))
              for(var info = 0;info < this.infos.length;info += 1){
                if (this.infos[info].is_ticket == 0)
                this.infos[info].is_ticket = "否";
              else
                this.infos[info].is_ticket = "是"
              }
            }
            )
            .catch(error => {
              // Handle login failure logic
              console.error("Login failed:", error);
            });
      },
      selectedDate(newdate,olddate){
        console.log('newdate ',newdate)
        var currentDate = new Date().toISOString().substr(0, 10)
        this.selectedDate=newdate
        console.log("typeof ",typeof this.selectedDate)
        if (currentDate >= this.selectedDate){
          console.log("ijn")
          this.is_delayed = true
        }
        else{
          this.is_delayed = false
        }
        this.flag = true
        if(this.flag)
        {
          this.flag = false
          axios.post("http://127.0.0.1:8000/api/select_date_travelname/",{
                        from_date:newdate,
                        travel_agency_name:this.selectedName,
                        },
                      {headers: {
                                'Content-Type': 'application/json',
                    }})
            .then(response => {
              this.infos = JSON.parse(JSON.stringify(response.data.data))
              for(var info = 0;info < this.infos.length;info += 1){
                if (this.infos[info].is_ticket == 0)
                this.infos[info].is_ticket = "否";
              else
                this.infos[info].is_ticket = "是"
              }
            }
            )
            .catch(error => {
              console.error("Login failed:", error);
            });
        }
        
      }
    }
};

</script>

<style scoped>
/* 在这里添加组件的样式 */
.tolay{
  margin-left: 0%;

}
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
  width: 70%; 
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
  margin-top: 15rem; /* 为第二个横条设置较小的上边距 */
  margin-bottom: 20rem;
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
