/*
export function someGetter (state) {
}
*/
export function getGroup (state) {
  if (state.group === null && typeof window !== 'undefined') {
    if (window.localStorage.getItem('group') !== null) {
      state.group = JSON.parse(window.localStorage.getItem('group'))
    }
  }
  return state.group
}

export function getAdmin (state) {
  if ((state.admin === null || state.admin === false) && typeof window !== 'undefined') {
    if (window.localStorage.getItem('admin') !== null) {
      state.admin = JSON.parse(window.localStorage.getItem('admin'))
    } else {
      state.admin = false
    }
  }
  return state.admin
}
