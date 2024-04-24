<template>
  <el-container>
    <el-aside width="100px"><MenuB :paramFromParent="parentData" /></el-aside>
  <div class="centered">
    <div>
      <div class="welcome-message">
        <p>欢迎订购！</p>
      </div>
      <input type="date" v-model="selectedDate">
      <div v-if="selectedDate">
        <h2>航班信息 - {{ selectedDate }}</h2>
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
            <tr v-for="flight in filteredFlights" :key="flight.flightNumber" @click="buyTicket(flight)" class="flight-row">
              <td>{{ flight.flightNumber }}</td>
              <td>{{ flight.origin }}</td>
              <td>{{ flight.destination }}</td>
              <td>{{ flight.departureTime }}</td>
              <td>{{ flight.arrivalTime }}</td>
              <td>{{ flight.price }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</el-container>
</template>

<script>
  import axios from "axios"
  import {store} from "../store/index.js"
  import MenuB from "./common/MenuB.vue"
  import { ElMessage } from 'element-plus'
export default {
  name:"QueryShow",
  components:{
      MenuB,
  },
  data() {
    return {
      selectedDate: new Date().toISOString().substr(0, 10),
      from_location:"",
      destination:"",
      travel_name:"",
      flights: [
        { 
          flightNumber: 'AB123',
          date: '2023-12-20',
          departureTime: '08:00',
          arrivalTime: '10:00',
          price: '$200',
          origin: 'City A', // Add origin information
          destination: 'City B' // Add destination information
        },
        { 
          flightNumber: 'CD456',
          date: '2023-12-20',
          departureTime: '12:00',
          arrivalTime: '14:00',
          price: '$180',
          origin: 'City C', // Add origin information
          destination: 'City D' // Add destination information
        },
        { 
          flightNumber: 'EF789',
          date: '2023-12-21',
          departureTime: '09:30',
          arrivalTime: '11:30',
          price: '$220',
          origin: 'City E', // Add origin information
          destination: 'City F' // Add destination information
        },
        // Add more flights with origin and destination information
      ],
      temp:JSON
    };
  },

  methods: {
    buyTicket(flight) {
      // var nowtime = new Date().toISOString().substr(0, 10)
      // var nowtime_hour = new Date().toISOString().substr(11,13)
      let date = new Date(+new Date() + 8 * 3600 * 1000).toISOString().replace(/T/g, ' ').replace(/\.[\d]{3}Z/, '');
      // let date = "2024-01-02 24:20:23";
      var nowtime = date.split(' ')[0]
      var nowtime_hour = date.split(' ')[1].split(':')[0]
      var minute = date.split(' ')[1].split(':')[1]
      var hour = flight.departureTime.split(':')[0]
      if (nowtime < this.selectedDate){
        var hour_numeric = parseInt(hour)
        var nowtime_hour_numeric = parseInt(nowtime_hour)
        if(hour_numeric == 2024){
          hour_numeric = 0
        }
        if(nowtime_hour=="00"){
          nowtime_hour_numeric=0
        }
        var diff = 24-nowtime_hour_numeric + hour_numeric
        console.log("diff ",diff)
          let flight_buy = flight
        console.log("buyticket ",this.travel_name)
        flight_buy['travel_name'] = this.travel_name
        this.$router.push({path:'/query/query_show/CustomerTicket',
                  query:{
                    jsonData: JSON.stringify(flight_buy)
                  }})
        
      }
      else{
        ElMessage.error("您只能在飞机起飞前一天购买航班!!!")
      }
    },
  },
  mounted(){
      try{
        this.temp = this.$route.query.jsonData;   
        this.temp = JSON.parse(JSON.stringify(this.temp))
        var per_data = JSON.parse(this.temp)
        this.flights = []
        this.selectedDate = per_data[0].from_date.substr(0,10)
        if (per_data[0].status == "success"){
        this.from_location = per_data[0].from_location;
        this.destination = per_data[0].destination;
        this.travel_name = per_data[0].travel_name;
        for (var i=0; i<per_data.length ;i += 1)
        {
          var str_price = '￥'
          str_price = str_price + per_data[i].price
          this.flights.push({flightNumber:per_data[i].flight_number, 
            from_date:per_data[i].from_date.substr(0,10), 
            departureTime:per_data[i].from_date.substr(0,10) + " " + per_data[i].from_date.split(" ")[1].substr(0,5),
            arrivalTime:per_data[i].arrived_date.substr(0,10) + " " + per_data[i].arrived_date.split(" ")[1].substr(0,5),
            origin:per_data[i].from_location,
            destination:per_data[i].destination,
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
      // console.log(typeof newdate);
      // console.log('ososo ',newdate)
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
        
        var per_data = JSON.parse(this.temp)
        if (per_data[0].status == 'not exist'){
          this.flights = []
        }
        else if(per_data[0].status=='success'){
          this.flights = []
          for (var i=0; i<per_data.length ;i += 1)
        {
          var str_price = '￥'
          str_price = str_price + per_data[i].price
          this.flights.push({flightNumber:per_data[i].flight_number, 
            from_date:per_data[i].from_date.substr(0,10), 
            departureTime:per_data[i].from_date.substr(0,10) + " " + per_data[i].from_date.split(" ")[1].substr(0,5),
            arrivalTime:per_data[i].arrived_date.substr(0,10) + " " + per_data[i].arrived_date.split(" ")[1].substr(0,5),
            origin:per_data[i].from_location,
            destination:per_data[i].destination,
          price: str_price})
        }   
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