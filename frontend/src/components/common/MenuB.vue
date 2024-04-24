<template>
  <el-radio-group v-model="isCollapse" style="margin-bottom: 20px" class="isFixed">
    <el-radio-button :label="false">expand</el-radio-button>
    <el-radio-button :label="true">collapse</el-radio-button>
  </el-radio-group>
  <el-menu
    default-active="this.$route.path"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
    :router="true"
    style="margin-top: 50px;"
  >
    <el-menu-item index="/query">
      <el-icon><icon-menu /></el-icon>
      <template #title>航班查询</template>
    </el-menu-item>
    <el-menu-item  index="/UserCommon">
      <el-icon><document /></el-icon>
      <template #title>我的</template>
    </el-menu-item>
  </el-menu>
</template>


<script>
    export default{
      name:"MenuB",
      data()
      {
        return {
          isCollapse:true
        }
      },
      props: {
    // 定义一个名为paramFromParent的prop
    paramFromParent_travel_name: String,
    },
    mycommon(){
      console.log("this is mycommon")
      this.$router.push([{
        path:'/UserCommon',
        query:paramFromParent_travel_name,
      }
      ])

    }
  }
</script>
<style>

  .isFixed{
    position:fixed;
    top:0;
    z-index: 1000;
  }
</style>