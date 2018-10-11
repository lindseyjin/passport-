<template>
  <table class="table table-light table-striped">
    <thead>
    <tr>
      <th v-for="tableHeader in tableHeaders">{{tableHeader}}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="item in pageData">
      <td>{{item['location']}}</td>
      <td><a :href="item['link']" target="_blank">{{item['program']}}</a></td>
      <td>{{item['host']}}</td>
      <td>{{item['languages']}}</td>
      <td>{{returnString(item['terms'])}}</td>
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
          'Location',
          'Program',
          'Host Institution',
          'Languages',
          'Terms'
        ],
      }
    },
    methods: {
      returnString (list) {
        let result = ""
        if (list === undefined || list.length === 0) return result
        for (let i = 0; i < list.length - 1; i++) {
          result += list[i] + ", "
        }
        result += list[list.length - 1]
        return result
      }
    }
  }
</script>

<style scoped>

</style>
