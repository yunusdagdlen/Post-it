<template>
  <div class="color-swatches">
    <div class="text-caption text-grey-7 q-mb-sm" v-if="label">{{ label }}</div>
    <div class="row items-center q-gutter-sm">
      <div
        v-for="c in options"
        :key="c"
        class="color-swatch"
        :style="{ background: c, outlineColor: c }"
        :aria-label="'Select color ' + c"
        :class="{ selected: modelValue === c }"
        role="button"
        tabindex="0"
        @click="$emit('update:modelValue', c)"
        @keydown.enter.prevent="$emit('update:modelValue', c)"
      >
        <q-icon v-if="modelValue === c" name="check" color="white" size="16px" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ColorSwatches',
  props: {
    modelValue: { type: String, default: '#4dabf7' },
    options: { type: Array, default: () => [] },
    label: { type: String, default: '' }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.color-swatch {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  cursor: pointer;
  outline: 2px solid transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s ease, outline-color 0.2s ease;
}
.color-swatch:hover {
  transform: scale(1.05);
}
.color-swatch.selected {
  outline: 2px solid rgba(0, 0, 0, 0.25);
}
</style>
