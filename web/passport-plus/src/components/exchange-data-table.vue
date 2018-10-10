<template>
  <div class="app-container">
    <table class="table table-dark">
      <thead>
      <tr>
        <th v-for="header in table_headers">{{header}}</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <th scope="row">1</th>
        <td>Mark</td>
        <td>Otto</td>
        <td>@mdo</td>
      </tr>
      <tr>
        <th scope="row">2</th>
        <td>Jacob</td>
        <td>Thornton</td>
        <td>@fat</td>
      </tr>
      <tr>
        <th scope="row">3</th>
        <td>Larry</td>
        <td>the Bird</td>
        <td>@twitter</td>
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
      table_headers: {
        'Program': 'program',
        'Host Institution': 'host',
        'Languages': 'languages',
        'Terms': 'terms'
      },
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
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
