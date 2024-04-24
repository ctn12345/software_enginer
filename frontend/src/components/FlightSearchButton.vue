<template>
  <button @click="handleClick">
    查 询
  </button>
</template>

<script>
export default {
  name:'FlightSearchButton',
  methods: {
    handleClick() {
      // 在按钮被点击时执行的逻辑
      event.preventDefault();
      this.$emit('click'); // 触发 click 事件，通知父组件
    }
  }
};
</script>

<style scoped>
/* 添加按钮样式，根据需要进行自定义 */
button {
  margin-top: 1.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  background-color: #41b883;
  color: white;
  border: none;
  border-radius: 4px;
}

button:hover {
  background-color: #368c77;
}
</style>
