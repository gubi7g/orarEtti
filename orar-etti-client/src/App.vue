<template>
  <div id="app">
    <h1>Orar ETTI</h1>

    <img id="ettigif" src="./assets/logo.gif" width="100" />
    <!-- <h1>{{createSerii}}</h1> -->
    <img id="vuelogo" src="./assets/logo.png" width="100" />
      <p>Clicked: {{clickElem()}}</p>

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
              <td v-else v-bind:key="grupa.id" :id="grupa + ora.split('-').join('')"></td>
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

          <b-form-checkbox-group v-model="selectedGroups" :options="currentSerie.grupe"></b-form-checkbox-group>
        </b-form-group>
        <div>
          Selected:
          <strong>{{ selectedGroups }}</strong>
          <br />All Selected:
          <strong>{{ allGroupsSelected }}</strong>
          <br />Indeterminate:
          <strong>{{ indeterminate }}</strong>
        </div>
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
    fetchGroups: function() {
      console.log(config.api.groups);
      this.$http.get(config.api.groups).then(result => {
        this.grupe = result.data;
        console.log("groups from api: ", this.grupe);
        for (const grupa of this.grupe) {
          this.grupeArray.push(grupa.name);
        }
        console.log(this.grupeArray);
      });
    },
    clickElem() {
      window.onclick = e => {
        this.selectedCell = e.target.id;
        console.log(e.target.id);
      };
      return this.selectedCell;
    },
    seriiDict() {
      let currSerie;
      let found;
      let res = [];
      for (const grupa of this.grupe) {
        if (grupa.length == 5) {
          currSerie = grupa.slice(-2)[0];
        }
        if (grupa.length == 4) {
          currSerie = grupa.slice(-1);
        }
        found = false;

        for (const serie of res) {
          if (serie.serie == currSerie && serie.serie) {
            serie.grupe.push(grupa);
            found = true;
            break;
          }
        }

        if (found == false) {
          res.push({
            serie: currSerie,
            grupe: [grupa],
            allGroupsSelected: false,
            selectedGroups: [],
            indeterminate: false
          });
        }
      }
      return res;
    },
    toggleAllGroups(checked) {
      this.selectedGroups = checked ? this.currentSerie.grupe.slice() : [];
    }
  },
  created: function() {
    this.fetchGroups();
    console.log("created!");
    this.serii = this.seriiDict();
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
      serii: [],
      selectedGroups: [],
      allGroupsSelected: false,
      indeterminate: false,
      selectedCourse: null,
      availableCourses: [
        { value: null, text: "Please select a course", disabled: true },
        { value: "am2", text: "Analiza Matematica 2 - Seria G", left: 5 }
      ],
      currentSerie: {},
      startTime: 0,
      endTime: 0,
      selectedCell: ""
    };
  },
  watch: {
    selectedGroups(newVal, oldVal) {
      console.log(newVal);
      console.log(oldVal);
      // Handle changes in individual flavour checkboxes
      if (newVal.length === 0) {
        this.indeterminate = false;
        this.allGroupsSelected = false;
      } else if (newVal.length === this.currentSerie.grupe.length) {
        this.indeterminate = false;
        this.allGroupsSelected = true;
      } else {
        this.indeterminate = true;
        this.allGroupsSelected = false;
      }
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
</style>
