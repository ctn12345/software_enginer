// import { createStore } from 'vuex'

// export default createStore({
//   state: {
//     travel_name:""
//   },
//   getters: {
//     replaceStateTravel_name(state)=>(travel_name)=>{
//       state.travel_name = travel_name
//     }
//   },
//   mutations: {
//   },
//   actions: {
//   },
//   modules: {
//   }
// })


// store.js
import { reactive } from 'vue'

export const store = reactive({
  travel_name: ""
})
