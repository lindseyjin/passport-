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
            <!--TODO: MOVE TO SEPARATE COMPONENT-->
            <div class="form-group">
              <label for=language-select>Languages: </label>
              <select v-model="selectedLang" id="language-select">
                <option v-for="lang in selectLangs">{{lang}}</option>
              </select>
            </div>
            <div class="form-group">
              <label for=term-select>Terms: </label>
              <select v-model="selectedTerm" class="select" id="term-select">
                <option v-for="term in selectTerms">{{term}}</option>
              </select>
            </div>
            <div class="form-group">
              <label for=dest-select>Destination: </label>
              <select v-model="selectedDest" class="select" id="dest-select">
                <option v-for="dest in selectDests">{{dest}}</option>
              </select>
            </div>
            <button type="submit" class="btn btn-info btn-sm" @click="applyFilters">Apply Filters</button>
            <button type="submit" class="btn btn-danger btn-sm" @click="clearFilters">Clear</button>
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
    <exchange-info-table v-bind:pageData="pageData"></exchange-info-table>
  </div>
</template>

<script>
  import axios from 'axios'
  import ShortList from './short-list'
  import ExchangeInfoTable from './exchange-info-table'

  export default {
    name: 'MainPage',
    components: {ShortList, ExchangeInfoTable},
    data () {
      return {
        msg: 'Welcome to Your Vue.js App',
        exchangeData: [],
        search: "",
        filters: false,
        currPage: 1,
        itemsPerPage: 20,
        shortList: [],
        filtering: false,
        selectedLang: '',
        selectedTerm: '',
        selectedDest: ''
      }
    },
    mounted () {
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
      selectTerms: function () {
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
      selectLangs: function () {
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
      selectDests: function () {
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
