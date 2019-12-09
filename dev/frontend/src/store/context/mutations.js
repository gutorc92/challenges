import { LocalStorage } from 'quasar'

export function setWebsite (state, website) {
  state.website = website
  LocalStorage.set('website', website)
}

export function setStyle (state, style) {
  LocalStorage.set('style', style)
  state.style = style
}

export function setPublicModules (state, modules) {
  LocalStorage.set('publicModules', modules)
  state.publicModules = modules
}

export function setPrivateModules (state, modules) {
  LocalStorage.set('privateModules', modules)
  state.privateModules = modules
}

export function setPlan (state, plan) {
  LocalStorage.set('plan', plan)
  state.plan = plan
}

export function setMenu (state, menu) {
  if (Array.isArray(menu)) {
    LocalStorage.set('menu', JSON.stringify(menu))
    state.menu = menu
  }
}

export function setLoadWebSite (state, load) {
  LocalStorage.set('loadWebSite', load)
  state.loadWebSite = load
}
