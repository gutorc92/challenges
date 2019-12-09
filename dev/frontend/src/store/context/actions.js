/*
export function someAction (context) {
}
*/
import { api } from 'src/boot/axios'

export async function loadPublicWebSite ({ commit, dispatch }, place) {
  try {
    if (typeof window !== 'undefined') {
      const hostname = window.location.hostname
      let response = await api.getWebsitePublic({
        where: { url: hostname }
      })
      let website = response.data['_items'][0]
      const menus = website.modules.public.find(v => v.place === place)
      let modules = []
      for (let moduleSite of menus.items) {
        modules.push(moduleSite.item)
      }
      response = await api.getModules({
        where: { slug: { $in: modules } }
      })
      let menusModules = []
      for (let moduleSite of menus.items.sort((a, b) => a.order - b.order)) {
        let item = moduleSite.item
        let menuItem = response.data['_items'].find(v => v.slug === item)
        menusModules.push(menuItem)
      }
      const responseStyle = await api.getStyle({
        where: { slug: website.style }
      })
      let style = responseStyle.data['_items'][0]
      commit('setWebsite', website)
      commit('setMenu', menusModules)
      commit('setStyle', style)
      commit('setLoadWebSite', true)
    }
  } catch (err) {
    console.error('err', err)
  }
}

export async function loadStyle ({ commit, getters }, eve) {
  try {
    let response = await eve.getStyle({
      where: { slug: getters['getWebSiteSlug'] }
    })
    let style = response.data['_items'][0]
    commit('setStyle', style)
  } catch (err) {
    console.error('err', err)
  }
}

export async function loadPrivateWebSite ({ commit }, menuPosition) {
  try {
    if (typeof window !== 'undefined') {
      const hostname = window.location.hostname
      let response = await api.getWebsitePrivate({
        where: { url: hostname }
      })
      let website = response.data['_items'][0]
      let menusPrivate = website.modules.private.find(v => v.place === menuPosition)
      const menus = menusPrivate
      let modules = []
      for (let moduleSite of menus.items) {
        modules.push(moduleSite.item)
      }
      response = await api.getModules({
        where: { slug: { $in: modules } }
      })
      let menusModules = []
      for (let moduleSite of menus.items.sort((a, b) => a.order - b.order)) {
        let item = moduleSite.item
        let menuItem = response.data['_items'].find(v => v.slug === item)
        menusModules.push(menuItem)
      }
      const responseStyle = await api.getStyle({
        where: { slug: website.style }
      })
      let style = responseStyle.data['_items'][0]
      commit('setMenu', menusModules)
      commit('setWebsite', website)
      commit('setStyle', style)
    }
  } catch (err) {
    console.error('err', err)
  }
}

export async function logout ({ state, commit, dispatch, rootState }) {
  try {
    await api.postUserLogout({
      email: rootState.user.email,
      website: state.website.slug,
      location: {}
    }, '')
    commit('user/clearUser')
    dispatch('loadPublicWebSite', 'menu')
  } catch (err) {
    console.error('logout error', err)
  }
}
