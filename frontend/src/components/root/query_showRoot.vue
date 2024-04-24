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
                        <el-button type="default" size="big" style="margin-left: 10px;" @click="showAddFlightModal">+</el-button>
                      </tr>
                    </thead>
                    <tbody>
                      
                        <tr v-for="flight in flights" :key="flight.flightNumber" @click="buyTicket(flight)" @contextmenu.prevent.stop="showContextMenu(flight, $event)" class="flight-row">
                          <td>{{ flight.flightNumber }}</td>
                          <td>{{ this.from_location }}</td>
                          <td>{{ this.destination }}</td>
                          <td>{{ flight.departureTime }}</td>
                          <td>{{ flight.arrivalTime }}</td>
                          <td>{{ flight.price }}</td>
                          <el-button type="default" size="big" style="margin-left: 10px;" @click="showAddFlightModal">+</el-button>
                        </tr>
                        
                    </tbody>
                  </table>
                </el-main>
                </el-container>
              
        
      </div>
    <!-- <button @click="showAddFlightModal">新增航班</button> -->
    <!-- 用于添加新航班的模态框 -->
      <el-dialog :close-on-click-modal="false" v-model="showModal" title="航班信息表" :show-close="false">
        <el-form :model="paramsForm">
          <el-col :span="11">
            <el-form-item label="航班号" label-width="120px">
                <el-input v-model="newFlight.flightNumber" autocomplete="off"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="11">
            <el-form-item label="价格" label-width="120px">
              <el-input v-model="newFlight.price" autocomplete="off"></el-input>
          </el-form-item>
          </el-col>

          <el-form-item label="飞机起点终点">
            <el-col :span="11">
              <el-text class="mx-1" style="text-align: center;">{{this.from_location}}</el-text>
            </el-col>
            <el-col :span="2" class="text-center">
              <span class="text-gray-500">-</span>
            </el-col>
            <el-col :span="11">
              <el-text class="mx-1">{{this.destination}}</el-text>
            </el-col>
          </el-form-item>

            <el-form-item label="航班时间">
              <el-col :span="11">
                <el-date-picker
                  v-model="newFlight.from_date"
                  type="date"
                  placeholder="Pick a date"
                  style="width: 100%"
                />
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">-</span>
              </el-col>
              <el-col :span="11">
                <el-time-picker
                  v-model="newFlight.departureTime"
                  placeholder="Pick a time"
                  style="width: 100%"
                />
              </el-col>

              <el-col :span="11">
                <el-date-picker
                  v-model="newFlight.arrivalDate"
                  type="date"
                  placeholder="Pick a date"
                  style="width: 100%"
                />
              </el-col>
              <el-col :span="2" class="text-center">
                <span class="text-gray-500">-</span>
              </el-col>
              <el-col :span="11">
                <el-time-picker
                  v-model="newFlight.arrivalTime"
                  placeholder="Pick a time"
                  style="width: 100%"
                />
              </el-col>
            </el-form-item>
            <el-form-item label="空余座位数" label-width="120px">
              <el-input v-model="newFlight.available_seat" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="horizon">
            <el-button type="primary" @click="addFlight">确 定</el-button>
            <el-button @click="cancelParams">取 消</el-button>
        </div>
    </el-dialog>
    </div>
  </div>
</el-main>
</el-container>
</template>

