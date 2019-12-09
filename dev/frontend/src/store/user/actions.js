/*
export function someAction (context) {
}
*/
import { Cookies } from 'quasar'
import api from 'src/boot/axios'

export async function loadUser ({ commit, getters }) {
  api.addToken(Cookies.get('token-user'))
}
