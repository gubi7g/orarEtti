<template>

  <div id="app">

    <table>
      <thead>
        <tr>
          <th v-for="grupa in ['', ...grupe]" :key="grupa.key">{{grupa}}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ora, ind_ora) in ore" v-bind:key="ora.id">
          <template v-for="grupa in ['', ...grupe]">
            <td v-if="grupa == ''" v-bind:key="grupa.id">{{ore[ind_ora]}}</td>
            <td v-else v-bind:key="grupa.id">haha</td>
          </template>
          
        </tr>
      </tbody>

    </table>
  </div>
</template>

<script>


export default {
  name: "App",
  components: {
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
      ],
      grupe: ['432A', '432B', '432C', '432D', '432E', '432F'],
      ore: ['08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21']
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

.orar {
    display: inline-block;
    flex-basis: 0;
    flex-grow: 1;
    max-width: 100%;
    // display: flex;
    position: relative;
    box-sizing: border-box;
    vertical-align: inherit;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
}

.title {
  flex: 0 0 100%;
  max-width: 100%;
}
</style>
