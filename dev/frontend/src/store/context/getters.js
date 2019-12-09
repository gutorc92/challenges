/*
export function someGetter (state) {
}
*/
import { LocalStorage } from 'quasar'

export function getLoadWebSite (state) {
  if ((state.loadWebSite === null || state.loadWebSite === false) && typeof window !== 'undefined') {
    if (LocalStorage.getItem('loadWebSite') !== null) {
      return LocalStorage.getItem('loadWebSite')
    } else {
      return false
    }
  }
  return state.loadWebSite
}

export function getMenu (state) {
  if (state.menu === null && typeof window !== 'undefined') {
    if (window.localStorage.getItem('menu') !== null) {
      return JSON.parse(window.localStorage.getItem('menu'))
    }
  }
  return state.menu
}

export function getWebSiteSlug (state) {
  let website = state.website
  if (website === null && typeof window !== 'undefined') {
    if (LocalStorage.getItem('website') !== null) {
      website = LocalStorage.getItem('website')
    }
  }
  console.log('website', website)
  if (website === null || website === undefined) {
    return undefined
  }
  if ('slug' in website) {
    return website.slug
  }
  return undefined
}

export function getWebSiteMenu (state) {
  if (state.website === null || state.website === undefined) {
    return undefined
  }
  return state.website.menu.type
}

export function getToolbar (state) {
  if (state.website === null || state.website === undefined) {
    return undefined
  }
  return state.website.menu.type
}

export function getStyle (state) {
  if (state.style === null || state.style === undefined) {
    return LocalStorage.getItem('style')
  }
  return state.style
}

export function getPlan (state) {
  if (state.plan === null || state.plan === undefined) {
    return LocalStorage.getItem('plan')
  }
  return state.plan
}

export function getMainComponent (state) {
  if (state.website === null || state.website === undefined) {
    return ''
  }
  return state.website.components.main
}
