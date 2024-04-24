<template>
  <el-container>
    <el-aside width="100px"><MenuRoot></MenuRoot></el-aside>
    <el-main>
      <div>
          <div>
            <div class="welcome-message">
              <p>欢迎订购！</p>
            </div>
            <input type="date" v-model="selectedDate">
            <div v-if="selectedDate">
              <h2>航班信息 - {{ selectedDate }}</h2>
              <el-container>
                <el-main>
                  <table class="mytable">
                    <thead>
                      <tr>
                        <th>航班号</th>
                        <th>起始地</th>
                        <th>目的地</th>
                        <th>起飞时间</th>
                        <th>降落时间</th>
                        <th>售价</th>
                      </tr>
                    </thead>
                    <tbody>
                        <tr v-for="flight in filteredFlights" :key="flight.flightNumber" @click="buyTicket(flight)" @contextmenu.prevent.stop="showContextMenu(flight, $event)" class="flight-row">
                          <td>{{ flight.flightNumber }}</td>
                          <td>{{ flight.origin }}</td>
                          <td>{{ flight.destination }}</td>
                          <td>{{ flight.departureTime }}</td>
                          <td>{{ flight.arrivalTime }}</td>
                          <td>{{ flight.price }}</td>
                          <el-button type="default" size="big" style="margin-left: 10px;">+</el-button>
                        </tr>
                    </tbody>
                  </table>
                </el-main>
                <el-aside width="100px">
                  <div class="button_style">
                    <el-button type="default" size="big">+</el-button>
                  </div>
                </el-aside>
                </el-container>
              
        
      </div>
    <!-- <button @click="showAddFlightModal">新增航班</button> -->
    <!-- 用于添加新航班的模态框 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <!-- 航班输入字段 -->
        <input type="text" v-model="newFlight.flightNumber" placeholder="航班号">
        <input type="date" v-model="newFlight.date">
        <input type="text" v-model="newFlight.departureTime" placeholder="起飞时间">
        <input type="text" v-model="newFlight.arrivalTime" placeholder="降落时间">
        <input type="text" v-model="newFlight.price" placeholder="售价">
        <input type="text" v-model="newFlight.origin" placeholder="起始地">
        <input type="text" v-model="newFlight.destination" placeholder="目的地">
        <!-- <el-button type="default">+</el-button> -->
        <!-- 添加或取消按钮 -->
        <!-- <button @click="addFlight">添加航班</button>
        <button @click="closeModal">取消</button> -->
      </div>
    </div>
    </div>
  </div>
</el-main>
</el-container>
</template>

<script>
  import axios from "axios"
  import MenuRoot from "./MenuRoot.vue"
