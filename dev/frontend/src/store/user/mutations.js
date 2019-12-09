/*
export function someMutation (state) {
}
*/

import { LocalStorage, Cookies } from 'quasar'

export function setUser (state, user) {
  if (window.localStorage.getItem('user') === null) {
    window.localStorage.setItem('user', JSON.stringify(user))
  }
  state.user = user
}

export function clearUser (state) {
  state.user = null
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem('user')
  }
  Cookies.remove('token-user')
}

export function setAuthenticated (state, isAuthenticated) {
  LocalStorage.set('isAuthenticated', isAuthenticated)
  state.isAuthenticated = isAuthenticated
}
