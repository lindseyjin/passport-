<template>
  <div class="app-container">
    <div class="card">
      <div class="card-header">
        Search Programs
      </div>
      <div class="card-body">
        <form class="form-search">
          <div class="input-append">
            <input type="text" v-model="search" class="span2 search-query">
            <button type="submit" class="btn btn-search" @click="updateSearch(search)">Search</button>
          </div>
        </form>
      </div>
    </div>
    <table class="table table-light table-striped table-bordered table-responsive">
      <thead>
      <tr>
        <th v-for="table_header in table_headers">{{table_header}}</th>
        <th/>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in exchange_data">
        <td>{{item['program']}}</td>
        <td>{{item['host']}}</td>
        <td>{{returnString(item['languages'])}}</td>
        <td>{{returnString(item['terms'])}}</td>
        <td><i class="fa fa-plus" aria-hidden="true"></i></td>
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
        table_headers: [
          'Program',
          'Host Institution',
          'Languages',
          'Terms'
        ],
        exchange_data: []
      }
    },
    mounted () {
      // Todo: move to services
      let self = this
      axios.get('http://127.0.0.1:5000/exchanges')
        .then(function (response) {
          console.log("successful get request")
          self.exchange_data = response.data
        })
        .catch(function (error){
          // console log error message
          console.log(error)
        })
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
  .btn {
    height: 26px;
  }
  .card-header {
    /*TODO: FIX FONTS AND HEIGHT*/
  }
</style>
