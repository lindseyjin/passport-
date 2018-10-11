<template>
  <div class="form-group">
    <label for=dropdown-select>{{label}} </label>
    <select v-model="selected" @input="event => {$emit('change-selection', event.target.value)}" class="select" id="dropdown-select">
      <option v-if="showNone" value="" selected class="text-gray"></option>
      <option v-for="opt in selectOptions">{{opt}}</option>
    </select>
  </div>
</template>

<script>
  export default {
    name: "Dropdown",
    props: ['label', 'selectOptions', 'showNone', 'clearFilters'],
    data () {
      return {
        selected: ''
      }
    },
    watch: {
      clearFilters: function () {
        if (this.clearFilters === true) {
          this.clearSelected()
          this.$emit('cleared')
        }
      }
    },
    methods: {
      clearSelected () {
        this.selected = ''
      }
    }
  }
</script>

<style scoped>
  select {
    height: 25px;
    margin-right: 20px;
  }
  .text-gray {
    color: gray;
  }
</style>
