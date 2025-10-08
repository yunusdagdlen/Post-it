<template class="q-px-xl">
  <div class="home q-mx-xl">
    <div class="page-header q-mb-md full-width bg-white">
      <page-header @success="fetchAllNotes" @filter="changeViewMode" @order="changeOrder" :postitList="this.postitList" />
    </div>

    <div>
      <q-markup-table class="q-mb-xl notes-table">
        <thead>
          <tr>
            <th class="text-left">Title</th>
            <th class="text-center">Rank</th>
            <th class="text-left">Status</th>
            <th class="text-left">Created</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="postit in this.postitList" :key="postit.uuid || postit.id">
            <tr>
              <td class="text-left title-col">
                <div class="title-text text-weight-bold">{{ postit.title }}</div>
                <!-- Mobile-only combined note content -->
                <div class="mobile-note">
                  <q-list separator>
                    <template v-for="(line, idx) in (postit.note || '').split('\n')" :key="postit.uuid + '-line-' + idx">
                      <q-item>
                        <q-item-section>{{ line }}</q-item-section>
                      </q-item>
                    </template>
                  </q-list>
                </div>
              </td>
              <td class="text-center rank-col">
                <MinimalStars :model-value="(postit.rank === null || postit.rank === undefined || postit.rank === '') ? 1 : postit.rank" :max="5" size="18px" class="minimal-stars" />
              </td>
              <td class="text-left status-col">
                <StatusPicker :model-value="postit.status ?? 0" @update:modelValue="val => updateStatus(postit, val)" />
              </td>
              <td class="text-left created-col">
                {{ formatDate(postit?.extra_info?.created_at) }}
              </td>
              <td class="text-center actions-col">
                <div class="actions-desktop">
                  <q-btn flat outline round color="grey-7" icon="mdi-content-copy" size="sm" @click="copyNote(postit)" />
                  <q-btn flat outline round color="grey-7" icon="edit" size="sm" @click="openEditDialog(postit.uuid, postit.title, postit.note)" />
                  <q-btn flat outline round color="grey-7" icon="delete" size="sm" @click="deleteNote(postit.uuid)" />
                  <q-btn flat outline round color="grey-7" icon="block" size="sm" @click="disableNote(postit.uuid)" />
                </div>
                <div class="actions-mobile">
                  <q-btn flat outline round color="grey-7" icon="menu" size="sm">
                    <q-menu fit anchor="bottom right" self="top right">
                      <q-list style="min-width: 160px">
                        <q-item clickable v-close-popup @click="copyNote(postit)">
                          <q-item-section avatar><q-icon name="mdi-content-copy" /></q-item-section>
                          <q-item-section>Copy</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="openEditDialog(postit.uuid, postit.title, postit.note)">
                          <q-item-section avatar><q-icon name="edit" /></q-item-section>
                          <q-item-section>Edit</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="deleteNote(postit.uuid)">
                          <q-item-section avatar><q-icon name="delete" /></q-item-section>
                          <q-item-section>Delete</q-item-section>
                        </q-item>
                        <q-item clickable v-close-popup @click="disableNote(postit.uuid)">
                          <q-item-section avatar><q-icon name="block" /></q-item-section>
                          <q-item-section>Disable</q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-btn>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </q-markup-table>
      
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
  </div>

  <q-dialog @hide="editNote(noteId)" v-model="editNoteDialog" transition-show="jump-down" transition-hide="jump-up">
    <q-card class="modal-card edit-note-card">
      <div class="modal-accent"></div>
      <q-card-section class="modal-header">
        <div class="row items-center no-wrap justify-between">
          <div class="row items-center no-wrap">
            <q-avatar size="28px" class="q-mr-sm" color="primary" text-color="white">
              <q-icon name="edit" size="18px" />
            </q-avatar>
            <div class="text-subtitle1 text-weight-medium">Edit note</div>
          </div>
          <q-btn flat round dense icon="close" v-close-popup />
        </div>
      </q-card-section>
      <q-card-section class="q-pt-sm">
        <q-input v-model="title" label="Title" filled standout="bg-grey-2 text-dark" dense />
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          v-model="note"
          label="Update your note..."
          filled
          standout="bg-grey-2 text-dark"
          type="textarea"
          autogrow
        />
      </q-card-section>
      <q-card-section class="q-pt-none q-px-md q-pb-md text-grey-7" style="font-size: 12px;">
        Changes are saved when you close the dialog
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import PageHeader from "@/components/PageHeader.vue";
import MinimalStars from "@/components/MinimalStars.vue";
import StatusPicker from "@/components/StatusPicker.vue";
import axios from "axios";
import { copyToClipboard } from "quasar";

