<template lang="pug">
  q-page.relative-position(ref="scrollTargetRef")
    span teste
</template>

<style>
</style>

<script>
export default {
  name: 'Welcome',
  data () {
    return {
      search: '',
      bases: [],
      loading: true,
      total: 2
    }
  },
  async created () {
    this.loading = true
    this.loading = false
  },
  methods: {
  }
}
</script>
<style lang="css">
.data-card{
  cursor: default;
  box-shadow: 3px 3px 3px rgba(0,0,0,0.05);
  -webkit-transition: all 200ms ease-in-out;
  -moz-transition: all 200ms ease-in-out;
  -ms-transition: all 200ms ease-in-out;
  -o-transition: all 200ms ease-in-out;
  transition: all 200ms ease-in-out;
}
.data-card:hover{
  box-shadow: 6px 6px 10px rgba(0,0,0,0.2);
}
</style>
