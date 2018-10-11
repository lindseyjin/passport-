<template>
  <div class="app-container">
    <div class="card">
      <div class="card-header">
        Search Programs
      </div>
      <div class="card-body">
        <div class="input-group mb-3">
          <input type="text" v-model="search" class="form-control" placeholder="Search keywords...">
          <div class="input-group-append">
            <span class="input-group-text" data-toggle="tooltip" title="Show Filters"
                  style="cursor: pointer;" @click="applyFilters()"><i class="fas fa-caret-down"></i></span>
            <button v-if="filters === false" type="submit" class="btn btn-info"><i class="fa fa-search" aria-hidden="true"></i></button>
          </div>
        </div>
        <div v-if="filters" class="card mb-3">
          <div class="card-body inline">
            <div class="form-group">
              <label for=language-select>Languages</label>
              <select class="selectpicker" id="language-select">
                <option>Mustard</option>
                <option>Ketchup</option>
                <option>Relish</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
    <table class="table table-light table-striped">
      <thead>
      <tr>
        <th v-for="tableHeader in tableHeaders">{{tableHeader}}</th>
        <th/>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in filteredTableData">
        <td>{{item['program']}}</td>
        <td>{{item['host']}}</td>
        <td>{{returnString(item['languages'])}}</td>
        <td>{{returnString(item['terms'])}}</td>
        <td v-if="inList(item) === false" @click="addToList(item)" v-bind:style="{ padding: '15px', cursor: 'pointer'}" class="text-success">
          <i class="fas fa-lg fa-plus-circle"></i></td>
        <td v-else @click="removeFromList(item)" v-bind:style="{ padding: '15px', cursor: 'pointer'}" class="text-danger">
          <i class="fas fa-lg fa-minus-circle"></i></td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'ExchangeDataTable',
    data () {
      return {
        msg: 'Welcome to Your Vue.js App',
        tableHeaders: [
          'Program',
          'Host Institution',
          'Languages',
          'Terms'
        ],
        exchangeData: [],
        search: "",
        filters: false,
        terms: {

        },
        shortList: []
      }
    },
    mounted () {
      // Todo: move to services
      let self = this
      axios.get('http://127.0.0.1:5000/exchanges')
        .then(function (response) {
          console.log("successful get request")
          self.exchangeData = response.data
        })
        .catch(function (error){
          // console log error message
          console.log(error)
        })
    },
    computed: {
      filteredTableData: function () {
        if (!this.search) return this.exchangeData
        let self = this
        return this.exchangeData.filter(function (item) {
          // return item['program'].toLowerCase().trim().indexOf(self.search) !== -1
          for (let key in item) {
            if (typeof item[key] === 'string') {
              if (item[key].toLowerCase().indexOf(self.search.toLowerCase().trim()) !== -1)
                return item
            }
            else if (Array.isArray(item[key])){
              for (let i = 0; i < item[key].length; i++) {
                if (item[key][i].toLowerCase().indexOf(self.search.toLowerCase().trim()) !== -1)
                  return item
              }

            }
          }
        })
      }
    },
    methods: {
      returnString (list) {
        if(typeof list === 'string') return list
        let result = ""
        if (list === undefined || list.length === 0) return result
        for (var i = 0; i < list.length - 1; i++) {
          result += list[i] + ", "
        }
        result += list[list.length - 1]
        return result
      },
      applyFilters() {
        this.filters = !this.filters
      },
      inList(program) {
        for (let i = 0; i < this.shortList.length; i++) {
          if (this.shortList[i] === program) {
            return true
          }
        }
        return false
      },
      addToList(program) {
        this.shortList.push(program)
      },
      removeFromList(program) {
        for (let i = 0; i < this.shortList.length; i++) {
          if (this.shortList[i] === program) {
            this.shortList.splice(i, 1)
          }
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .app-container {
    margin: 0;
  }
  .card {
    margin-bottom: 20px;
  }
  .card-header {
    /*TODO: FIX FONTS AND HEIGHT*/
    font-size: 16px;
    padding: auto 0;
  }
</style>
