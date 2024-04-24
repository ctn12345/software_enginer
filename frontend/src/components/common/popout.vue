<template>
    <div class="popup">
      <div class="popup-content">
        <!-- 弹窗内容 -->
        
        <slot></slot>
        <p class="label_beauty">这是不符合要求的</p>
        <!-- 关闭按钮 -->
        <button :class="button-red" @click="closePopup">确定</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name:"PopOut",
    props: {
      isVisible: Boolean,
    },
    setup(props, { emit }) {
      const closePopup = () => {
        // console.log("cskk  ", props.isVisible)
        emit('close');
      };
  
      return { closePopup };
    },
  };
  </script>
  
  <style scoped>
    .button{
     margin-left: 40px;
     
     color: azure; 

    }
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
  }
  .label_beauty{
    border-color: white;
    text-align: center;
    margin-left: 20px;
    width: 100px;
  }
  </style>
  