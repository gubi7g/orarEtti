<template>
  <div id="app">
    <h1>Orar ETTI</h1>

    <img id="ettigif" src="./assets/logo.gif" width="100" />
    <!-- <h1>{{createSerii}}</h1> -->
    <img id="vuelogo" src="./assets/logo.png" width="100" />
    <p>Clicked: {{clickCell()}}</p>
    <h3>Selected Year: {{selectedYear}}</h3>
    <b-row>

      <b-col><b-button @click.stop="selectedYear = 1">An 1</b-button></b-col>
      <b-col><b-button @click.stop="selectedYear = 2">An 2</b-button></b-col>
      <b-col><b-button @click.stop="selectedYear = 3">An 3</b-button></b-col>
      <b-col><b-button @click.stop="selectedYear = 4">An 4</b-button></b-col>
    </b-row>
    <b-row>

      <table class="orar">
        <thead>
          <tr>
            <th v-for="grupa in ['', ...grupeArray]" :key="grupa.key">{{grupa}}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ora, ind_ora) in ore" v-bind:key="ora.id">
            <template v-for="grupa in ['', ...grupeArray]">
              <td v-if="grupa == ''" v-bind:key="grupa.id">{{ore[ind_ora]}}</td>
              <td v-else v-bind:key="grupa.id" :id="grupa + ora.split('-').join('')" :class="createSelectedClass(grupa + ora.split('-').join('')).includes() ? 'selected' : ''"></td>
            </template>
          </tr>
        </tbody>
      </table>
    </b-row>
    <b-row>
      <b-col>
        <h1>Edit your course</h1>

        <h3>Course:</h3>

        <b-form-select
          v-model="selectedCourse"
          id="dropdown-courses"
          class="mt-3"
          :options="availableCourses"
        ></b-form-select>
        <h3>Day:</h3>
        <b-form-select v-model="selectedDay" id="dropdown-days" class="mt-3" :options="dotw"></b-form-select>
        <h3>Start Time:</h3>
        <b-form-input type="time"></b-form-input>
        <h3>End Time:</h3>
        <b-form-input type="time"></b-form-input>
      </b-col>
      <b-col>
        <h1>Please select groups/series:</h1>
        <b-form-group id="checkbox-serie" text="Courses" class="m-md-2">
          <b-form-checkbox
            v-model="allGroupsSelected"
            :indeterminate="indeterminate"
            @change="toggleAllGroups"
          >{{ allGroupsSelected ? 'Un-select all ' : 'Select all ' }}</b-form-checkbox>

          <b-form-checkbox-group v-model="selectedGroups" :options="grupeArray"></b-form-checkbox-group>
        </b-form-group>
        <div>
          Selected:
          <strong>{{ selectedGroups }}</strong>
          <br />All Selected:
          <strong>{{ allGroupsSelected }}</strong>
          <br />Indeterminate:
          <strong>{{ indeterminate }}</strong>
        </div>
        <div>selected start time: {{this.selectedTimeInt.substr(0,2)}}</div>
        <div>selected class: {{createSelectedClass()}}</div>
      </b-col>
    </b-row>

    <!-- <p>{{this.serii}}</p> -->
  </div>
</template>

<script>
const config = require("./config.json");

export default {
  name: "App",
  components: {},
  computed: {},
  methods: {
    fetchGroups: function(an) {
      console.log(config.api.groups);
      this.$http.get(config.api.groups + `/${an}/`).then(result => {
        this.grupeArray = []

        this.grupe = result.data;
        console.log("groups from api: ", this.grupe);
        for (const grupa of this.grupe) {
          this.grupeArray.push(grupa.name);
        }
        console.log(this.grupeArray);
      });
    },


    createSelectedClass: function() {
      let x = ""
      this.selectedGroups.forEach(group => {
        x += '#' + group + this.selectedTimeInt + ','
      })
      return x
    },
    
    clickCell() {
      window.onclick = e => {
        console.log(e.target.id);

        if(/^4[1-4]\d[A-G](a|b|)\d{4}$/.test(e.target.id)){
          let clickedGroupName
          if(e.target.id.length == 9){
            clickedGroupName = e.target.id.substr(0, 5)
            
          } else if (e.target.id.length == 8){
            clickedGroupName = e.target.id.substr(0, 4)

          }
          else{
            return console.log('error on click group name length')
          }

          console.log(clickedGroupName)
          if(this.selectedGroups.includes(clickedGroupName)){
            console.log(this.selectedGroups[this.selectedGroups.indexOf(clickedGroupName)].substr(e.target.id.length-4, e.target.id.length))
            if (e.target.id.substr(e.target.id.length-4, e.target.id.length) == this.selectedTimeInt){ // daca este acelasi interval selectat, sterge-l din selectate
              this.selectedGroups.splice(this.selectedGroups.indexOf(clickedGroupName), 1)
            }
            else {
              //pass
            }
          }
          else{
            console.log('added new group to selected')
            this.selectedGroups.push(clickedGroupName)
          }
          this.selectedTimeInt = e.target.id.substr(e.target.id.length-4, e.target.id.length)
        }

        return e.target.id;

      };
    },
    toggleAllGroups(checked) {
      this.selectedGroups = checked ? this.grupeArray.slice() : [];
    }
  },
  created: function() {
    this.fetchGroups(this.selectedYear);
    console.log("created!");

  },
  data: () => {
    return {
      grupe: [],
      grupeArray: [],
      ore: [
        "08-09",
        "09-10",
        "10-11",
        "11-12",
        "12-13",
        "13-14",
        "14-15",
        "15-16",
        "16-17",
        "17-18",
        "18-19",
        "19-20",
        "20-21"
      ],
      dotw: [
        { value: null, text: "Please select a day", disabled: true },
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      selectedDay: null,
      selectedGroups: [],
      allGroupsSelected: false,
      indeterminate: false,
      selectedCourse: null,
      availableCourses: [
        { value: null, text: "Please select a course", disabled: true },
        { value: "am2", text: "Analiza Matematica 2 - Seria G", left: 5 }
      ],
      currentSerie: {},
      selectedTimeInt: "",
      selectedYear: 1,
      selectedGroupsIds: [],
      selectedClass: ''
    };
  },
  watch: {
    selectedGroups(newVal) {
      // Handle changes in individual flavour checkboxes
      if (newVal.length === 0) {
        this.indeterminate = false;
        this.allGroupsSelected = false;
      } else if (newVal.length === this.grupeArray.length) {
        this.indeterminate = false;
        this.allGroupsSelected = true;
      } else {
        this.indeterminate = true;
        this.allGroupsSelected = false;
      }
    },
    selectedYear(val) {
      this.fetchGroups(val)
    }
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

.title {
  flex: 0 0 100%;
  max-width: 100%;
}

table {
  // overflow: scroll;
  display: block;
  max-width: 100%;
  overflow-x: scroll;

}
td {
  border: 1px solid black;
  min-width: 200px;
  height: 40px;
}

#vuelogo {
  position: absolute;
  top: 0px;
  left: 0px;
}

this.selectedClass {
  background: black;
}
</style>
