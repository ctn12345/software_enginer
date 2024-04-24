

<template>
    <!-- 有一个 <header> 元素，包含一个展示 Vue logo 的 <img> 元素和一个使用 HelloWorld 组件的 <div> 元素 -->
  
      
      <el-container>
        <el-aside>
          <MenuRoot></MenuRoot>
        </el-aside>
        <el-main>
    <div class="flightsearch">
      <FlightSearchRoot />
    </div>
  </el-main>
    </el-container>
    
  </template>
  
  <script>
    // 导入了两个组件，HelloWorld 和 TheWelcome
    import FlightSearchRoot from './FlightSearchRoot.vue';
    import MenuRoot from './MenuRoot.vue';
    export default {
      name:"QueryFlightRoot",
      data(){
        return {
          reveive_json:JSON
        }
       
      },
      components: {
        FlightSearchRoot,
        MenuRoot,
      },
     mounted(){
  
     }
    };
  </script>
  
  <style scoped>
  header {
    line-height: 1.5;
  }
  
  .logo {
    display: block;
    margin: 0 auto 2rem;
  }
  
  @media (min-width: 1024px) {
    header {
      display: flex;
      place-items: center;
      padding-right: calc(var(--section-gap) / 2);
    }
  
    .logo {
      margin: 0 2rem 0 0;
    }
  
    main .wrapper {
      display: flex;
      place-items: flex-start;
      flex-wrap: wrap;
      margin-left: 1rem;
    }
    .flightsearch{
      margin-left: 0px;
    }
  }
  </style>
  