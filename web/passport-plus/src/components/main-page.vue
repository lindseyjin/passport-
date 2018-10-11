<template>
  <div class="app-container">
    <div class="card">
      <div class="card-header">
        Search Programs
      </div>
      <div class="card-body">
        <div class="input-group input-group-sm mb-3">
          <div class="input-group-prepend">
            <div class="input-group-text border-right-0 border">
              <i class="fa fa-search"></i>
            </div>
          </div>
          <input type="text" v-model="search" class="form-control" placeholder="Search keywords...">
          <div class="input-group-append">
            <span class="input-group-text bg-primary text-white" data-toggle="tooltip" title="Show Filters"
                  style="cursor: pointer;" @click="toggleFiltersTab()">Filter <i class="fas fa-caret-down"></i></span>
          </div>
        </div>
        <div v-if="showFilters" class="card mb-3">
          <div class="card-body inline">
            <dropdown
              v-bind:label="labels[0]"
              v-bind:selectOptions="selectLangOptions"
              v-bind:showNone="true"
              v-bind:clearFilters="clearFilters['lang']"
              v-on:cleared="filtersCleared('lang')"
              v-on:change-selection="setLang"
            ></dropdown>
            <dropdown
              v-bind:label="labels[1]"
              v-bind:selectOptions="selectTermOptions"
              v-bind:showNone="true"
              v-bind:clearFilters="clearFilters['term']"
              v-on:cleared="filtersCleared('term')"
              v-on:change-selection="setTerm"
            ></dropdown>
            <dropdown
              v-bind:label="labels[2]"
              v-bind:selectOptions="selectDestOptions"
              v-bind:showNone="true"
              v-bind:clearFilters="clearFilters['dest']"
              v-on:cleared="filtersCleared('dest')"
              v-on:change-selection="setDest"
            ></dropdown>
            <button type="submit" class="btn btn-info btn-sm" @click="applyFilters">Apply Filters</button>
            <button type="submit" class="btn btn-danger btn-sm" @click="removeFilters">Clear</button>
          </div>
        </div>
      </div>
    </div>
    <br>
    <div class="pagination-row">
      <dropdown
        v-bind:label="pageSelectLabel"
        v-bind:selectOptions="pageOptions"
        v-bind:showNone="false"
        v-on:change-selection="setItemsPerPage"
      ></dropdown>
      <h6 style="margin-right: 15px">Page {{currPage}} of {{totalPages}}</h6>
      <b-pagination class="pagination-info" size="sm" :total-rows="this.filteredTableData.length" v-model="currPage"
                    :per-page="itemsPerPage">
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
        exchangeData: [],
        search: "",
        showFilters: false,
        clearFilters: {
          'term': false,
          'lang': false,
          'dest': false
        },
        isFiltering: false,
        currPage: 1,
        itemsPerPage: 20,
        pageOptions: [20, 50, 100, 200],
        pageSelectLabel: "Items per Page: ",
        labels: [
          'Languages: ',
          'Terms: ',
          'Destinations: '
        ],
        // arrays of selectable filter options
        selectLangOptions: [],
        selectDestOptions: [],
        selectTermOptions: [],
        // currently selected options in search boxes
        selectedLang: '',
        selectedTerm: '',
        selectedDest: '',
        // options being filtered by, not always == currently selected
        filterByLang: '',
        filterByTerm: '',
        filterByDest: ''
      }
    },
    computed: {
      totalPages: function () {
        return Math.ceil(this.filteredTableData.length/this.itemsPerPage)
      },
      pageData: function () {
        let start_index = this.itemsPerPage * (this.currPage - 1)
        let end_index = start_index + this.itemsPerPage
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
          if (self.filterByLang === "" || item['languages'].indexOf(self.filterByLang) !== -1) {
            if (self.filterByDest === "" || item['location'] === self.filterByDest) {
              if (self.filterByTerm === "" || item['terms'].includes(self.filterByTerm)) {
                return item
              }
            }
          }
        })
      },
      filteredTableData: function () {
        let filteredData = this.exchangeData
        let self = this

        if (this.isFiltering === true) {
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
          self.selectDestOptions = self.createListSelectOptions('location')
          self.selectTermOptions = self.createListSelectOptions('terms')
          self.selectLangOptions = self.createListSelectOptions('languages')
        })
        .catch(function (error){
          // console log error message
          console.log(error)
        })
    },
    methods: {
      toggleFiltersTab() {
        this.showFilters = !this.showFilters
      },
      applyFilters() {
        this.isFiltering = true
        this.filterByLang = this.selectedLang
        this.filterByTerm = this.selectedTerm
        this.filterByDest = this.selectedDest
      },
      removeFilters() {
        this.isFiltering = false
        this.clearFilters['term'] = true
        this.clearFilters['lang'] = true
        this.clearFilters['dest'] = true
      },
      filtersCleared(header) {
        this.clearFilters[header] = false
      },
      createListSelectOptions(header) {
        let options = []
        for (let x = 0; x < this.exchangeData.length; x++) {
          if (header === 'terms'){
            let currTerm = this.exchangeData[x][header]
            if (currTerm) {
              for (let y = 0; y < currTerm.length; y++) {
                if (!options.includes(currTerm[y])) {
                  options.push(currTerm[y])
                }
              }
            }
          }
          else {
            if (this.exchangeData[x][header]) {
              if (!options.includes(this.exchangeData[x][header])) {
                options.push(this.exchangeData[x][header])
              }
            }
          }
        }
        return options.sort()
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
        this.itemsPerPage = parseInt(value)
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
</style>
