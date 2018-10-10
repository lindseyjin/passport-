<template>
  <div class="container">
    <div class="row">
      <h1>Passport</h1>
      <h1 id="plus">+</h1>
    </div>
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App'
  }
</script>

<style>
  body {
    background-image: url("../static/img/notebook.png");
    font-family: 'Lato', sans-serif;
    font-size: 14px;
  }
  h1 {
    font-family: 'Architects Daughter', cursive;
    font-size: 60px;
    margin: 30px 15px;
  }
  #plus {
    color: #1d7b35;
  }
</style>
