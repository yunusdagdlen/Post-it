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
.app-layout {
  background: linear-gradient(135deg, #f7f9fc 0%, #eef2f7 100%);
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
