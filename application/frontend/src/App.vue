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
</style>
