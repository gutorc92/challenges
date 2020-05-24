<template lang="pug">
  div
    q-card(flat)
      q-card-section
        q-item-label.text-h5 Cadastro de Herói
      q-card-section
        q-input(
          v-model="name"
          :rules="[val => !!val || 'Um nome é necessário']"
          label="Nome")
        q-select(
          v-model="classHeroe"
          label="Classe"
          :options="options"
        )
      q-card-actions
        q-btn(@click="register" color="green") Salvar
    q-card(flat)
      q-card-section
        q-item-label.text-h5 Força
      q-card-section
        q-item(v-for="heroe in heroes" :key="heroe._id")
          q-item-section {{heroe.name}}
          q-item-section {{heroe.class}}
          q-item-section
            div(class="q-pa-md q-gutter-sm")
              q-btn(round color="amber" icon="update" )
              q-btn(icon="remove_circle" round)
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'HeroeForm',
  data () {
    return {
      name: '',
      classHeroe: '',
      alert: false,
      confirm: false,
      error: '',
      heroes: [],
      totalPages: 5,
      page: 1,
      options: ['S', 'A', 'B', 'C']
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
        let response = await this.$eve.getHeroe({})
        this.heroes = response.data['_items']
        this.totalPages = response.data['_meta']['total']
      } catch (err) {
        console.error('error', err)
      }
    },
    async register () {
      try {
        this.$eve.postHeroe({
          name: this.name,
          class: this.classHeroe
        })
        this.$q.notify({
          message: 'Herói cadastrado com sucesso'
        })
        this.fetchData()
        this.name = ''
        this.classHeroe = ''
      } catch (err) {
        this.alert = true
        this.error = 'Usuário ou senha estão incorretos'
        console.error('err', err)
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
