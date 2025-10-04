<template>
  <q-rating
    :model-value="modelValue"
    :max="max"
    :size="size"
    color="amber"
    void-color="grey-4"
    icon="star_border"
    icon-selected="star"
    no-half
    aria-label="Rank by stars"
    class="minimal-stars"
    @update:model-value="$emit('update:modelValue', $event)"
    @click.stop
    @mousedown.stop
    @touchstart.stop
    @pointerdown.stop
  />
</template>

<script>
export default {
  name: 'MinimalStars',
  props: {
    modelValue: { type: Number, default: 1 },
    max: { type: Number, default: 5 },
    size: { type: String, default: '28px' }
  },
  emits: ['update:modelValue']
};
</script>

<style scoped>
.minimal-stars :deep(.q-rating__icon) {
  text-shadow: none !important;
  box-shadow: none !important;
  filter: none !important;
}
.minimal-stars :deep(.q-focus-helper) {
  box-shadow: none !important;
}
</style>