export default {
  name:"QueryShowRoot",
  components:{
      MenuRoot,
  },
  data() {
    return {
      selectedDate: new Date().toISOString().substr(0, 10),
      from_location:"",
      destination:"",
      showModal: false,
      newFlight: {
      flightNumber: '',
      date: '',
      departureTime: '',
      arrivalTime: '',
      price: '',
      origin: '',
      destination: ''},
      flights: [ // 航班信息数据
        { flightNumber: 'AB123', from_date: '2023-12-20', departureTime: '08:00', arrivalTime: '10:00', price: '$200' },
        { flightNumber: 'CD456', from_date: '2023-12-20', departureTime: '12:00', arrivalTime: '14:00', price: '$180' },
        { flightNumber: 'EF789', from_date: '2023-12-21', departureTime: '09:30', arrivalTime: '11:30', price: '$220' },
        // 更多航班信息...
      ],
      temp:JSON,
    };
  },

  methods: {
    buyTicket(flight) {
        console.log('购买了航班', flight.flightNumber);
        // this.$router.push('/buy');                      //在这里实现网页的跳转
      },

      showContextMenu(flight, event) {
        event.preventDefault(); // 阻止默认右键菜单
        this.selectedFlight = flight; // 将选中的航班保存在selectedFlight中
        console.log('真的点击了')
        const confirmDelete = window.confirm(`确认删除航班 ${flight.flightNumber} 吗？`);
        if (confirmDelete) {
            this.deleteSelectedFlight();
        }
    },

      deleteSelectedFlight() {                 //这里处理删除
      if (this.selectedFlight) {
        const index = this.flights.indexOf(this.selectedFlight);
        if (index !== -1) {
          this.flights.splice(index, 1);
          this.selectedFlight = null;
        }
      }
    },
    showAddFlightModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      // 当关闭模态框时重置newFlight数据
      this.newFlight = {
        flightNumber: '',
        date: '',
        departureTime: '',
        arrivalTime: '',
        price: '',
        origin: '',
        destination: ''
      };
    },
    addFlight() {                                          // 可以在这个函数将新的信息添加到后端
      this.flights.push({ ...this.newFlight }); 
      
      
      
      this.closeModal();        //关掉模块框
    }
  },
  mounted(){
    console.log("this is the first mount")
      try{
        this.temp = this.$route.query.jsonData;  // 上衣   
        this.temp = JSON.parse(JSON.stringify(this.temp))
        var per_data = JSON.parse(this.temp)
        console.log('per data ',per_data)
        this.selectedDate = per_data[0].from_date.substr(0,10)
        if (per_data[0].status == "success"){
        this.flights = []
        this.from_location = per_data[0].from_location;
        this.destination = per_data[0].destination;
        for (var i=0; i<per_data.length ;i += 1)
        {
          var str_price = '$'
          str_price = str_price + per_data[i].price
          this.flights.push({flightNumber:per_data[i].flight_number, 
            from_date:per_data[i].from_date.substr(0,10), 
            departureTime:per_data[i].from_date.split(" ")[1].substr(0,5),
            arrivalTime:per_data[i].arrived_date.substr(0,10),
          price: str_price})
        }
      }
      else if(per_data[0].status="not exist")  {
        this.from_location = per_data[0].from_location;
        this.destination = per_data[0].destination;
      }       
      } catch(error){
        console.log("it is wrong")

      }finally{

      } 
    },
  computed: {
    filteredFlights() {
      // 根据选中的日期过滤航班信息
      return this.flights.filter(flight => flight.from_date === this.selectedDate);
    },
  },
  watch:{
  selectedDate(newdate,olddate){
    try{
      console.log(typeof newdate);
      console.log('ososo ',newdate)
      // 发送登录请求到后端
      axios.post("http://127.0.0.1:8000/api/flight-search/", {
        from_location: this.from_location,
        destination: this.destination,
        departureTime: newdate,
      }, {
  headers: {
    'Content-Type': 'application/json',
  },
  })
      .then(response => {
        // 处理登录成功的逻辑，例如保存用户信息到本地存储
        // localStorage.setItem("token", response.data.token);
        // 跳转到其他页面或执行其他操作

        this.temp = response.data   
        // this.temp = JSON.stringify(this.temp)
        
        
        this.temp = JSON.parse(JSON.stringify(JSON.stringify(this.temp)))
        // this.temp = JSON.parse(JSON.stringify(this.temp))
        
        var per_data = JSON.parse(this.temp)
        if (per_data[0].status == 'not exist'){
          this.flights = []
        }
        else if(per_data[0].status=='success'){
          this.flights = []
          for (var i=0; i<per_data.length ;i += 1)
        {
          var str_price = '$'
          str_price = str_price + per_data[i].price
          this.flights.push({flightNumber:per_data[i].flight_number, 
            from_date:per_data[i].from_date.substr(0,10), 
            departureTime:per_data[i].from_date.split(" ")[1].substr(0,5),
            arrivalTime:per_data[i].arrived_date.substr(0,10) + " " +  per_data[i].arrived_date.split(" ")[1].substr(0,5),
            origin:per_data[i].from_location,
            destination:per_data[i].destination,
          price: str_price})
        }   
        console.log("init ", this.flights)
        }
        
      })
      .catch(error => {
        // 处理登录失败的逻辑，例如显示错误信息
        console.error("Login failed:", error);
      });
    }
    catch(error){
      console.log('ssssfdoksakij')
    }
  }
}
};


</script>

<style>

.button_style{
  padding: 0px;
  margin-top: 30%;
  }
.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh; 
}
.welcome-message p {
  font-size: 60px;
  color: #ff0303;
}
.mytable{
  border-collapse: collapse;
  width: 80%; 
  margin-top: 30px; 
  font-size: 30px; 
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
</style>