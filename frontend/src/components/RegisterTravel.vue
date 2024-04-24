
<style>
    .column {
    float: left;
    padding: 70px;
}
    .column_side {
  width: 25%;
}
    .label_beauty{
    border: 0.1px solid rgb(235, 215, 215);
    /* padding:10px 10px;  */
    background:#00000000;
    width:80px;
    height:20px;
    border-radius:0px;
    margin-right: 10px;
    margin-top: 15px;
    }
    .button_beauty{
    border: 0.2px solid blacrgb(255, 255, 255);
    border-radius: 10px;
    background: #4fe3d4;
    width: 60px;
    height: 30px;  
    }
    .column.middle{
    width: 30%;
    background-color: rgb(246, 241, 241);
    }
    .layout_head{
    padding: 20px;
    text-align: center;
    }
    .column.side {
    width: 25%;
}
</style>
<!-- 手机号、账号、密码、旅行社 -->
<template>
    <RegisterDemo></RegisterDemo>
</template>
<script>

    import RegisterDemo from "./RegisterDemo.vue"
    
    export default{
        name:"RegisterTravel",
        components:{
            RegisterDemo,
        },

}
</script>

