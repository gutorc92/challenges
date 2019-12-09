<template lang="pug">
  q-layout(view='hHh lpR fFf')
    q-header(elevated reveal :color="style.color.primary")
      q-toolbar
        q-btn(v-if="hasLeftMenu" dense flat round icon='menu' @click='left = !left')
        q-toolbar-title
          span {{style.descriptions.default}}
        q-btn(dense flat round icon='input' @click="logoutUser")
    q-drawer.bg-grey(v-model='left' side='left' bordered)
      q-list.no-padding.no-border
        q-item(v-for="menu in menus" :key="menu.slug" v-if="hasMenuUser(menu)" :to="menu.link" exact)
          q-item-section {{menu.name}}
    q-page-container
      router-view
</template>

<script>
import { mapActions } from 'vuex'
import menuMixin from 'src/components/mixins/menu.mixin'
import { openURL } from 'quasar'

export default {
  name: 'LoggedLayout',
  mixins: [menuMixin],
  data () {
    return {
      left: this.$q.platform.is.desktop
    }
  },
  computed: {
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
      let p = 'nada'
      return p
    } catch (err) {
      console.error('error', err)
    }
  },
  methods: {
    openURL,
    ...mapActions({
      logout: 'context/logout'
    }),
    logoutUser () {
      this.logout()
      this.$router.push({ name: 'login' })
    }
  }
}
</script>

<style>
</style>
