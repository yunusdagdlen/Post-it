<template class="q-px-xl">
  <div class="home fullscreen q-mx-xl scroll">
    <div
      class="page-header q-mb-xl full-width bg-white"
      style="border-radius: 15px"
    >
      <page-header
        @success="fetchAllNotes"
        @viewMode="changeViewMode"
        :postitList="this.postitList"
      />
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
      viewMode: "active",
    };
  },
  methods: {
    fetchAllNotes() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = { workspace_id: workspace_id, mode: this.viewMode };
      axios
        .get(`app/list_postits`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.postitList = response.data.postits;
            if (response.data?.workspace_id) {
              this.$router.push({
                query: { workspace_id: response.data.workspace_id },
              });
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    changeViewMode() {
      if (this.viewMode === "active") {
        this.viewMode = "deactive";
      } else {
        this.viewMode = "active";
      }
      this.fetchAllNotes();
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
  padding-top: 5vh;
}
</style>
