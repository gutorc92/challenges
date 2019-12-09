<template lang="pug">
  q-layout(view="lHh Lpr lFf").bg-grey-10
    .header-login.shadow-7(:class="headerColor || 'bg-grey-7'")
    q-page-container
      router-view
</template>

<script>
import { mapActions } from 'vuex'
import { openURL } from 'quasar'

export default {
  name: 'LoginLayout',
  data () {
    return {
      headerColor: null
    }
  },
  computed: {
    loadedWebSite () {
      return this.$store.getters['context/getLoadWebSite']
    }
  },
  async created () {
    try {
      if (!this.loadedWebSite) {
        this.loadPublicWebSite('menu')
      }
    } catch (err) {
      console.error('error', err)
    }
  },
  methods: {
    openURL,
    ...mapActions({
      loadPublicWebSite: 'context/loadPublicWebSite'
    })
  }
}
</script>

<style>
.header-login{
  height: 40%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
}
</style>
