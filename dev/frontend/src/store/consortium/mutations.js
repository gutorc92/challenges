/*
export function someMutation (state) {
}
*/
export function setAdmin (state, admin) {
  if (typeof window !== 'undefined') {
    window.localStorage.setItem('admin', JSON.stringify(admin))
  }
  state.admin = admin
}

export function setGroup (state, group) {
  if (typeof window !== 'undefined') {
    window.localStorage.setItem('group', JSON.stringify(group))
  }
  state.group = group
}
