<template>
  <div>
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
          <!-- <b-col>
            <h1>Please select groups/series:</h1>
            <b-form-group id="checkbox-serie" text="Courses" class="m-md-2">
              <b-form-checkbox
                v-model="allGroupsSelected"
                :indeterminate="indeterminate"
                @change="toggleAllGroups"
              >{{ allGroupsSelected ? 'Un-select all ' : 'Select all ' }}</b-form-checkbox>

              <b-form-checkbox-group v-model="selectedGroups" :options="groupsArray"></b-form-checkbox-group>
            </b-form-group>
          </b-col> -->
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
            <h1>selected start time: {{selectedTimeInt.substr(0,2)}}</h1>
          </b-col>
          <b-col>
            <h1>selected day: {{selectedDay}}</h1>
          </b-col>
        </b-row>
      </b-col>
    </b-row>

    <h3>Selected Year: {{selectedYear}}</h3>
    <b-row>
      <b-col>
        <b-button @click="selectedYear = 1">An 1</b-button>
      </b-col>
      <b-col>
        <b-button @click="selectedYear = 2">An 2</b-button>
      </b-col>
      <b-col>
        <b-button @click="selectedYear = 3">An 3</b-button>
      </b-col>
      <b-col>
        <b-button @click="selectedYear = 4">An 4</b-button>
      </b-col>
    </b-row>
    <b-row>
      <table class="orar" @click="clickCellRevised()">
        <thead>
          <tr>
            <th
              v-for="grupa in ['Day', 'Time', ...groupsArrayTest]"
              :key="grupa.key"
            >{{grupa.grupa}}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(dayInt, dayIntIndex) in createDayIntTable">
            <tr v-bind:key="dayInt.id">
              <template v-for="grupa in [{grupa: 1}, {grupa: 2}, ...groupsArrayTest]">
                <td
                  v-if="grupa.grupa == 1 && dayIntIndex % ore.length == 0"
                  v-bind:key="grupa.grupa.id"
                  :rowspan="ore.length"
                >{{dayInt[0]}}</td>
                <td v-else-if="grupa.grupa == 2" v-bind:key="grupa.grupa.id">{{dayInt[1]}}</td>
                <td
                  v-else-if="grupa.grupa != 1 && grupa.grupa != 2"
                  v-bind:key="grupa.grupa.id"
                  :id="createIdFromClass(grupa.grupa, dayInt[1].split('-').join(''), dayInt[0])"
                  :class="findSelectedTimeInts.indexOf(dayInt[1].split('-').join('')) > -1 && dayInt[0] == selectedDay ? updateCellsStyle(createIdFromClass(grupa.grupa, dayInt[1].split('-').join(''), dayInt[0])) : ''"
                ></td>
              </template>
            </tr>
          </template>
        </tbody>
      </table>
      <div :style="findFloatingButtonPosition()" id="floatingDiv">
        <b-button @click="postClass()">Send</b-button>
      </div>
    </b-row>
    <template v-for="cls in this.allReservedClasses">
      <div :key="cls.id">{{cls.name}} {{cls.groups}}</div>
    </template>
  </div>

  <!-- <p>{{this.serii}}</p> -->
</template>

<script>
const config = require("../config.json");