//axios.defaults.baseURL = "https://notedflow.com";
//axios.defaults.baseURL = "http://127.0.0.1:5000";

export default {
  name: "NoteListView",
  components: { PageHeader, MinimalStars, StatusPicker },
  data() {
    return {
      postitList: [],
      editNoteDialog: false,
      title: null,
      note: null,
      noteId: null,
      // filters and ordering for list view
      viewMode: 'active',
      orderDesc: true, // newest first
      rankFilter: '',
      statusFilter: '',
      searchTerm: '',
      // pagination
      offset: 0,
      initialLimit: 30,
      loadMoreLimit: 15,
      hasMore: true,
      isLoadingMore: false,
    };
  },
  methods: {
    openEditDialog(noteId, title, note) {
      this.noteId = noteId;
      this.title = title;
      this.note = note;
      this.editNoteDialog = true;
    },
    copyNote(postit) {
      try {
        const text = `${postit.title ? postit.title + "\n\n" : ''}${postit.note || ''}`.trim();
        if (!text) return;
        copyToClipboard(text).then(() => {
          if (this.$swal && typeof this.$swal.fire === 'function') {
            this.$swal.fire({ position: 'bottom-end', icon: 'success', title: 'Copied', showConfirmButton: false, timer: 1200 });
          }
        }).catch(() => {});
      } catch (e) { /* noop */ }
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
    displayRank(r) {
      return (r === null || r === undefined || r === '') ? 1 : r;
    },
    formatDate(iso) {
      try {
        if (!iso) return '';
        const d = new Date(iso);
        if (isNaN(d.getTime())) return '';
        return `${d.toLocaleDateString()} ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
      } catch (e) { return ''; }
    },
    updateStatus(postit, val) {
      const workspace_id = this.$route.query?.workspace_id;
      const params = { workspace_id, note_id: postit.uuid, status: val };
      // optimistic update
      postit.status = val;
      axios.get(`/app/edit-note/`, { params, withCredentials: true })
        .then(() => {})
        .catch(() => {});
    },
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
    editNote(noteId) {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: noteId,
        title: this.title,
        note: this.note,
      };
      axios
        .get(`/app/edit-note/`, { params, withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.editNoteDialog = false;
            this.title = null;
            this.note = null;
            this.noteId = null;
            this.fetchAllNotes();
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteNote(noteId) {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: noteId,
      };
      axios
        .get(`/app/delete-note/`, { params, withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.editNoteDialog = false;
            this.fetchAllNotes();
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    disableNote(noteId) {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: noteId,
      };
      axios
        .get(`/app/disable-note/`, { params, withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.editNoteDialog = false;
            this.fetchAllNotes();
          }
        })
        .catch((error) => {
          console.log(error);
        });
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
}

.home .page-header {
  height: auto;
}

.home .q-markup-table {
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 10px 24px rgba(31, 45, 61, 0.08);
  background: #ffffff;
}

.home thead th {
  background: #f8f9fb;
  color: #495057;
  font-weight: 600;
}

.home tbody tr:nth-child(even) {
  background: #fcfdff;
}

.home td,
.home th {
  border-color: rgba(0, 0, 0, 0.06);
}

/* Make list view table mobile-friendly */
.notes-table { table-layout: fixed; width: 100%; }
.notes-table th, .notes-table td { white-space: normal; overflow-wrap: anywhere; word-break: break-word; }
.notes-table td .q-item, .notes-table td .q-item__section { white-space: normal; overflow-wrap: anywhere; word-break: break-word; }

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

/* Columns */
.title-col { width: auto; }
.actions-col { width: auto; }
.actions-col { display: flex; gap: 6px; justify-content: flex-end; align-items: center; }

/* Visibility and layout */
.mobile-note { display: block; margin-top: 6px; }
.actions-desktop { display: inline-flex; }
.actions-mobile { display: none; }
@media (max-width: 599px) {
  .actions-desktop { display: none; }
  .actions-mobile { display: inline-flex; }
}
/* notes-col removed */

/* Ensure wrapping inside combined cell */
.title-text, .mobile-note, .mobile-note .q-item, .mobile-note .q-item__section {
  white-space: normal; overflow-wrap: anywhere; word-break: break-word;
}

.modal-card {
  width: 90vw;
  max-width: 720px;
  color: #1f2d3d;
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(31, 45, 61, 0.18);
  overflow: hidden;
  background: #ffffff;
}

.modal-accent {
  height: 4px;
  width: 100%;
  background: #4dabf7;
}

.modal-header {
  padding-top: 14px;
  padding-bottom: 8px;
}

.modal-card .q-field--filled .q-field__control {
  border-radius: 12px;
}

.modal-card .q-textarea .q-field__native {
  min-height: 120px;
}
</style>
