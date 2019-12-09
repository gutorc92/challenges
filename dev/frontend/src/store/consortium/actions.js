/*
export function someAction (context) {
}
*/
import { api } from 'src/boot/axios'

export async function loadConsortiumGroup ({ commit }, email) {
  try {
    let response = await api.getConsortiumGroup({
      where: { admin: email }
    })
    let group = response ? response.data['_items'][0] : null
    commit('setAdmin', group !== null)
    commit('setGroup', group)
  } catch (err) {
    console.error('err', err)
  }
}
