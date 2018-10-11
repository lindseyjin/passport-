<template>
  <div class="form-group">
    <label for=dropdown-select>{{label}} </label>
    <select v-model="selected" @input="event => {$emit('change-selection', event.target.value)}" class="select" id="dropdown-select">
      <option v-for="opt in selectOptions">{{opt}}</option>
    </select>
  </div>
</template>

<script>
  export default {
    name: "Dropdown",
    props: ['label', 'selectOptions'],
    data () {
      return {
        selected: ''
      }
    }
  }
</script>

<style scoped>

</style>
