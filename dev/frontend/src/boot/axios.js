import axios from 'axios'
import Api from 'axios-eve'

export const api = new Api({
  urls: [
    {
      'url': 'style',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'modules',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'website/public',
      'type': 'eve',
      'methods': ['GET']
    },
    {
      'url': 'website/private',
      'type': 'eve',
      'methods': ['GET', 'POST']
    },
    {
      'url': 'user/auth',
      'type': 'eve',
      'methods': ['POST']
    },
    {
      'url': 'user/logout',
      'type': 'eve',
      'methods': ['POST']
    },
    {
      'url': 'user/login',
      'type': 'eve',
      'methods': ['GET']
    },
    {
      'url': 'user/admin',
      'type': 'eve',
      'methods': ['POST']
    },
    {
      'url': 'user/list',
      'type': 'eve',
      'methods': ['GET', 'PATCH']
    },
    {
      'url': 'posts',
      'type': 'eve',
      'methods': ['GET', 'POST']
    },
    {
      'url': 'base',
      'type': 'eve',
      'methods': ['GET', 'POST']
    },
    {
      'url': 'source',
      'type': 'eve',
      'methods': ['GET']
    },
    {
      'url': 'federation',
      'type': 'eve',
      'methods': ['GET', 'POST']
    },
    {
      'url': 'consortium',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'consortium/group',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'research',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'questions',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'plan',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'permission',
      'type': 'eve',
      'methods': ['GET', 'POST', 'PATCH']
    },
    {
      'url': 'heroe',
      'type': 'eve',
      'methods': ['GET', 'POST']
    },
    {
      'url': 'battle',
      'type': 'eve',
      'methods': ['GET', 'POST']
    }
  ],
  baseURL: process.env.API || 'http://localhost:8000',
  headers: {
    'Cache-Control': 'no-cache'
  },
  auth: {
    username: process.env.USER_API || 'admin',
    password: process.env.PASS || 'admin'
  },
  timeout: 1500
})

export default async ({ Vue }) => {
  Vue.prototype.$axios = axios
  Vue.prototype.$eve = api
}
