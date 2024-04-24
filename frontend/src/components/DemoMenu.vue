




<template>
  <div>
    <el-aside width="300px">
      <MenuB></MenuB>
  </el-aside>

  </div>
    
    
  </template>

  <script scope>
    import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
  } from '@element-plus/icons-vue'
  import RegisterTravel from "./RegisterTravel.vue"
  import MenuB from "./common/MenuB.vue"
    export default{
      name:"DemoMenu",
      components: {
        MenuB,
  },
      data()
      {
        return {
          isCollapse:true
        }
      },
      FlightSearch(){
        this.$router.push('/query')
      }

    }
  </script>
  


  <style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 600px;
  }
  .layout{
    width: 200px;
    margin-left: 20%;
    height:200px;
  }
  .draw{
    width: 400px;
  }
  </style>