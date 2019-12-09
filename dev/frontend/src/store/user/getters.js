/*
export function someGetter (state) {
}
*/
import { LocalStorage } from 'quasar'

export function user (state) {
  if (state.user === null) {
    if (typeof window !== 'undefined' && window.localStorage.getItem('user') !== null) {
      let user = JSON.parse(window.localStorage.getItem('user'))
      return user
    }
  }
  return state.user
}

export function isAuthenticated (state) {
  if (state.isAuthenticated !== null) {
    return state.isAuthenticated
  }
  if (LocalStorage.getItem('isAuthenticated') != null) {
    return LocalStorage.getItem('isAuthenticated')
  }
  return false
}
