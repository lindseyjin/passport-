import Vue from 'vue'
import Router from 'vue-router'
import ExchangeDataTable from '@/components/exchange-data-table'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ExchangeDataTable',
      component: ExchangeDataTable
    }
  ]
})
