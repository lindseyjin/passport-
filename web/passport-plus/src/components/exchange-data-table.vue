<template>
  <div class="app-container">
    <table class="table table-dark">
      <thead>
      <tr>
        <th v-for="table_header in table_headers">{{table_header}}</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in exchange_data">
        <td>{{item['program']}}</td>
        <td>{{item['host']}}</td>
        <td>{{returnString(item['languages'])}}</td>
        <td>{{returnString(item['terms'])}}</td>
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
      if($.type(list) === "string") return list
      let result = ""
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

</style>