export default {
  name: "Orar",
  components: {},
  computed: {
    createDayIntTable: function() {
      let table = [];

      for (const day of this.dotw.slice(1, this.dotw.length)) {
        for (const int of this.ore) {
          table.push([day, int]);
        }
      }

      return table;
    },
    groupsArray() {
      // computed prop representing remaining groups after filtering series + year
      let res = [];
      for (const grupa of this.allGroupsArray) {
        if (grupa[1] == this.selectedYear) {
          if (grupa[3] == this.selectedSeries) res.push(grupa);
          else if (this.selectedSeries == null) res.push(grupa);
        }
      }
      return res;
    },
    groupsArrayTest() {
      // computed prop representing remaining groups after filtering series + year
      let res = [];
      for (const grupa of this.allGroupsArray) {
        let tmp = {};

        if (grupa[1] == this.selectedYear) {
          if (grupa[3] == this.selectedSeries) {
            tmp.grupa = grupa;
            tmp.selected = false;
            tmp.style = "";
          } else if (this.selectedSeries == null) {
            tmp.grupa = grupa;
            tmp.selected = false;
            tmp.style = "";
          }

          res.push(tmp);
        }
      }
      return res;
    },
    findSelectedTimeInts() {
      let selectedTimeInts = [];
      if (this.selectedGroupsRevised.length > 0) {
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

          if (startTimeSelected >= "21") break;
          selectedTimeInts.push(startTimeSelected + endTimeSelected);
        }
      }
      console.log(selectedTimeInts);
      return selectedTimeInts;
    }
  },
  methods: {
    breakIntoConsecGroups(array) {
      // ceva gen [1, 3, 4] -> [[1], [3, 4]] doar ca pt grupe pt toate clasele
      // another eg: [1, 2, 4] -> [[1, 2], [4]]

      let res = [];
      let tmp = [];
      let sorted = [...array].sort(this.compareGroups);
      let i = this.allGroupsArray.indexOf(sorted[0]);
      console.log(sorted);
      let continuity = true;
      for (const grupa of sorted) {
        if (grupa == this.allGroupsArray[i]) {
          if (!continuity) continuity = true;

          tmp.push(grupa);
          i++;
        } else {
          if (tmp.length) {
            if (continuity) continuity = false;

            res.push(tmp);
            tmp = [];
          }
          while (grupa != this.allGroupsArray[i]) {
            // fast-forward pana cand ajungi la indexul dorit
            i++;
            console.log(i);
            if (i > 500) {
              console.log("ERROR");
              break;
            }
          }
          tmp.push(grupa);
        }
      }

      if (!res.length || tmp.length) res.push(tmp);

      return res;
    },

    getCellProps(id) {
      let currCellTimeInt = id.substr(-6, 4);
      let currCellDay = id.substr(-2, 2);
      let currCellGroup;
      if (id.length == 11) {
        currCellGroup = id.substr(0, 5);
      } else if (id.length == 10) {
        currCellGroup = id.substr(0, 4);
      }

      for (const day of this.dotw.slice(1, this.dotw.length)) {
        if (day.substr(0, 2) == currCellDay) {
          currCellDay = day.substr(0, 2);
          break;
        }
      }

      return {
        group: currCellGroup,
        timeInt: currCellTimeInt,
        day: currCellDay
      };
    },
    createIdFromClass(group, int, day) {
      return group + int + day.substr(0, 2);
    },
    findFloatingButtonPosition: function() {
      let maxGroup = this.findMaxGroupFromSelected(this.selectedGroups);
      if (this.findSelectedTimeInts.length > 0) {
        if (this.selectedTimeInt) {
          let closestCell = document.getElementById(
            maxGroup +
              this.findSelectedTimeInts.pop() +
              this.selectedDay.substr(0, 2)
          );

          let x = Math.round(
            window.scrollX + closestCell.getBoundingClientRect().left
          );
          let y = Math.round(
            window.scrollY + closestCell.getBoundingClientRect().top
          );

          return `position:absolute; z-index:10; top:${y + 50}px; left:${x}px`;
        }
      } else {
        return "display: none";
      }
    },
    postClass: function() {
      console.log({
        name: this.selectedCourse,
        duration: this.selectedDuration,
        day: this.selectedDay,
        startTime: this.findSelectedTimeInts[0].substr(0, 2),
        endTime: this.findSelectedTimeInts[
          this.findSelectedTimeInts.length - 1
        ].substr(2, 2),
        prof: this.loggedProf,
        room: this.selectedRoom,
        groups: this.selectedGroups
      });
      let newClass = {
        name: this.selectedCourse,
        duration: this.selectedDuration,
        day: this.selectedDay,
        startTime: this.findSelectedTimeInts[0].substr(0, 2),
        endTime: this.findSelectedTimeInts[
          this.findSelectedTimeInts.length - 1
        ].substr(2, 2),
        prof: this.loggedProf,
        room: this.selectedRoom,
        groups: this.selectedGroups
      };
      this.$http
        .post(config.admin.newclass, newClass)
        .then(response => {
          console.log(response);
          console.log("succesfully reserved interval");

          // mai fa un fetch dupa classes.
          this.fetchClasses();
        })
        .catch(err => {
          console.log(err);
        });
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

        // this.filterGroupsArray(); // ca sa nu fie empty tabelul on reload...
      });
    },
    fetchClasses: function() {
      this.$http.get(config.api.classes).then(result => {
        this.allReservedClasses = result.data;
        // this.allReservedClasses = this.breakIntoConsecGroups(this.allReservedClasses)
        console.log("reserved classes:", this.allReservedClasses);
      });
    },
    // filterGroupsArray() {
    //   this.groupsArray = [];
    //   for (const grupa of this.allGroupsArray) {
    //     if (grupa[1] == this.selectedYear) {
    //       if (grupa[3] == this.selectedSeries) this.groupsArray.push(grupa);
    //       else if (this.selectedSeries == null) this.groupsArray.push(grupa);
    //     }
    //   }
    // },

    findMinGroupFromSelected(x) {
      let min = this.groupsArray[this.groupsArray.length - 1]; // initialize with max group
      for (const grupa of x) {
        if (this.compareGroups(min, grupa) >= 0) min = grupa;
      }

      return min;
    },
    findMaxGroupFromSelected(x) {
      let max = this.groupsArray[0];
      for (const grupa of x) {
        if (this.compareGroups(grupa, max) >= 0) max = grupa;
      }

      return max;
    },
    //    gr1 > gr2? return 1
    //    gr1 == gr2? return 0
    //    gr1 < gr2? return -1
    compareGroups: function(gr1, gr2) {
      if (gr1[1] > gr2[1]) {
        return 1;
      } else if (gr1[1] == gr2[1]) {
        if (gr1[3] > gr2[3]) {
          return 1;
        } else if (gr1[3] == gr2[3]) {
          if (gr1[2] > gr2[2]) {
            return 1;
          } else if (gr1[2] == gr2[2]) {
            if (gr1.length == 5 && gr2.length == 5) {
              if (gr1[4] > gr2[4]) return 1;
              else if (gr1[4] == gr2[4]) return 0;
              else return -1;
            } else {
              return 0;
            }
          } else {
            // gr1[2] < gr2[2]
            return -1;
          }
        } else {
          // gr1[3] < gr2[3]
          return -1;
        }
      } else {
        // gr[1] < gr2[1]
        return -1;
      }
    },
    getGroupsBetweenMinMax: function(array) {
      let res = [];
      let minGroup = this.findMinGroupFromSelected(array);
      let maxGroup = this.findMaxGroupFromSelected(array);

      let indStart = this.groupsArray.indexOf(minGroup);
      let indEnd = this.groupsArray.indexOf(maxGroup);

      for (let i = indStart + 1; i < indEnd; i++) {
        res.push(this.groupsArray[i]);
      }

      return res;
    },

    toggleAllGroups(checked) {
      this.selectedGroups = checked ? this.allGroupsArray.slice() : [];
    },
    clickCellRevised() {
      /*
        1 singur click:
          - daca este deja inclus in selectedGroups: nu ar trebui sa faca nimic inca
          - daca nu este deja inclus in selectedGroups: ar trebui sa fie deja aplicat stilul, adica bagat in selectedGroups.

        dbl click:
          - daca este inclus: 
      **/
      // let clickedGroupExt;
      let group, timeInt, day;
      window.onclick = e => {
        console.log('click')
        // aici as vrea sa se incarce deja selected class pentru cell-ul clicked
        // daca nu facem asta, o sa fie delay-ul pus de la setTimeout ALWAYS daca nu faci dublu click
        this.prevent = false;
        if (/^4[1-4]\d[A-G](a|b|)\d{4}[A-Z][a-z]$/.test(e.target.id)) {
          let temp = this.getCellProps(e.target.id);
          group = temp.group
          timeInt = temp.timeInt
          day = temp.day

          console.log(group)
          console.log(this.getCellProps(e.target.id))

          this.selectedTimeInt = timeInt;

          // facem schimbarea de zi in afara conditiei
          for (const _day of this.dotw.slice(1, this.dotw.lengh)) {
            // primul element e junk pt dropdown
            if (_day.substr(0, 2) == day) {
              this.selectedDay = _day;
              break;
            }
          }


          this.maybeDblClick = setTimeout(() => {
            // aici vreau sa adaug/scot din selected grupa clicked, si sa pornesc event listner pt hover
            let found = false;

            if (!this.prevent) {
              if (this.selectedDay.substr(0, 2) == day) {
                // daca clickul este in aceeasi zi
                if (timeInt == this.selectedTimeInt) {
                  // daca este SI acelasi interval selectat (pe langa aceeasi zi), sterge-l din selectate
                  for (const [
                    index,
                    selection
                  ] of this.selectedGroupsRevised.entries()) {
                    if (selection.indexOf(group) > -1) {
                      if (selection.length == 1) {
                        // daca este deja selectat si este doar o casuta izolata
                        this.selectedGroupsRevised.splice(
                          this.selectedGroupsRevised.indexOf(selection),
                          1
                        );
                      } else {
                        // daca este deja selectat dar este un interval
                        if (
                          group == selection[0] ||
                          group == selection[selection.lengh - 1]
                        ) {
                          this.selectedGroupsRevised[index] = selection.splice(
                            group,
                            1
                          );
                        } else {
                          this.selectedGroupsRevised.splice(index, 1);
                        }
                      }
                      found = true;
                      break;
                    }
                  }

                  if (!found) {
                    // daca nu a fost gasita grupa, o adaugam!
                    // acum vine partea mai complicata...
                  }
                }
              }

              // no matter what cell is clicked, we update selectedTimeInt and selectedDay after each click.
              
            }
            return;
          }, 500)// we must apply classes outside the timeout for faster response
        }

        window.ondblclick = () => {
          console.log(group)
          // aici vreau sa adaug/scot din selected si atat.
          this.prevent = true;
          clearTimeout(this.maybbeDblClick);
          this.selectedGroupsRevised.push([group])
          console.log("sike! dbl click");
          console.log(this.selectedGroupsRevised);

        };

        
      };

      
    },
    updateCellsStyle(id) {
      const { group, timeInt } = this.getCellProps(id);
      let style = "";
      for (const g of this.selectedGroupsRevised) {
        if (g.indexOf(group) > -1) {
          const timeInts = this.findSelectedTimeInts;
          if (timeInts.indexOf(timeInt) == 0) {
            style += " selectedCellsTop";
          }

          if (timeInts.indexOf(timeInt) == timeInts.length - 1) {
            style += " selectedCellsBottom";
          }

          if (g.indexOf(group) == 0) {
            style += " selectedCellsLeft";
          }

          if (g.indexOf(group) == g.length - 1) {
            style += " selectedCellsRight";
          }
          break;
        }
      }
      return style;
    }
  },
  created: function() {
    this.fetchGroups();
    this.fetchCourses();
    // add fetchClasses
    this.fetchClasses();
    console.log("created!");
  },

  data: () => {
    return {
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
      selectedGroupsRevised: [],
      allGroupsSelected: false,
      indeterminate: false,
      selectedCourse: null,
      selectedTimeInt: "",
      selectedYear: 1,
      selectedSeries: null,
      allCoursesArray: [],
      coursesArray: [],
      selectedDuration: 2,
      loggedProf: null,
      selectedRoom: null,
      selectedGroupsDbl: [],
      selectedGroupsSgl: [],
      maybeDblClick: 0,
      prevent: false,
      clickSelection: [],
      selectedGroupsInt: [],
      selectedGroupsUnique: [],
      allReservedClasses: []
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
      // this.filterGroupsArray();
      this.filterCoursesArray();
      this.selectedGroupsSgl = [];
      this.selectedGroupsDbl = [];
    },
    selectedSeries() {
      // this.filterGroupsArray();
      this.selectedGroupsSgl = [];
      this.selectedGroupsDbl = [];
    },
    selectedCourse() {
      console.log("new selected course: ", this.selectedCourse);
    },
    selectedGroupsDbl() {
      this.selectedGroups = [
        ...new Set([...this.selectedGroupsSgl, ...this.selectedGroupsDbl])
      ]; // temp fix. hate this
    },
    selectedGroupsSgl() {
      this.selectedGroups = [
        ...new Set([...this.selectedGroupsDbl, ...this.selectedGroupsSgl])
      ]; // temp fix. hate this
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
  min-width: 100px;
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
