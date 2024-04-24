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
      <el-menu-item index="/queryRoot">
        <el-icon><icon-menu /></el-icon>
        <template #title>航班查询</template>
      </el-menu-item>
      <el-menu-item index="/UserProfile">
        <el-icon><document /></el-icon>
        <template #title>我的</template>
      </el-menu-item>
    </el-menu>
</template>


<script>
export default{
name:"MenuRoot",
data()
{
return {
isCollapse:true
}
},
}
</script>
<style>

.isFixed{
position:fixed;
top:0;
z-index: 1000;
}
</style>