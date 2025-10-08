<template>
  <q-layout view="lHh Lpr lFf" class="app-layout">
    <router-view />
  </q-layout>
</template>

<script>
import { ref } from "vue";

export default {
  name: "LayoutDefault",

  components: {},

  setup() {
    return {
      leftDrawerOpen: ref(false),
    };
  },
};
</script>

<style>
html, body, #app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", sans-serif;
}
* { font-family: inherit; }

.app-layout {
  background: 
    linear-gradient(to right, #e0e0e0 1px, transparent 1px),
    linear-gradient(to bottom, #e0e0e0 1px, transparent 1px);
  background-color: #f5f5f5;
  background-size: 20px 20px;
  min-height: 100vh;
  color: #2f3542;
}

/* Ensure SweetAlert2 overlays atop Quasar layout/components */
.swal2-container {
  z-index: 30000 !important;
}
.swal2-container .swal2-popup {
  z-index: 30001 !important;
}
</style>
