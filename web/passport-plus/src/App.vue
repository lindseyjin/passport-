<template>
  <div class="container">
    <div class="row">
      <h1>Passport</h1>
      <h1 id="plus">+</h1>
    </div>
  <exchange-data-table></exchange-data-table>
  </div>
</template>

<script>
  import ExchangeDataTable from './components/exchange-data-table'
  export default {
    name: 'App',
    components: {ExchangeDataTable}
  }
</script>

<style>
  body {
    background-image: url("../static/img/notebook.png");
    font-family: 'Lato', sans-serif;
    font-size: 13px;
  }
  h1 {
    font-family: 'Architects Daughter', cursive;
    font-size: 65px;
  }
  .row {
    margin: 30px 0 20px;
  }
  #plus {
    color: #1d7b35;
  }
</style>
