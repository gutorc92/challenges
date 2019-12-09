<template lang="pug">
  q-page
    div(class="q-pa-md")
      login-form()
</template>

<script>
import { openURL } from 'quasar'
import LoginForm from 'src/components/sign/LoginForm'

export default {
  name: 'Login',
  components: {
    LoginForm
  },
  data () {
    return {
    }
  },
  async created () {
  },
  methods: {
    openURL
  }
}
</script>

<style>
</style>
