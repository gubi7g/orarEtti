<template>
  <div id="app">
    <h1>Orar ETTI</h1>

    <img id="ettigif" src="./assets/logo.gif" width="100" />

    <!-- <h1>{{createSerii}}</h1> -->
    <img id="vuelogo" src="./assets/logo.png" width="100" />
    <b-row>
      <b-col>
        <p>Clicked: {{clickElem()}} </p>

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
                <td v-else v-bind:key="grupa.id" :id="grupa + ora.split('-').join('')"></td>
              </template>
            </tr>
          </tbody>
        </table>
      </b-col>
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
export default {
  name: "App",
  components: {},
  computed: {
  },
  methods: {
    clickElem() {
      window.onclick = e => {
        this.selectedCell = e.target.id;
        console.log(e.target.id)
        
      };
      return this.selectedCell
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
    console.log("created!");
    this.serii = this.seriiDict();
    console.log(this.serii);
    this.currentSerie = this.serii[0];
    console.log(this.currentSerie);
  },
  data: () => {
    return {
      grupe: ["432A", "433A", "432B", "432C", "432D", "432E", "432F"],
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

table {
  border-collapse: collapse;
}
td {
  border: 1px solid black;
  width: 100px;
  height: 50px;
}

#vuelogo {
  position: absolute;
  top: 0px;
  left: 0px;
}
</style>
