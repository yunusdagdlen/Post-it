<template>
  <div class="home fullscreen scroll">
    <div
      class="page-header q-mb-md full-width bg-white"
      style="border-radius: 15px"
    >
      <page-header
        ref="pageHeader"
        @success="fetchAllNotes"
        @filter="changeViewMode"
        @order="changeOrder"
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

    <transition-group
      v-else
      name="card-list"
      tag="div"
      class="cards-list"
    >
      <postit-card
        v-for="postit in this.postitList"
        :key="postit.uuid"
        :postit="postit"
        @ok="fetchAllNotes"
      />
    </transition-group>
    
    <!-- Show more button -->
    <div v-if="postitList.length > 0 && hasMore" class="show-more-container">
      <q-btn
        :loading="isLoadingMore"
        :disable="isLoadingMore"
        color="primary"
        outline
        label="Show more"
        icon="expand_more"
        @click="loadMore"
        class="show-more-btn"
      />
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
      orderDesc: true,
      rankFilter: '',
      statusFilter: '',
      searchTerm: '',
      offset: 0,
      initialLimit: 30,
      loadMoreLimit: 15,
      hasMore: true,
      isLoadingMore: false,
    };
  },
  methods: {
    fetchAllNotes() {
      // Reset pagination state
      this.offset = 0;
      this.hasMore = true;
      
      const workspace_id = this.$route.query?.workspace_id;
      const params = { 
        workspace_id: workspace_id, 
        mode: this.viewMode,
        limit: this.initialLimit,
        offset: 0,
        order: this.orderDesc ? 'desc' : 'asc'
      };
      if (this.rankFilter !== '' && this.rankFilter !== null && this.rankFilter !== undefined) params.rank = this.rankFilter;
      if (this.statusFilter !== '' && this.statusFilter !== null && this.statusFilter !== undefined) params.status = this.statusFilter;
      if ((this.searchTerm || '').trim() !== '') params.search = (this.searchTerm || '').trim();
      axios
        .get(`/app/list_postits`, { params, withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            const list = response.data.postits || [];
            this.postitList = list;
            this.offset = list.length;
            // If we received fewer notes than requested, there are no more
            this.hasMore = list.length >= this.initialLimit;
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
    loadMore() {
      if (this.isLoadingMore || !this.hasMore) return;
      
      this.isLoadingMore = true;
      const workspace_id = this.$route.query?.workspace_id;
      const params = { 
        workspace_id: workspace_id, 
        mode: this.viewMode,
        limit: this.loadMoreLimit,
        offset: this.offset,
        order: this.orderDesc ? 'desc' : 'asc'
      };
      if (this.rankFilter !== '' && this.rankFilter !== null && this.rankFilter !== undefined) params.rank = this.rankFilter;
      if (this.statusFilter !== '' && this.statusFilter !== null && this.statusFilter !== undefined) params.status = this.statusFilter;
      if ((this.searchTerm || '').trim() !== '') params.search = (this.searchTerm || '').trim();
      
      axios
        .get(`/app/list_postits`, { params, withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            const list = response.data.postits || [];
            this.postitList = [...this.postitList, ...list];
            this.offset += list.length;
            // If we received fewer notes than requested, there are no more
            this.hasMore = list.length >= this.loadMoreLimit;
          }
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          this.isLoadingMore = false;
        });
    },
    changeViewMode(payload) {
      if (typeof payload === 'object' && payload !== null) {
        if (payload.mode) this.viewMode = payload.mode;
        if (payload.rank !== undefined) this.rankFilter = payload.rank;
        if (payload.status !== undefined) this.statusFilter = payload.status;
        if (payload.search !== undefined) this.searchTerm = payload.search;
      } else if (payload) {
        this.viewMode = payload;
      }
      this.fetchAllNotes();
    },
    changeOrder(dir) {
      this.orderDesc = dir ? (dir === 'desc') : !this.orderDesc;
      // Refetch from backend with new order
      this.fetchAllNotes();
    },
    openNewNoteDialog() {
      // Use the PageHeader child component's dialog opening method
      this.$refs.pageHeader && this.$refs.pageHeader.newNoteDialog();
    },
    handleScroll() {
      // Check if user has scrolled near the bottom
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;

      // Trigger load more when within 200px of bottom
      if (scrollTop + windowHeight >= documentHeight - 200) {
        this.loadMore();
      }
    },
  },
  computed: {
    ...mapGetters(["baseUrl"]),
  },
  mounted() {
    this.fetchAllNotes();
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
};
</script>

<style scoped>
.home {
  padding-top: 2vh;
  padding-bottom: 4vh;
  padding-left: 12px;
  padding-right: 12px;
  max-width: 1600px;
  margin-left: auto;
  margin-right: auto;
  overflow-x: hidden;
}

@media (min-width: 600px) {
  .home {
    padding-left: 16px;
    padding-right: 16px;
  }
}
@media (min-width: 1024px) {
  .home {
    padding-left: 24px;
    padding-right: 24px;
  }
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

/* Cards list container to avoid negative gutters from Quasar row */
  .cards-list {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
}
/* Ensure cards can flow side-by-side on wider screens */
.cards-list > .PostitMain { width: 100%; }
@media (min-width: 768px) {
  .cards-list {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: stretch;
    justify-content: center; /* prevent recentering when a card height changes */
    gap: 12px;
  }
  .cards-list > .PostitMain {
    /* allow 2–3 columns depending on viewport */
    flex: 1 1 340px;
    max-width: 520px;
  }
}
@media (min-width: 1280px) {
  .cards-list { justify-content: center; }
  .cards-list > .PostitMain { flex-basis: 360px; }
}

/* Show more button styling */
.show-more-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  margin-bottom: 24px;
}

.show-more-btn {
  min-width: 180px;
  padding: 12px 24px;
  border-radius: 16px;
  background: white;
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow: 0 10px 24px rgba(31, 45, 61, 0.12);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.show-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(31, 45, 61, 0.16);
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

/* Card list transition animations */
.card-list-enter-active {
  transition: all 0.4s ease-out;
}

.card-list-leave-active {
  transition: all 0.3s ease-in;
}

.card-list-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

.card-list-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}

.card-list-move {
  transition: transform 0.3s ease;
}
</style>
