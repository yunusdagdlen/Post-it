<template class="q-px-xl">
  <div class="home fullscreen scroll">
    <div class="page-header q-mb-xl full-width bg-white">
      <page-header @success="fetchAllNotes" />
    </div>

    <div
      class="row q-col-gutter-lg"
      style="display: flex; align-items: baseline; justify-content: center"
    >
      <template v-for="postit in this.postitList" :key="postit">
        <postit-card :postit="postit" @ok="fetchAllNotes" />
      </template>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import PageHeader from "@/components/PageHeader.vue";
import axios from "axios";
import PostitCard from "@/components/PostitCard.vue";

export default {
  name: "HomeView",
  components: {
    PostitCard,
    PageHeader,
  },
  data() {
    return {
      postitList: [],
    };
  },
  methods: {
    fetchAllNotes() {
      // const axiosInstance = axios.create({
      //   timeout: 45000,
      //   headers: {
      //     "Access-Control-Allow-Origin": "*",
      //     "Access-Control-Allow-Methods":
      //       "GET, POST, PATCH, PUT, DELETE, OPTIONS",
      //     "Access-Control-Allow-Credentials": true,
      //     "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token",
      //     // eslint-disable-next-line no-undef
      //   },
      //   responseType: "json",
      //   responseEncoding: "utf8",
      //   withCredentials: true,
      // });

      const workspace_id = this.$route.query?.workspace_id;
      const params = { workspace_id: workspace_id };
      axios
        .get(`http://127.0.0.1:5000/`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.postitList = response.data;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.fetchAllNotes();
  },
};
</script>

<style scoped>
.home {
  .page-header {
    height: 55px;
  }
  padding-left: 10vh;
  padding-right: 10vh;
  padding-top: 5vh;
}
</style>
