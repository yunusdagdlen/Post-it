<template>
  <q-btn
    flat
    dense
    size="sm"
    class="status-chip"
    :color="textColor"
    :icon="icon"
    :label="label"
    @click.stop
  >
    <q-menu anchor="top left" self="bottom left">
      <q-list style="min-width: 160px">
        <q-item clickable v-close-popup @click.stop="select(0)">
          <q-item-section avatar><q-icon name="fiber_new" :color="modelValue===0 ? 'primary' : 'grey-6'" /></q-item-section>
          <q-item-section>New</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click.stop="select(1)">
          <q-item-section avatar><q-icon name="autorenew" :color="modelValue===1 ? 'primary' : 'grey-6'" /></q-item-section>
          <q-item-section>In progress</q-item-section>
        </q-item>
        <q-item clickable v-close-popup @click.stop="select(2)">
          <q-item-section avatar><q-icon name="check_circle" :color="modelValue===2 ? 'primary' : 'grey-6'" /></q-item-section>
          <q-item-section>Done</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script>
export default {
  name: 'StatusPicker',
  props: {
    modelValue: { type: Number, default: 0 }
  },
  emits: ['update:modelValue'],
  computed: {
    label() {
      const s = this.modelValue ?? 0;
      return s === 2 ? 'Done' : (s === 1 ? 'In progress' : 'New');
    },
    icon() {
      const s = this.modelValue ?? 0;
      return s === 2 ? 'check_circle' : (s === 1 ? 'autorenew' : 'fiber_new');
    },
    textColor() {
      return 'grey-9';
    }
  },
  methods: {
    select(val) {
      this.$emit('update:modelValue', val);
    }
  }
}
</script>

<style scoped>
.status-chip {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  min-width: 0 !important;
  text-transform: none !important;
}
.status-chip :deep(.q-btn__content) {
  gap: 6px;
}
.status-chip:hover {
  text-decoration: underline;
}
</style>
