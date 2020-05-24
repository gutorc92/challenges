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
              q-item-section(avatar)
                q-icon(:name="heroe.allocated ? 'checked' : 'clear'")
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
import cloneDeep from 'lodash/cloneDeep'
import findIndex from 'lodash/findIndex'
import find from 'lodash/find'
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
      heroes: [],
      dangerToClass: {
        'Tiger': 'A',
        'Dragon': 'S',
        'Wolf': 'B',
        'God': 'C'
      },
      oldBattle: null,
      battle: {
        heroes: [],
        dangerLevel: '',
        monsterName: '',
        location: []
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
      this.battle = data
      this.saveBatle()
    })
  },
  methods: {
    async saveBatle () {
      if (this.oldBattle !== null && this.oldBattle.heroes.length() !== 0) {
        map(this.oldBattle.heroes, (heroe) => {
          let index = findIndex(this.heroes, { '_id': heroe._id })
          this.heroes[index].alocated = false
        })
      }
      let heroe = find(this.heroes, { alocated: false, class: this.dangerToClass[this.battle.dangerLevel] })
      let index = findIndex(this.heroes, { '_id': heroe._id })
      this.heroes[index].alocated = true
      this.battle.heroes.push(heroe)
      try {
        await this.$eve.postBattle({
          heroes: [heroe._id],
          dangerLevel: this.battle.dangerLevel,
          monsterName: this.battle.monsterName
        })
        this.oldBattle = cloneDeep(this.battle)
      } catch (err) {
        console.log('err')
      }
    }
  }
}
</script>
