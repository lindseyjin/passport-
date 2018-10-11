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
                  style="cursor: pointer;" @click="toggleFiltersTab()"><i class="fas fa-caret-down"></i></span>
            <button v-if="filters === false" type="submit" class="btn btn-primary"><i class="fa fa-search" aria-hidden="true"></i></button>
          </div>
        </div>
        <div v-if="filters" class="card mb-3">
          <div class="card-body inline">
            <dropdown
              v-bind:label="labels[0]"
              v-bind:selectOptions="selectLangs"
              v-on:change-selection="setLang"
            ></dropdown>
            <dropdown
              v-bind:label="labels[1]"
              v-bind:selectOptions="selectTerms"
              v-on:change-selection="setTerm"
            ></dropdown>
            <dropdown
              v-bind:label="labels[2]"
              v-bind:selectOptions="selectDests"
              v-on:change-selection="setDest"
            ></dropdown>
            <button type="submit" class="btn btn-info btn-sm" @click="applyFilters">Apply Filters</button>
            <button type="submit" class="btn btn-danger btn-sm" @click="clearFilters">Clear</button>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="pagination-row">
      <dropdown
        v-bind:label="pageSelectLabel"
        v-bind:selectOptions="pageOptions"
        v-on:change-selection="setItemsPerPage"
      ></dropdown>
      <h6 style="margin-right: 15px">Page {{currPage}} of {{totalPages}}</h6>
      <b-pagination class="pagination-info" size="sm" :total-rows="this.filteredTableData.length" v-model="currPage" :per-page="itemsPerPage">
      </b-pagination>
    </div>
    <exchange-info-table
      v-bind:pageData="pageData"
    ></exchange-info-table>
  </div>
</template>

<script>
  import axios from 'axios'
  import Dropdown from './dropdown'
  import ExchangeInfoTable from './exchange-info-table'

  export default {
    name: 'MainPage',
    components: {Dropdown, ExchangeInfoTable},
    data () {
      return {
        msg: 'Welcome to Your Vue.js App',
        exchangeData: [],
        search: "",
        filters: false,
        currPage: 1,
        itemsPerPage: 20,
        pageSelectLabel: "Items per Page: ",
        pageOptions: [20, 50, 100, 200],
        shortList: [],
        filtering: false,
        labels: [
          'Languages: ',
          'Terms: ',
          'Destinations: '
        ],
        selectDestVals: [],
        selectLangVals: [],
        selectTermVals: [],
        selectedLang: '',
        selectedTerm: '',
        selectedDest: ''
      }
    },
    computed: {
      totalPages: function () {
        return Math.ceil(this.filteredTableData.length/this.itemsPerPage)
      },
      pageData: function () {
        let start_index = parseInt(this.itemsPerPage)*(this.currPage - 1)
        let end_index = start_index + parseInt(this.itemsPerPage)
        if (end_index < this.filteredTableData.length) {
          return this.filteredTableData.slice(start_index, end_index)
        }
        else {
          return this.filteredTableData.slice(start_index)
        }
      },
      addFiltersData: function () {
        let self = this
        return this.exchangeData.filter(function (item) {
          if (self.selectedLang === "" || item['languages'].indexOf(self.selectedLang) !== -1) {
            if (self.selectedDest === "" || item['location'] === self.selectedDest) {
              if (self.selectedTerm === "" || item['terms'].includes(self.selectedTerm)) {
                return item
              }
            }
          }
        })
      },
      filteredTableData: function () {
        let filteredData = this.exchangeData
        let self = this

        if (this.filtering === true) {
          filteredData = this.addFiltersData
        }
        // filter by search
        if (this.search !== "") {
          return filteredData.filter(function (item) {
            for (let key in item) {
              if (key === 'terms') {
                for (let i = 0; i < item[key].length; i++) {
                  if (item[key][i].toLowerCase().indexOf(self.search.toLowerCase().trim()) !== -1)
                    return item
                }
              }
              else if (key !== 'link') {
                if (item[key].toLowerCase().indexOf(self.search.toLowerCase().trim()) !== -1)
                  return item
              }
            }
          })
        }
        return filteredData
      }
    },
    mounted () {
      let self = this
      axios.get('http://127.0.0.1:5000/exchanges')
        .then(function (response) {
          console.log("successful get request")
          self.exchangeData = response.data
          self.selectDestVals = self.selectDests()
        })
        .catch(function (error){
          // console log error message
          console.log(error)
        })
    },
    methods: {
      toggleFiltersTab() {
        this.filters = !this.filters
      },
      applyFilters() {
        this.filtering = true
      },
      clearFilters() {
        this.filtering = false
        this.selectedLang = this.selectedTerm = this.selectedDest = ""
      },
      selectTerms () {
        let terms = []
        for (let x = 0; x < this.exchangeData.length; x++) {
          let currTerm = this.exchangeData[x]['terms']
          if (currTerm) {
            for (let y = 0; y < currTerm.length; y++) {
              if (!terms.includes(currTerm[y])) {
                terms.push(currTerm[y])
              }
            }
          }
        }
        return terms
      },
      selectLangs () {
        let langs = []
        for (let x = 0; x < this.exchangeData.length; x++) {
          if (this.exchangeData[x]['languages']) {
            if (!langs.includes(this.exchangeData[x]['languages'])) {
              langs.push(this.exchangeData[x]['languages'])
            }
          }
        }
        return langs
      },
      selectDests () {
        let dests = []
        for (let x = 0; x < this.exchangeData.length; x++) {
          if (this.exchangeData[x]['location']) {
            if (!dests.includes(this.exchangeData[x]['location'])) {
              dests.push(this.exchangeData[x]['location'])
            }
          }
        }
        return dests
      },
      setLang(value) {
        this.selectedLang = value
      },
      setTerm(value) {
        this.selectedTerm = value
      },
      setDest(value) {
        this.selectedDest = value
      },
      setItemsPerPage(value) {
        this.itemsPerPage = value
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
  form{
    display:inline-block;
  }
  .form-group {
    margin-right: 15px;
  }
  #page-select {
    height: 25px;
  }
</style>
