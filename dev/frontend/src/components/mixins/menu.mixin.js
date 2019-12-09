import includes from 'lodash/includes'
export default {
  computed: {
    menus () {
      return this.$store.getters['context/getMenu']
    },
    plan () {
      let plan = this.$store.getters['context/getPlan']
      if (plan === undefined) {
        return { color: { primary: '' } }
      }
      return plan
    }
  },
  methods: {
    hasMenu (menu) {
      return includes(this.plan.permission.modules.admin, menu.slug)
    },
    hasMenuUser (menu) {
      return includes(this.plan.permission.modules.desktop, menu.slug)
    }
  }
}
