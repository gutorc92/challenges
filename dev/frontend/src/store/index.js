import Vue from 'vue'
import Vuex from 'vuex'
import VueSocketIO from 'vue-socket.io'
// import example from './module-example'
import user from './user'
import context from './context'

Vue.use(Vuex)
/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      // example
      user,
      context
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  })
  Vue.use(new VueSocketIO({
    debug: true,
    connection: 'https://zrp-challenge-socket.herokuapp.com:443',
    vuex: {
      Store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_'
    }
  }))
  return Store
}
