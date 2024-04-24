<script setup>
  import FlightSearchButtonRoot from './FlightSearchButtonRoot.vue'
  </script>
  
  <template>
    <div>
      <div>
        <h2>机票查询</h2>
      </div>
      <form>
        <label for="from_location">出发城市：</label>
        <input type="text" id="from_location" v-model="from_location" placeholder="请输入出发城市" />
  
        <label for="destination">到达城市：</label>
        <input type="text" id="destination" v-model="destination" placeholder="请输入到达城市" />
  
        <label for="departureTime">出发时间：</label>
        <input type="date" id="departureTime" v-model="departureTime" />
  
        <FlightSearchButtonRoot @click="handleSearch" />
      </form>
    </div>
  </template>
  
  <script>
    import axios from "axios"
export default {
  name:'FlightSearchRoot',
  data() {
    return {
      is_submiting:false,
      from_location: '',
      destination: '',
      departureTime: '',
    };
  },
  components:{
  },
  methods: {
    async handleSearch() {
      // 延时操作
      // await new Promise(resolve => setTimeout(resolve, 2000));
      if (this.isSubmitting) {
      return; // 防止重复提交
    }
    this.isSubmitting = true;

    const formattedDate = new Date(this.departureTime).toISOString();
    console.log("Before");
    console.log("格式化 Date:", formattedDate);
    console.log("After");
    
      // 发送登录请求到后端
      axios.post("http://127.0.0.1:8000/api/flight-search/", {
        from_location: this.from_location,
        destination: this.destination,
        departureTime: formattedDate,
      }, {
  headers: {
    'Content-Type': 'application/json',
  },
  })
      .then(response => {
        // 处理登录成功的逻辑，例如保存用户信息到本地存储
        // localStorage.setItem("token", response.data.token);
        // 跳转到其他页面或执行其他操作

          this.$router.push({path:'/queryRoot/query_showRoot',
                query:{
                  jsonData: JSON.stringify(response.data),
                }})
      })
      .catch(error => {
        // 处理登录失败的逻辑，例如显示错误信息
        console.error("Login failed:", error);
      });
    },
  },

};
</script>

  
  <style scoped>

  /* 如果需要，可以添加自定义样式 */
  h2 {
    font-size: 2.5rem; /* 设置标题的字体大小 */
    color: #1c1b1b; /* 设置标题的文字颜色 */
    margin-bottom: 1rem; /* 设置标题与下方表单的间距 */
    text-align: left;
    margin-left: 30%;
  }
  form {
    display: flex;
    flex-direction: column;
    max-width: 300px;
    margin-left: 25%;
  }
  
  label {
    margin-top: 1rem;
  }
  </style>