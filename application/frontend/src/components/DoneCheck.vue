<template>
  <q-icon
    v-if="show"
    name="check_circle"
    :color="color"
    :size="size"
    @click.stop.prevent
  >
    <q-tooltip anchor="top middle" self="bottom middle" class="bg-grey-9 text-white">{{ tooltip }}</q-tooltip>
  </q-icon>
</template>

<script>
export default {
  name: 'DoneCheck',
  props: {
    show: { type: Boolean, default: false },
    color: { type: String, default: 'black' },
    size: { type: String, default: '20px' },
    tooltip: { type: String, default: 'congrats you finished this' }
  }
}
</script>

<style scoped>
</style>
