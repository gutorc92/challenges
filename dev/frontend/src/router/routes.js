
import store from '../store'

const ifAuthenticated = (to, from, next) => {
  console.log('auth', store().getters['user/isAuthenticated'])
  if (store().getters['user/isAuthenticated']) {
    store().dispatch('user/loadUser')
    next()
    return
  }
  next('/login')
}

const ifNotAuthenticated = (to, from, next) => {
  if (!store().getters['user/isAuthenticated']) {
    next()
    return
  }
  next('/user')
}

const routes = [
  {
    path: '/',
    beforeEnter: ifNotAuthenticated,
    component: () => import('layouts/BasicLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') }
    ]
  },
  {
    path: '/login',
    beforeEnter: ifNotAuthenticated,
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      {
        path: '',
        name: 'login',
        component: () => import('pages/sign/Login.vue')
      }
    ]
  },
  {
    path: '/user',
    beforeEnter: ifAuthenticated,
    component: () => import('layouts/LoggedLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/Welcome.vue')
      },
      {
        path: 'heroe',
        component: () => import('pages/Heroe')
      },
      {
        path: 'battle',
        component: () => import('pages/Battle')
      }
    ]
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
