<template lang="pug">
  q-page.fit.row.wrap.justify-center.items-start.content-start
    heroe-form.col-6()
</template>

<script>
import HeroeForm from 'src/components/heroe/HeroeForm'
export default {
  name: 'Heroe',
  components: {
    HeroeForm
  }
}
</script>
