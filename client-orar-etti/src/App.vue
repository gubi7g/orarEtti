<template>
  <div id="app">
    <h1>Orar ETTI</h1>

    <img id="ettigif" src="./assets/logo.gif" width="100" />
    <!-- <h1>{{createSerii}}</h1> -->
    <img id="vuelogo" src="./assets/logo.png" width="100" />

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
          <b-col>
            <h1>Please select groups/series:</h1>
            <b-form-group id="checkbox-serie" text="Courses" class="m-md-2">
              <b-form-checkbox
                v-model="allGroupsSelected"
                :indeterminate="indeterminate"
                @change="toggleAllGroups"
              >{{ allGroupsSelected ? 'Un-select all ' : 'Select all ' }}</b-form-checkbox>

              <b-form-checkbox-group v-model="selectedGroups" :options="groupsArray"></b-form-checkbox-group>
            </b-form-group>
          </b-col>
          <b-col>
            <div>
              Selected groups:
              <strong>{{ selectedGroups }}</strong>
              <br />All Selected:
              <strong>{{ allGroupsSelected }}</strong>
              <br />Indeterminate:
              <strong>{{ indeterminate }}</strong>
            </div>
          </b-col>
          <b-col>
            <h1>selected start time: {{this.selectedTimeInt.substr(0,2)}}</h1>
          </b-col>
          <b-col>
            <h1>selected day: {{this.selectedDay}}</h1>
          </b-col>
        </b-row>
      </b-col>
      <b-col>
        <p>{{(this.compareGroups('414A', '414A') == undefined) ? 'yes' : 'no' }}</p>
      </b-col>
    </b-row>

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
            <th v-for="grupa in ['Day', 'Time', ...groupsArray]" :key="grupa.key">{{grupa}}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(dayInt, dayIntIndex) in createDayIntTable()">
            <tr v-bind:key="dayInt.id">
              <template v-for="grupa in [1, 2, ...groupsArray]">
                <td
                  v-if="grupa == 1 && dayIntIndex % ore.length == 0"
                  v-bind:key="grupa.id"
                  :rowspan="ore.length"
                >{{dayInt[0]}}</td>
                <td v-else-if="grupa == 2" v-bind:key="grupa.id">{{dayInt[1]}}</td>
                <td
                  v-else-if="grupa != 1 && grupa != 2"
                  v-bind:key="grupa.id"
                  :id="grupa + dayInt[1].split('-').join('') + dayInt[0].substr(0,2)"
                  :class="assignSelectedClasses(grupa + dayInt[1].split('-').join('') + dayInt[0].substr(0,2))"
                ></td>
              </template>
            </tr>
          </template>
        </tbody>
      </table>
      <div :style="findFloatingButtonPosition()" id="floatingDiv">
        <b-button @click="postReservation()">Send</b-button>
      </div>
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
    findFloatingButtonPosition: function() {
      let maxGroup = this.findMaxGroupFromSelected();
      if (this.findSelectedTimeInts().length > 0) {

        if (this.selectedTimeInt) {
          let closestCell = document.getElementById(
            maxGroup +
              this.findSelectedTimeInts().pop() +
              this.selectedDay.substr(0, 2)
          );

          let x = Math.round(
            window.scrollX + closestCell.getBoundingClientRect().left
          );
          let y = Math.round(
            window.scrollY + closestCell.getBoundingClientRect().top
          );

          return `position:absolute; z-index:10; top:${y +
            50}px; left:${x}px`;
        }
      }
    },

    postReservation: function() {
      console.log({
        name: this.selectedCourse,
        duration: this.selectedDuration,
        day: this.selectedDay,
        startTime: this.findSelectedTimeInts()[0].substr(0, 2),
        endTime: this.findSelectedTimeInts()[this.findSelectedTimeInts().length - 1].substr(2, 2),
        prof: this.loggedProf,
        room: this.selectedRoom,
        groups: this.selectedGroups
      })
      let newClass = {
        name: this.selectedCourse,
        duration: this.selectedDuration,
        day: this.selectedDay,
        startTime: this.findSelectedTimeInts()[0].substr(0, 2),
        endTime: this.findSelectedTimeInts()[this.findSelectedTimeInts().length - 1].substr(2, 2),
        prof: this.loggedProf,
        room: this.selectedRoom,
        groups: this.selectedGroups
      }
      this.$http.post(config.admin.newclass, newClass)
        .then(response => {
          console.log(response)
          console.log('succesfully reserved interval')
        })
        .catch(err => { console.log(err) })
    },

    createDayIntTable: function() {
      let table = [];

      for (const day of this.dotw.slice(1, this.dotw.length)) {
        for (const int of this.ore) {
          table.push([day, int]);
        }
      }

      return table;
    },
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

            if(startTimeSelected >= '21') break
          selectedTimeInts.push(startTimeSelected + endTimeSelected);
        }
      }
      console.log(selectedTimeInts);
      return selectedTimeInts;
    },
    findMinGroupFromSelected() {
      let min = this.groupsArray[this.groupsArray.length - 1];
      for (const grupa of this.selectedGroups) {
        if (this.compareGroups(min, grupa)) min = grupa;
      }

      return min;
    },
    findMaxGroupFromSelected() {
      let max = this.groupsArray[0];
      for (const grupa of this.selectedGroups) {
        if (this.compareGroups(grupa, max)) max = grupa;
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
            if (gr1.length == 5 && gr2.length == 5) {
              if (gr1[4] >= gr2[4]) return true;
              else return false;
            } else return true;
          } else {
            // gr1[2] < gr2[2]
            return false;
          }
        } else {
          // gr1[3] < gr2[3]
          return false;
        }
      } else {
        // gr[1] < gr2[1]
        return false;
      }
    },
    getGroupsBetweenMinMax: function() {
      let res = [];
      let minGroup = this.findMinGroupFromSelected();
      let maxGroup = this.findMaxGroupFromSelected();

      let indStart = this.groupsArray.indexOf(minGroup);
      let indEnd = this.groupsArray.indexOf(maxGroup);

      for (let i = indStart + 1; i < indEnd; i++) {
        res.push(this.groupsArray[i]);
      }

      return res;
    },
    assignSelectedClasses: function(id) {
      let res = "";
      let currCellGroup = "";
      let currCellTimeInt = id.substr(-6, 4);
      let currCellDay = id.substr(-2, 2);

      if (id.length == 11) {
        currCellGroup = id.substr(0, 5);
      } else if (id.length == 10) {
        currCellGroup = id.substr(0, 4);
      }


      if(this.selectedDay && currCellDay != this.selectedDay.substr(0, 2))
        return res

      if (!this.selectedGroups.includes(currCellGroup)) {
        if (!this.getGroupsBetweenMinMax().includes(currCellGroup)) {
          return res;
        }
        for (const group of this.getGroupsBetweenMinMax())
          this.selectedGroups.push(group);
      }

      let selectedTimeInts = this.findSelectedTimeInts();

      let minGroup = this.findMinGroupFromSelected();
      let maxGroup = this.findMaxGroupFromSelected();
      console.log("min: ", minGroup, " max: ", maxGroup);

      

      if (this.selectedDay != null) {
        if (currCellDay == this.selectedDay.substr(0, 2)) {
          if (this.selectedGroups.length > 0) {
            if (
              currCellTimeInt >= selectedTimeInts[0] &&
              selectedTimeInts[selectedTimeInts.length - 1] >=
                currCellTimeInt &&
              currCellGroup == minGroup
            ) {
              res += "selectedCellsLeft ";
            }

            if (
              currCellTimeInt >= selectedTimeInts[0] &&
              selectedTimeInts[selectedTimeInts.length - 1] >=
                currCellTimeInt &&
              currCellGroup == maxGroup
            ) {
              res += "selectedCellsRight ";
            }
            // console.log(this.compareGroups(currCellGroup, minGroup))
            // console.log(this.compareGroups(maxGroup, currCellGroup))
            // console.log('current cell: ', currCellGroup)

            // console.log(this.compareGroups(currCellGroup, minGroup))
            // console.log( this.compareGroups(maxGroup, currCellGroup))

            // console.log(currCellTimeInt == selectedTimeInts[0])
            if (
              this.compareGroups(currCellGroup, minGroup) &&
              this.compareGroups(maxGroup, currCellGroup) &&
              currCellTimeInt == selectedTimeInts[0]
            ) {
              res += "selectedCellsTop ";
            }

            if (
              this.compareGroups(currCellGroup, minGroup) &&
              this.compareGroups(maxGroup, currCellGroup) &&
              currCellTimeInt == selectedTimeInts[selectedTimeInts.length - 1]
            ) {
              res += "selectedCellsBottom ";
            }
          }
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
        if (/^4[1-4]\d[A-G](a|b|)\d{4}[A-Z][a-z]$/.test(e.target.id)) {
          let clickedGroupName;
          let clickedInt
          let clickedDay
          if (e.target.id.length == 11) {
            clickedGroupName = e.target.id.substr(0, 5);
          } else if (e.target.id.length == 10) {
            clickedGroupName = e.target.id.substr(0, 4);
          } else {
            return console.log("error on click group name length");
          }

          clickedDay = e.target.id.substr(-2, 2)
          clickedInt = e.target.id.substr(e.target.id.length - 6, 4)

          console.log(clickedGroupName);
          if (this.selectedGroups.includes(clickedGroupName)) {
            // daca este deja in grupele selectate
            console.log(clickedInt);
            if (this.selectedDay.substr(0, 2) == clickedDay) {
              // daca clickul este in aceeasi zi
              console.log(this.selectedDay.substr(0, 2));
              console.log(clickedDay);
              if (
                clickedInt ==
                this.selectedTimeInt
              ) {
                // daca este SI acelasi interval selectat (pe langa aceeasi zi), sterge-l din selectate
                if (this.getGroupsBetweenMinMax().includes(clickedGroupName)) {
                  this.selectedGroups = [];
                }
                this.selectedGroups.splice(
                  this.selectedGroups.indexOf(clickedGroupName),
                  1
                );
              } else { // daca este in aceeasi zi dar alt interval
                for (const day of this.dotw.slice(1, this.dotw.lengh)) {
                  // primul element e junk pt dropdown
                  if (day.substr(0, 2) == clickedDay)
                    this.selectedDay = day;
                }
                //pass
              }
            } else {
              // we have to modify the entry with the same group
            }
          } else {
            console.log("added new group to selected");
            this.selectedGroups.push(clickedGroupName);
          }

          // intervalul selectat si ziua selectata trebuie neaparat schimbate DUPA verificare pt a pastra valoarea zilei/intervalului selectat
          this.selectedTimeInt = clickedInt

          // facem schimbarea de zi in afara conditiei
          for (const day of this.dotw.slice(1, this.dotw.lengh)) {
            // primul element e junk pt dropdown
            if (day.substr(0, 2) == clickedDay)
              this.selectedDay = day;
          }
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
      selectedDuration: 2,
      loggedProf: null,
      selectedRoom: null
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

.floatingDiv {
  position: absolute;
  z-index: 10;
  top: 30px;
  left: 50px;
  border: 3px solid #c00;
  background-color: #fff;
  width: 300px;
}
</style>
