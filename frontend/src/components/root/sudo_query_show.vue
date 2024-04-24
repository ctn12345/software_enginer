<template>
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
              <tr v-for="flight in filteredFlights" :key="flight.flightNumber" @click="buyTicket(flight)" @contextmenu.prevent.stop="showContextMenu(flight, $event)" class="flight-row">
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
      <button @click="showAddFlightModal">新增航班</button>
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
          <!-- <input type="text" v-model="newFlight.destination" placeholder="目的地"> -->
          <!-- 添加或取消按钮 -->
          <!-- <button @click="addFlight">添加航班</button> -->
          <!-- <button @click="closeModal">取消</button> -->
        </div>
      </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        showModal: false,
        newFlight: {
        flightNumber: '',
        date: '',
        departureTime: '',
        arrivalTime: '',
        price: '',
        origin: '',
        destination: ''},

        selectedDate: new Date().toISOString().substr(0, 10),
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
        ]
      };
    },
    methods: {
      buyTicket(flight) {
        console.log('购买了航班', flight.flightNumber);
        this.$router.push('/buy');                      //在这里实现网页的跳转
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
    addFlight() {
                                                        // 可以在这个函数将新的信息添加到后端
      this.flights.push({ ...this.newFlight });       
      this.closeModal();        //关掉模块框
    }
  },
    computed: {
      filteredFlights() {
        // 根据选中的日期过滤航班信息
        return this.flights.filter(flight => flight.date === this.selectedDate);
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
    white-space: nowrap;
    animation: marquee 10s linear infinite; /* 根据需要调整时间和动画 */
  }
  
  .mytable{
    border-collapse: collapse;
    width: 80%; 
    margin-top: 30px; 
    font-size: 24px; 
  }
  .mytable th,.mytable td{
    border: 1px solid #ddd;
    padding: 30px; 
    text-align: left;
    white-space: nowrap; /* 防止文字换行 */
  }
  .flight-row:hover {
    background-color: #f5f5f5; /* 悬停时的背景色 */
    cursor: pointer; /* 鼠标悬停样式为手型 */
  }
  @keyframes marquee {
    from {
      transform: translateX(100%);
    }
    to {
      transform: translateX(-100%);
    }
  }
  .modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 60%;
}

/* 模态框内容和关闭按钮的样式（根据需要调整） */
input, button {
  margin: 5px;
}
  </style>