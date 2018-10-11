<template>
  <div class="app-container">
    <div class="card">
      <div class="card-header">
        Search Programs
      </div>
      <div class="card-body">
        <div class="input-group input-group-sm mb-3">
          <input type="text" v-model="search" class="form-control" placeholder="Search keywords...">
          <div class="input-group-append">
            <span class="input-group-text" data-toggle="tooltip" title="Show Filters"
                  style="cursor: pointer;" @click="applyFilters()"><i class="fas fa-caret-down"></i></span>
            <button v-if="filters === false" type="submit" class="btn btn-primary"><i class="fa fa-search" aria-hidden="true"></i></button>
          </div>
        </div>
        <div v-if="filters" class="card mb-3">
          <div class="card-body inline">
            <div class="form-group">
              <label for=language-select>Languages: </label>
              <select class="select" id="language-select">
                <option>Mustard</option>
                <option>Ketchup</option>
                <option>Relish</option>
              </select>
            </div>
            <div class="form-group">
              <label for=term-select>Terms: </label>
              <select class="select" id="term-select">
                <option>Fall 2019</option>
                <option>Summer 2019</option>
                <option>Fall 2019 and Spring 2020</option>
                <option>Fall 2019 and Winter 2020</option>
                <option>Spring 2019</option>
                <option>Winter 2020</option>
              </select>
            </div>
            <div class="form-group">
              <label for=dest-select>Destination: </label>
              <select class="select" id="dest-select">
                <option>Fall 2019</option>
                <option>Summer 2019</option>
                <option>Fall 2019 and Spring 2020</option>
                <option>Fall 2019 and Winter 2020</option>
                <option>Spring 2019</option>
                <option>Winter 2020</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="pagination-row">
      <div class="form-group">
        <label for=page-select><h6>Items per Page:</h6></label>
        <select v-model="itemsPerPage" id="page-select">
          <option>20</option>
          <option>50</option>
          <option>100</option>
          <option>200</option>
        </select>
      </div>
      <h6 style="margin-right: 15px">Page {{currPage}} of {{totalPages}}</h6>
      <b-pagination class="pagination-info" size="sm" :total-rows="this.filteredTableData.length" v-model="currPage" :per-page="itemsPerPage">
      </b-pagination>
    </div>
    <table class="table table-light table-striped">
      <thead>
      <tr>
        <th v-for="tableHeader in tableHeaders">{{tableHeader}}</th>
        <th/>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in pageData">
        <td>{{item['location']}}</td>
        <td><a :href="item['link']" target="_blank">{{item['program']}}</a></td>
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
  import ShortList from './short-list'

  export default {
    name: 'ExchangeDataTable',
    components: {ShortList},
    data () {
      return {
        msg: 'Welcome to Your Vue.js App',
        tableHeaders: [
          'Location',
          'Program',
          'Host Institution',
          'Languages',
          'Terms'
        ],
        exchangeData: [],
        search: "",
        filters: false,
        currPage: 1,
        itemsPerPage: 20,
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
      select_terms: function () {

      },
      select_languages: function () {

      },
      select_destination: function () {

      },
      totalPages: function () {
        return Math.ceil(this.filteredTableData.length/this.itemsPerPage)
      },
      pageData: function () {
        let start_index = this.itemsPerPage*(this.currPage - 1)
        let end_index = start_index + this.itemsPerPage
        if (end_index < this.filteredTableData.length) {
          return this.filteredTableData.slice(start_index, end_index)
        }
        else {
          return this.filteredTableData.slice(start_index)
        }
      },
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
    padding: 5px 10px;
  }
  .pagination-row {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    margin-bottom: -10px;
  }
  h6 {
    margin-top: 5px;
    font-size: 14px;
  }
  .form-group {
    margin-right: 15px;
  }
  #page-select {
    height: 25px;
  }
</style>
