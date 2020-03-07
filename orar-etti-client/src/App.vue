<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />

    <draggable v-model="myArray" @start="drag=true" @end="drag=false" @choose="onChoose">
      <div class="sortable" v-for="element in myArray" :key="element.id" >
        <strong>{{element.name}}</strong>
        <span>{{element.id}}</span>
      </div>
    </draggable>
    
  </div>
</template>

<script>
import draggable from "vuedraggable";

export default {
  name: "App",
  components: {
    draggable
  },
  methods: {
    onChoose: (evt) => {
      console.log(evt)
    }
  },
  data: () => {
    return {
      myArray: [
        { name: "galer", id: 0 },
        { name: "mihai", id: 1 },
        { name: "matei", id: 2 },
        { name: "masinuta", id: 3 },
        { name: "galer", id: 4 }
      ]
    };
  }
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.sortable {
  width: 120px;
  height: 40px;
  border: 1px solid black;
  cursor: move;

  span {
    float: right;
  }
}
</style>
