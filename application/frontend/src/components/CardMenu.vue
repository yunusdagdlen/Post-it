<template>
  <q-btn rounded flat dense icon="mdi-menu" color="black" @click.stop @touchstart.stop @mousedown.stop @pointerdown.stop>
    <q-menu fit anchor="bottom right" self="top right">
      <div class="row no-wrap q-pa-sm">
        <div class="column">
          <q-btn
            size="sm"
            flat
            outline
            rounded
            align="left"
            color="grey-7"
            icon="edit"
            label="Edit"
            @click="$emit('edit')"
          />
          <q-btn
            flat
            outline
            rounded
            align="left"
            color="grey-7"
            icon="delete"
            label="Delete"
            size="sm"
            @click="$emit('delete')"
          />
          <q-btn
            flat
            outline
            rounded
            align="left"
            color="grey-7"
            icon="block"
            label="Disable"
            size="sm"
            @click="$emit('disable')"
          />
        </div>
      </div>
    </q-menu>
  </q-btn>
</template>

<script>
export default {
  name: 'CardMenu',
  emits: ['edit', 'delete', 'disable']
}
</script>

<style scoped>
</style>
