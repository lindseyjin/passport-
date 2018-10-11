<template>
  <table class="table table-light table-striped">
    <thead>
    <tr>
      <th v-for="tableHeader in tableHeaders">{{tableHeader}}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="item in pageData">
      <td><a :href="item['link']" target="_blank">{{item['program']}}</a></td>
      <td>{{item['host']}}</td>
      <td>{{item['location']}}</td>
      <td>{{item['languages']}}</td>
      <td style="width: 180px"><span v-for="term in item['terms']">{{term}}<br/></span></td>
    </tr>
    </tbody>
  </table>
</template>

<script>
  export default {
    name: "ExchangeInfoTable",
    props: ['pageData'],
    data () {
      return {
        tableHeaders: [
          'Program',
          'Host Institution',
          'Location',
          'Languages',
          'Terms'
        ],
      }
    }
  }
</script>

<style scoped>

</style>