<script>
import axios from "axios"
import MenuRoot from "./MenuRoot.vue"
import { ElButton, ElDialog } from 'element-plus'
import { ElMessage } from 'element-plus'
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
      flag:false,
      newFlight: {
      flightNumber: '',
      from_date: '',
      departureTime: '',
      arrivalDate: '',
      arrivalTime:'',
      price: '',
      origin: '',
      destination: '',
    available_seat:''},
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
    cancelParams(){
      this.showModal=false
    },
    buyTicket(flight) {
        // console.log('购买了航班', flight.flightNumber);
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
          console.log("selected flight ",this.selectedFlight)

          console.log("selected flight ",this.flights)
          console.log("selected flight ",this.flights[index],'     ',index)
          axios.post("http://127.0.0.1:8000/api/delete_flight/", {
            flight_number:this.selectedFlight.flightNumber,
            }, {
        headers: {
          'Content-Type': 'application/json',
        },
        })
          .then(response => {
            if (response.data.status == "success"){
              this.flights.splice(index, 1);
              ElMessage.success("成功删除航班")
            }
      })
      .catch(error => {
        // 处理登录失败的逻辑，例如显示错误信息
        console.error("Login failed:", error);
      });
          this.selectedFlight = null;
        }
      }
    },
    showAddFlightModal() {
      console.log('yhis ',this.showModal)
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      // 当关闭模态框时重置newFlight数据
      this.newFlight = {
        flightNumber: '',
      from_date: '',
      departureTime: '',
      arrivalDate: '',
      arrivalTime:'',
      price: '',
      origin: '',
      destination: '',
    available_seat:''
      };
    },
    addFlight() {   
      console.log('from_date ',typeof this.newFlight.from_date)
      if (this.newFlight.flightNumber == "" || this.newFlight.from_date == "" || this.newFlight.departureTime == "" || this.newFlight.arrivalDate == "" || this.newFlight.arrivalTime == ""
      ||this.newFlight.price == "" || this.newFlight.available_seat == "")
      {
        ElMessage.error("请把表单填写完整")
        return;
      }

      const departureTime = new Date(this.newFlight.departureTime);
      const from_date = new Date(this.newFlight.from_date)

      const arrivedate = new Date(this.newFlight.arrivalDate)
      const arrivetime = new Date(this.newFlight.arrivalTime)

      var formattedDate1 = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'Asia/Shanghai',
        hour12:false,
      }).format(departureTime);

      var formattedDate0 = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: 'Asia/Shanghai'
      }).format(from_date);

      var formattedDate2 = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: 'Asia/Shanghai',
        hour12:false,
      }).format(arrivetime);

      var formattedDate3 = new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: 'Asia/Shanghai'
      }).format(arrivedate);

      formattedDate0 = formattedDate0.split('/')
      var from_time = formattedDate0[2] + '-' + formattedDate0[0] + '-' + formattedDate0[1]  + formattedDate1.split(',')[1].substr(0,9)

      formattedDate3 = formattedDate3.split('/')
      var arrived_time = formattedDate3[2] + '-' + formattedDate3[0] + '-' + formattedDate3[1] + formattedDate2.split(',')[1].substr(0,9)



      console.log('from_date ',typeof this.newFlight.from_date)
      console.log('departureTime ',this.newFlight.departureTime)
      console.log('arriveDate ',this.newFlight.arrivalDate)
      console.log('arrivalTime ',this.newFlight.arrivalTime)
      this.flag = true
      // 可以在这个函数将新的信息添加到后端
      if (this.flag)
      {
        this.flag=false
      axios.post("http://127.0.0.1:8000/api/insert_flight/", {
            flight_number:this.newFlight.flightNumber,
            from_date:from_time,
            arrived_date:arrived_time,
            price:this.newFlight.price,
            destination:this.destination,
            from_location:this.from_location,
            available_seat:this.newFlight.available_seat,
            }, {
        headers: {
          'Content-Type': 'application/json',
        },
        })
          .then(response => {
            if (response.data.status == 'success')
            {
              this.showModal=false
              ElMessage.success("恭喜你，成功插入航班!")
              if (from_time.split(' ')[0] == this.selectedDate)
              {
                var ppp = '￥' + this.newFlight.price
                this.flights.push({flightNumber:this.newFlight.flightNumber,  
                        from_date:from_time.split(' ')[0], 
                        departureTime:from_time.split(' ')[1],
                        arrivalTime:arrived_time,
                        origin:this.from_location,
                        destination:this.destination,
                        price: ppp,
                        available_seat:this.newFlight.available_seat,})
              }       
              this.newFlight = {
                                flightNumber: '',
                                from_date: '',
                                departureTime: '',
                                arrivalDate: '',
                                arrivalTime:'',
                                price: '',
                                origin: '',
                                destination: '',
                              available_seat:''
                                };
            }
            else{
              this.newFlight = {
                                flightNumber: '',
                                from_date: '',
                                departureTime: '',
                                arrivalDate: '',
                                arrivalTime:'',
                                price: '',
                                origin: '',
                                destination: '',
                              available_seat:''
                                };
              ElMessage.error(response.data.msg)
            }
      })
      .catch(error => {
        // 处理登录失败的逻辑，例如显示错误信息
        console.error("Login failed:", error);
      });

      // this.closeModal();        //关掉模块框
      }
    }
  },
  mounted(){
      try{
        this.temp = this.$route.query.jsonData;  //    
        this.temp = JSON.parse(JSON.stringify(this.temp))
        var per_data = JSON.parse(this.temp)
        console.log('per data ',per_data)
        this.selectedDate = per_data[0].from_date.substr(0,10)
        // if (per_data[0].status == "success"){
        this.flights = []
        this.from_location = per_data[0].from_location;
        this.destination = per_data[0].destination;
        this.flag = true

        if (this.flag){
          this.flag=false
          axios.post("http://127.0.0.1:8000/api/flight-search/", {
                      from_location: this.from_location,
                      destination: this.destination,
                      departureTime: this.selectedDate,
                    }, {
                headers: {
                  'Content-Type': 'application/json',
                },
                })
              .then(response => {

                this.temp = response.data   

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
                  var str_price = '￥'
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
          var str_price = '￥'
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