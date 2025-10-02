<template class="q-px-xl">
  <div class="home fullscreen q-mx-xl scroll">
    <div
      class="page-header q-mb-xl full-width bg-white"
      style="border-radius: 15px"
    >
      <page-header
        ref="pageHeader"
        @success="fetchAllNotes"
        @filter="changeViewMode"
        :postitList="this.postitList"
      />
    </div>

    <!-- Empty state: invite user to create the first note -->
    <div v-if="postitList.length === 0" class="empty-state">
      <div class="empty-card" @click="openNewNoteDialog">
        <div class="icon">✏️</div>
        <div class="title">Start by adding a note</div>
        <div class="subtitle">Create your first note to get started. NotedFlow is a shareable notebook with simple status control — perfect for capturing ideas and tracking progress.</div>
        <q-btn color="primary" label="Start now" class="q-mt-md" @click.stop="openNewNoteDialog" />
      </div>
    </div>

    <div
      v-else
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
import { mapGetters } from "vuex";

//axios.defaults.baseURL = "https://notedflow.com";
//axios.defaults.baseURL = "http://127.0.0.1:5000";

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
    changeViewMode(mode) {
      if (mode) {
        this.viewMode = mode;
      }
      this.fetchAllNotes();
    },
    openNewNoteDialog() {
      // Use the PageHeader child component's dialog opening method
      this.$refs.pageHeader && this.$refs.pageHeader.newNoteDialog();
    },
  },
  computed: {
    ...mapGetters(["baseUrl"]),
  },
  mounted() {
    this.fetchAllNotes();
  },
};
</script>

<style scoped>
.home {
  padding-top: 5vh;
  padding-bottom: 4vh;
}

.home .page-header {
  height: auto;
  background: transparent !important;
}

.home .row {
  align-items: stretch;
  justify-content: center;
  flex-wrap: wrap;
}

/* Empty state styling */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
}

.empty-card {
  user-select: none;
  cursor: pointer;
  text-align: center;
  padding: 32px 28px;
  border-radius: 16px;
  border: 2px dashed #ced4da;
  background: #fff;
  color: #495057;
  max-width: 520px;
  width: 100%;
  transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.empty-card:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

.empty-card .icon {
  font-size: 42px;
  margin-bottom: 8px;
}

.empty-card .title {
  font-size: 20px;
  font-weight: 600;
}

.empty-card .subtitle {
  font-size: 14px;
  color: #868e96;
  margin-top: 4px;
}
</style>
