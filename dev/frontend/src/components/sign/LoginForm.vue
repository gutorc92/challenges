<template lang="pug">
  q-card.shadow-10.login-box(:class="loginFormType")
    q-card-section
      q-item
        q-item-section Login
    q-card-section
      q-item
        q-item-section
          q-input(v-model="email" type="email" label="Email"
            filled
            color="teal")
    q-card-section
      q-item
        q-item-section
          q-input(v-model="password" :type="isPwd ? 'password' : 'text'" label="Senha"
            filled
            @keyup.enter.native="login()"
            color="teal")
            template(v-slot:append)
              q-icon(
                :name="isPwd ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="isPwd = !isPwd")
    q-card-section
      q-item
        q-item-section
          q-btn.full-width(label="Acessar" @click="login" color="primary")
    q-card-section.no-padding.no-margin
      q-item.no-padding.no-margin
        q-item-section.no-padding
          q-btn.full-width(label="Voltar" to="/" flat color="grey")
        q-item-section.no-padding
          q-btn.full-width(label="Redefinir Senha" to="/" flat color="grey")
    q-dialog(v-model='alert')
      q-card
        q-card-section
          .text-h6 Ocorreu um problema
        q-card-section
          | {{error}}
        q-card-actions(align='right')
          q-btn(flat='', label='OK', color='primary', v-close-popup='')
    q-dialog(v-model='confirm')
      q-card
        q-card-section
          .text-h6 Escolha de dashboard
        q-card-section
          | Você tem acesso administrativo e de usuário. Qual vc deseja acessar?
        q-card-actions(align='right')
          q-btn(flat='', label='Admin', color='primary', @click="loginAdmin")
          q-btn(flat='', label='Usuário', color='primary', @click="loginAdmin('admin')")
</template>

<script>
import pick from 'lodash/pick'
import { mapActions } from 'vuex'
export default {
  name: 'LoginForm',
  data () {
    return {
      email: '',
      password: '',
      isPwd: true,
      alert: false,
      confirm: false,
      loginFormType: 'login-right',
      error: ''
    }
  },
  computed: {
    slugWebSite () {
      return this.$store.getters['context/getWebSiteSlug']
    }
  },
  async created () {
    await this.fetchData()
  },
  methods: {
    ...mapActions({
      loadPrivateWebSite: 'context/loadPrivateWebSite'
    }),
    async fetchData () {
      try {
        let p = 'nada'
        return p
      } catch (err) {
        console.error('error', err)
      }
    },
    async login () {
      // let ip = await this.$axios.get(`${window.location.protocol}//ipinfo.io/json`)
      // try {
      //   let loc = { type: 'Point', coordinates: ip.data.loc.split(',').map(parseFloat).reverse() }
      //   ip.data.loc = loc
      // } catch (e) {}
      let ip = {
        'ip': '189.6.24.87',
        'loc': {
          'type': 'Point',
          'coordinates': [-43.2192, -22.8305]
        },
        'country': 'BR',
        'region': 'Federal District',
        'city': 'Brasília'
      }
      try {
        const hostname = this.slugWebSite !== undefined ? this.slugWebSite : ''
        const response = await this.$eve.postUserAuth({
          email: this.email,
          website: hostname,
          location: pick(ip.data, ['country', 'city', 'region', 'ip', 'loc'])
        }, '', { 'pswdtk': this.password })
        let plan = response.data.plan
        this.$q.cookies.set('token-user', response.data.token)
        this.$eve.addToken(response.data.token)
        const responseData = await this.$eve.getUserLogin({
          where: { email: response.data.email }
        })
        if (!responseData || responseData.data['result'] === false) {
          this.alert = true
          this.error = 'Não logou'
          return false
        }
        if ('_items' in responseData.data) {
          let user = responseData.data._items[0]
          this.$store.commit('user/setUser', user)
          this.$store.commit('context/setPlan', plan)
          this.$store.commit('user/setAuthenticated', true)
          if (plan.admin_permission) {
            this.confirm = true
          } else {
            this.loginAdmin()
          }
        }
      } catch (err) {
        this.alert = true
        this.error = 'Usuário ou senha estão incorretos'
        console.error('err', err)
      }
    },
    async loginAdmin (interfaceUser = 'user') {
      if (interfaceUser === 'user') {
        await this.loadPrivateWebSite('menu-user')
        this.$router.push('/user')
      } else {
        await this.loadPrivateWebSite('menu')
        this.$router.push('/admin')
      }
    }
  }
}
</script>

<style>
.login-box{
  max-width: 100%;
  width: 400px;
  position: absolute;
  top: calc(50% - (324px / 2));
}
.login-center{
  right: calc(50% - 200px);
}
.login-right{
  right: 10%;
}
@media screen and (max-width: 600px) {
  .login-box{
    right: 16px;
    left: 16px;
    width: auto;
  }
}
</style>
