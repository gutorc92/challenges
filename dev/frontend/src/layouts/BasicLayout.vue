<template lang="pug">
  q-layout(view='hHh lpR fFf')
    q-header(elevated reveal :color="style.color.primary")
      q-toolbar
        q-btn(v-if="hasLeftMenu" dense flat round icon='menu' @click='left = !left')
        q-toolbar-title
          span {{style.descriptions.default}}
        q-btn(dense flat round icon='input' @click="$router.push('login')")
    q-drawer(v-if="hasLeftMenu" v-model='left' side='left' bordered)
      q-list.no-padding.no-border
        q-item(v-for="menu in menus" :key="menu.slug" :to="menu.link" exact)
          q-item-section {{menu.name}}
    q-page-container
      router-view
</template>

<script>
import { mapActions } from 'vuex'
import { openURL } from 'quasar'

export default {
  name: 'BasicLayout',
  data () {
    return {
      left: this.$q.platform.is.desktop
    }
  },
  computed: {
    menus () {
      return this.$store.getters['context/getMenu']
    },
    hasLeftMenu () {
      let menu = this.$store.getters['context/getWebSiteMenu']
      return menu === 'left-drawer'
    },
    style () {
      let style = this.$store.getters['context/getStyle']
      if (style === undefined) {
        return { color: { primary: '' }, descriptions: { default: '' } }
      }
      return style
    }
  },
  async created () {
    try {
      this.loadPublicWebSite('menu')
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
</style>
