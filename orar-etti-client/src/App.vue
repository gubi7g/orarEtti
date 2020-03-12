<template>
  <div id="app">
    <h1>Orar ETTI</h1>

    <img id="ettigif" src="./assets/logo.gif" width="100" />
    <!-- <h1>{{createSerii}}</h1> -->
    <img id="vuelogo" src="./assets/logo.png" width="100" />
    <h3>Selected Year: {{selectedYear}}</h3>
    <b-row>
      <b-col>
        <b-button @click.stop="selectedYear = 1">An 1</b-button>
      </b-col>
      <b-col>
        <b-button @click.stop="selectedYear = 2">An 2</b-button>
      </b-col>
      <b-col>
        <b-button @click.stop="selectedYear = 3">An 3</b-button>
      </b-col>
      <b-col>
        <b-button @click.stop="selectedYear = 4">An 4</b-button>
      </b-col>
    </b-row>
    <b-row>
      <table class="orar" @click="clickCell(); rightClick()">
        <thead>
          <tr>
            <th v-for="grupa in ['', ...groupsArray]" :key="grupa.key">{{grupa}}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(ora, ind_ora) in ore" v-bind:key="ora.id">
            <template v-for="grupa in ['', ...groupsArray]">
              <td v-if="grupa == ''" v-bind:key="grupa.id">{{ore[ind_ora]}}</td>
              <td
                v-else
                v-bind:key="grupa.id"
                :id="grupa + ora.split('-').join('')"
                :class="assignSelectedClasses(grupa + ora.split('-').join(''))"
              ></td>
            </template>
          </tr>
        </tbody>
      </table>
    </b-row>
    <b-row>
      <b-col cols="8">
        <h1>Edit your course</h1>

        <b-row>
          <b-col>
            <h3>Select your course:</h3>
            <b-form-select
              v-model="selectedCourse"
              id="dropdown-courses"
              class="mt-2"
              :options="coursesArray"
            ></b-form-select>
          </b-col>

          <b-col>
            <h3>...or input your own!</h3>
            <b-form-input v-model="selectedCourse" id="input-text-course" placeholder="Class name"></b-form-input>
          </b-col>

          <b-col>
            <h3>Select series</h3>
            <b-form-select
              v-model="selectedSeries"
              id="dropdown-series"
              class="mt-2"
              :options="seriesArray"
            ></b-form-select>
          </b-col>
          <b-col>
            <h3>Enter duration</h3>
            <b-form-input
              v-model="selectedDuration"
              id="input-text-duration"
              placeholder="Duration"
            ></b-form-input>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <h3>Day:</h3>
            <b-form-select v-model="selectedDay" id="dropdown-days" class="mt-3" :options="dotw"></b-form-select>
          </b-col>
          <b-col>
            <h3>Start Time:</h3>
            <b-form-input type="time"></b-form-input>
          </b-col>
          <b-col>
            <h3>End Time:</h3>
            <b-form-input type="time"></b-form-input>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <h1>selected course: {{selectedCourse}}</h1>
          </b-col>
          <b-col>
            <h1>selected series: {{selectedSeries}}</h1>
          </b-col>
          <b-col>
            <h1>selected duration: {{selectedDuration}}</h1>
          </b-col>
        </b-row>

        <b-row>
          <h1>Please select groups/series:</h1>
          <b-form-group id="checkbox-serie" text="Courses" class="m-md-2">
            <b-form-checkbox
              v-model="allGroupsSelected"
              :indeterminate="indeterminate"
              @change="toggleAllGroups"
            >{{ allGroupsSelected ? 'Un-select all ' : 'Select all ' }}</b-form-checkbox>

            <b-form-checkbox-group v-model="selectedGroups" :options="groupsArray"></b-form-checkbox-group>
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
        </b-row>
      </b-col>
      <b-col><p>{{(this.compareGroups('414A', '414A') == undefined) ? 'yes' : 'no' }}</p></b-col>
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
    fetchCourses: function() {
      this.$http.get(config.api.courses).then(result => {
        this.allCoursesArray = [];
        console.log("all courses: ", this.allCoursesArray);
        for (const course of result.data) {
          course.text = course.name;
          course.value = course.name;
          this.allCoursesArray.push(course);
        }

        this.filterCoursesArray(); // ca sa nu fie empty tabelul on reload...
      });
    },
    filterCoursesArray: function() {
      this.coursesArray = [];
      this.coursesArray.push({
        value: null,
        text: `Year ${this.selectedYear} courses`,
        disabled: true
      });
      for (const course of this.allCoursesArray) {
        if (course.an == this.selectedYear) this.coursesArray.push(course);
      }
      this.selectedCourse = null;

      console.log(this.coursesArray);
    },
    fetchGroups: function() {
      console.log(config.api.groups);
      this.$http.get(config.api.groups).then(result => {
        this.allGroupsArray = [];
        this.seriesArray.push({ text: "Select all series", value: null });
        for (const grupa of result.data) {
          this.allGroupsArray.push(grupa.name);
          this.seriesArray.push(grupa.series);
        }
        this.seriesArray = [...new Set(this.seriesArray)];
        console.log(this.allGroupsArray);
        console.log(this.seriesArray);

        this.filterGroupsArray(); // ca sa nu fie empty tabelul on reload...
      });
    },
    filterGroupsArray() {
      this.groupsArray = [];
      for (const grupa of this.allGroupsArray) {
        if (grupa[1] == this.selectedYear) {
          if (grupa[3] == this.selectedSeries) this.groupsArray.push(grupa);
          else if (this.selectedSeries == null) this.groupsArray.push(grupa);
        }
      }
    },
    findSelectedTimeInts: function() {
      let selectedTimeInts = [];
      if (this.selectedGroups.length > 0) {
        for (let i = 0; i < this.selectedDuration; i++) {
          let startTimeSelected = (
            parseInt(this.selectedTimeInt.substr(0, 2)) + i
          )
            .toString()
            .padStart(2, "0");
          let endTimeSelected = (
            parseInt(this.selectedTimeInt.substr(2, 2)) + i
          )
            .toString()
            .padStart(2, "0");

          selectedTimeInts.push(startTimeSelected + endTimeSelected);
        }
      }
      return selectedTimeInts;
    },
    findMinGroupFromSelected() {
      let min = this.groupsArray[this.groupsArray.length - 1];
      for (const grupa of this.selectedGroups) {
      //   if (grupa[3] < min[3]) {
      //     min = grupa;
      //   } else if (grupa[3] == min[3]) {
      //     if (grupa[1] < min[1]) {
      //       min = grupa;
      //     } else if (grupa[1] == min[1]) {
      //       if (grupa[2] < min[2]) {
      //         min = grupa;
      //       } else if (grupa[2] == min[2]) {
      //         if ((grupa.length == min.length) == 5)
      //           if (grupa[4] < min[4]) min = grupa;
      //       }
      //     }
      //   }
        if(this.compareGroups(min, grupa))
          min = grupa
      }

      return min;
    },
    findMaxGroupFromSelected() {
      let max = this.groupsArray[0];
      for (const grupa of this.selectedGroups) {
        // if (grupa[3] > max[3]) {
        //   max = grupa;
        // } else if (grupa[3] == max[3]) {
        //   if (grupa[1] > max[1]) {
        //     max = grupa;
        //   } else if (grupa[1] == max[1]) {
        //     if (grupa[2] > max[2]) {
        //       max = grupa;
        //     } else if (grupa[2] == max[2]) {
        //       if ((grupa.length == max.length) == 5)
        //         if (grupa[4] > max[4]) max = grupa;
        //     }
        //   }
        // }
        if(this.compareGroups(grupa, max))
          max = grupa
      }

      return max;
    },
    // is @gr1 >= than @gr2?
    compareGroups: function(gr1, gr2) {
      if (gr1[1] > gr2[1]) {
        return true;
      } else if (gr1[1] == gr2[1]) {
        if (gr1[3] > gr2[3]) {
          return true;
        } else if (gr1[3] == gr2[3]) {
          if (gr1[2] > gr2[2]) {
            return true;
          } else if (gr1[2] == gr2[2]) {
            if (gr1.length == 5 && gr2.length == 5){
              if (gr1[4] >= gr2[4]) return true;
              else return false;
            }
            else return true
              
          } else { // gr1[2] < gr2[2] 
            return false;
          }
        } else { // gr1[3] < gr2[3] 
          return false;
        }
      } else { // gr[1] < gr2[1]
        return false;
      }
    },
    assignSelectedClasses: function(id) {
      let res = "";
      let currCellGroup = "";

      if (id.length == 9) {
        currCellGroup = id.substr(0, 5);
      } else if (id.length == 8) {
        currCellGroup = id.substr(0, 4);
      }

      if(!this.selectedGroups.includes(currCellGroup))
        return res


      let selectedTimeInts = this.findSelectedTimeInts();
      console.log(selectedTimeInts)
      // if(selectedTimeInts.length > 0)
      //   selectedTimeInts.sort();

      let minGroup = this.findMinGroupFromSelected();
      let maxGroup = this.findMaxGroupFromSelected();
      console.log("min: ", minGroup, " max: ", maxGroup);


      

      let currCellTimeInt = id.substr(-4, 4);
      if (this.selectedGroups.length > 0) {
        if (
          currCellTimeInt >= selectedTimeInts[0] &&
          selectedTimeInts[selectedTimeInts.length - 1] >= currCellTimeInt &&
          currCellGroup == minGroup
        ) {
          res += "selectedCellsLeft ";
        }

        if (
          currCellTimeInt >= selectedTimeInts[0] &&
          selectedTimeInts[selectedTimeInts.length - 1] >= currCellTimeInt &&
          currCellGroup == maxGroup
        ) {
          res += "selectedCellsRight ";
        }
        // console.log(this.compareGroups(currCellGroup, minGroup))
        // console.log(this.compareGroups(maxGroup, currCellGroup))
        console.log('current cell: ', currCellGroup)

        console.log(this.compareGroups(currCellGroup, minGroup))
        console.log( this.compareGroups(maxGroup, currCellGroup))

        console.log(currCellTimeInt == selectedTimeInts[0])
        if (
          this.compareGroups(currCellGroup, minGroup) &&
          this.compareGroups(maxGroup, currCellGroup) &&
          currCellTimeInt == selectedTimeInts[0]
        ) {
          console.log("res-top");

          res += "selectedCellsTop ";
        }

        if (
          this.compareGroups(currCellGroup, minGroup) &&
          this.compareGroups(maxGroup, currCellGroup) &&
          currCellTimeInt == selectedTimeInts[selectedTimeInts.length - 1]
        ) {
          console.log("res-bottom");
          res += "selectedCellsBottom ";
        }
      }

      return res;
    },
    rightClick() {
      window.oncontextmenu = e => {
        let isRightMB;
        e = e || window.event;
        if ("which" in e)
          // Gecko (Firefox), WebKit (Safari/Chrome) & Opera
          isRightMB = e.which == 3;
        else if ("button" in e)
          // IE, Opera
          isRightMB = e.button == 2;

        if (isRightMB) this.selectedGroups = [];
        return false;
      };
    },
    clickCell() {
      window.onclick = e => {
        if (/^4[1-4]\d[A-G](a|b|)\d{4}$/.test(e.target.id)) {
          let clickedGroupName;
          if (e.target.id.length == 9) {
            clickedGroupName = e.target.id.substr(0, 5);
          } else if (e.target.id.length == 8) {
            clickedGroupName = e.target.id.substr(0, 4);
          } else {
            return console.log("error on click group name length");
          }

          console.log(clickedGroupName);
          if (this.selectedGroups.includes(clickedGroupName)) {
            console.log(
              this.selectedGroups[
                this.selectedGroups.indexOf(clickedGroupName)
              ].substr(e.target.id.length - 4, e.target.id.length)
            );
            if (
              e.target.id.substr(e.target.id.length - 4, e.target.id.length) ==
              this.selectedTimeInt
            ) {
              // daca este acelasi interval selectat, sterge-l din selectate
              this.selectedGroups.splice(
                this.selectedGroups.indexOf(clickedGroupName),
                1
              );
            } else {
              //pass
            }
          } else {
            console.log("added new group to selected");
            this.selectedGroups.push(clickedGroupName);
          }
          this.selectedTimeInt = e.target.id.substr(
            e.target.id.length - 4,
            e.target.id.length
          );
        }

        return e.target.id;
      };
    },
    toggleAllGroups(checked) {
      this.selectedGroups = checked ? this.groupsArray.slice() : [];
    }
  },
  created: function() {
    this.fetchGroups();
    this.fetchCourses();
    console.log("created!");
  },
  data: () => {
    return {
      groupsArray: [],
      allGroupsArray: [],
      seriesArray: [],
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
      currentSerie: {},
      selectedTimeInt: "",
      selectedYear: 1,
      selectedGroupsIds: [],
      selectedClass: "",
      selectedSeries: null,
      allCoursesArray: [],
      coursesArray: [],
      selectedDuration: 2
    };
  },
  watch: {
    selectedGroups(newVal) {
      // Handle changes in individual flavour checkboxes
      if (newVal.length === 0) {
        this.indeterminate = false;
        this.allGroupsSelected = false;
      } else if (newVal.length === this.groupsArray.length) {
        this.indeterminate = false;
        this.allGroupsSelected = true;
      } else {
        this.indeterminate = true;
        this.allGroupsSelected = false;
      }
    },
    selectedYear() {
      this.filterGroupsArray();
      this.filterCoursesArray();
      this.selectedGroups = [];
    },
    selectedSeries() {
      this.filterGroupsArray();
      this.selectedGroups = [];
    },
    selectedCourse() {
      console.log("new selected course: ", this.selectedCourse);
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
.selectedCells {
  border: 5px solid orangered;
}

.selectedCellsTop {
  border-top: 5px solid orangered;
}

.selectedCellsRight {
  border-right: 5px solid orangered;
}

.selectedCellsLeft {
  border-left: 5px solid orangered;
}

.selectedCellsBottom {
  border-bottom: 5px solid orangered;
}
</style>
