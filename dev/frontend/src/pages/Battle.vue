<template lang="pug">
  q-page.fit.row.wrap.justify-center.items-start.content-start
    q-splitter.col-10(v-model="splitterModel")
      template(v-slot:before)
        q-card.full-width(flat)
          q-card-section
            q-item-label.text.h5 Heróis
          q-card-section
            q-item(v-for="heroe in heroes" :key="heroe._id")
              q-item-section {{heroe.name}}
              q-item-section {{heroe.class}}
      template(v-slot:after)
        q-card.full-width(flat)
          q-card-section
            q-item-label.text.h5 Ameaças
          q-card-section
            q-item
              q-item-section {{battle.monsterName}}
              q-item-section {{battle.dangerLevel}}
</template>

<script>
import map from 'lodash/map'
import extend from 'lodash/extend'

export default {
  name: 'Battle',
  sockets: {
    connect: () => {
      console.log('socket connected')
    }
  },
  data () {
    return {
      splitterModel: 50,
      battle: {
        dangerLevel: '',
        monsterName: '',
        location: [],
        heroes: []
      }
    }
  },
  watch: {
    battle: {
      deep: true,
      handler: (newValue, oldValue) => {
        console.log('newValue', newValue)
      }
    }
  },
  async created () {
    let response = await this.$eve.getHeroe({})
    let heroes = []
    heroes = map(response.data['_items'], (element) => {
      return extend({}, element, { alocated: false })
    })
    this.heroes = heroes
    this.sockets.subscribe('occurrence', (data) => {
      console.log('data', data)
      this.battle = data
    })
  },
  methods: {
    async saveBatle () {
      await this.$eve.postBattle({})
    }
  }
}
</script>
