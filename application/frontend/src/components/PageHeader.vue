<template class="">
  <div class="PageHeader">
    <div class="HeaderToolbar bordered bg-white">
      <q-toolbar class="q-px-xl rounded bordered">
        <q-toolbar-title class="text-weight-medium">
          <router-link
            style="text-decoration: none; color: #adb5bd"
            :to="{ path: 'app', query: { workspace_id: workspace_id } }"
          >
            NotedFlow
          </router-link>
        </q-toolbar-title>
        <div class="q-mr-md">
          <q-btn
            rounded
            flat
            dense
            icon="mdi-pencil-plus-outline"
            class="q-px-md"
            aria-label="Add note"
            @click="newNoteDialog"
          >
            <q-tooltip anchor="bottom middle" self="top middle" class="bg-grey-9 text-white">Add note</q-tooltip>
          </q-btn>
          <q-btn
            rounded
            flat
            dense
            :icon="viewToggleIcon"
            class="q-px-md"
            :aria-label="viewToggleAria"
            @click="toggleView"
          >
            <q-tooltip anchor="bottom middle" self="top middle" class="bg-grey-9 text-white">{{ viewToggleTooltip }}</q-tooltip>
          </q-btn>
          <q-btn
            rounded
            flat
            dense
            icon="link"
            class="q-px-md"
            aria-label="Copy workspace link"
            @click="CopyWorkspaceUrl"
          >
            <q-tooltip anchor="bottom middle" self="top middle" class="bg-grey-9 text-white">Copy workspace link</q-tooltip>
          </q-btn>
          <q-btn-dropdown
            rounded
            flat
            dense
            icon="filter_alt"
            class="q-px-md"
            aria-label="Filter"
            content-class="viewmode-menu"
          >
            <q-list style="min-width: 140px">
              <q-item clickable v-close-popup @click="setViewMode('active')">
                <q-item-section avatar><q-icon name="check_circle" :color="currentMode==='active' ? 'primary' : 'grey-5'" /></q-item-section>
                <q-item-section>Active</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="setViewMode('deactive')">
                <q-item-section avatar><q-icon name="block" :color="currentMode==='deactive' ? 'primary' : 'grey-5'" /></q-item-section>
                <q-item-section>Deactive</q-item-section>
              </q-item>
              <q-separator spaced inset />
              <q-item clickable v-close-popup @click="setViewMode('all')">
                <q-item-section avatar><q-icon name="layers" :color="currentMode==='all' ? 'primary' : 'grey-5'" /></q-item-section>
                <q-item-section>All</q-item-section>
              </q-item>
            </q-list>
            <q-tooltip anchor="bottom middle" self="top middle" class="bg-grey-9 text-white">Filter</q-tooltip>
          </q-btn-dropdown>
          <q-btn
            rounded
            flat
            dense
            icon="restart_alt"
            class="q-px-md"
            aria-label="Reset workspace"
            @click="resetWorkspace"
          >
            <q-tooltip anchor="bottom middle" self="top middle" class="bg-grey-9 text-white">Reset workspace</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>
    </div>
  </div>

  <q-dialog v-model="newNote" transition-show="jump-down" transition-hide="jump-up">
    <q-card class="modal-card new-note-card" :style="{ '--accent': color }">
      <div class="modal-accent" :style="{ background: color }"></div>
      <q-card-section class="modal-header">
        <div class="row items-center no-wrap justify-between">
          <div class="row items-center no-wrap">
            <q-avatar size="28px" class="q-mr-sm" :style="{ background: color }">
              <q-icon name="mdi-pencil-plus-outline" color="white" size="18px" />
            </q-avatar>
            <div class="text-subtitle1 text-weight-medium">Add note</div>
          </div>
          <q-btn flat round dense icon="close" v-close-popup />
        </div>
      </q-card-section>
      <q-card-section class="q-pt-sm">
        <q-input v-model="title" label="Title" filled standout="bg-grey-2 text-dark" dense autofocus />
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          v-model="content"
          label="Write your note..."
          filled
          standout="bg-grey-2 text-dark"
          type="textarea"
          autogrow
        />
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md">
        <q-btn flat color="grey-7" label="Cancel" v-close-popup />
        <q-btn unelevated color="primary" label="Save" icon="save" @click="saveNewNote()" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import axios from "axios";
import { copyToClipboard } from "quasar";

//axios.defaults.baseURL = "https://notedflow.com";
//axios.defaults.baseURL = "http://127.0.0.1:5000";

export default {
  name: "PageHeader",
  data() {
    return {
      workspace_id: this.$route.query?.workspace_id,
      newNote: false,
      postitListDialog: false,
      content: "",
      title: "",
      color: "",
      currentMode: 'active',
    };
  },
  watch: {
    "$route.query.workspace_id": {
      handler(workspace_id) {
        this.workspace_id = workspace_id;
      },
      deep: true,
      immediate: true,
    },
  },
  emits: ["success", "filter", "viewMode"],
  props: {
    postitList: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  computed: {
    viewModeLabel() {
      const map = { active: 'Active', deactive: 'Deactive', disabled: 'Deactive', all: 'All' };
      return map[this.currentMode] || 'Active';
    },
    isListView() {
      return this.$route.path && this.$route.path.includes('note-list');
    },
    viewToggleIcon() {
      return this.isListView ? 'dashboard' : 'view_list';
    },
    viewToggleTooltip() {
      return this.isListView ? 'Switch to board view' : 'Switch to list view';
    },
    viewToggleAria() {
      return this.viewToggleTooltip;
    }
  },
  methods: {
    ChangeViewMode() {
      // Backward compatibility: emit without parameter (parent may ignore)
      this.$emit("filter");
      this.$emit("viewMode");
    },
    setViewMode(mode) {
      this.currentMode = mode;
      // Emit new event name and legacy one for compatibility
      this.$emit('filter', mode);
      this.$emit('viewMode', mode);
    },
    toggleView() {
      const wid = this.$route.query?.workspace_id || this.workspace_id;
      if (this.isListView) {
        // Go to board view
        this.$router.push({ path: 'app', query: { workspace_id: wid } });
      } else {
        // Go to list view
        this.$router.push({ path: 'note-list', query: { workspace_id: wid } });
      }
    },
    saveNewNote() {
      const workspace_id = this.workspace_id;
      const params = {
        note: this.content,
        title: this.title,
        color: this.color,
        workspace_id: workspace_id,
      };
      console.log(params);
      axios
        .get("app/add", { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.newNote = false;
            this.content = "";
            this.title = "";
            this.color = "#29bf12";
            this.$emit("success");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    newNoteDialog() {
      const colorList = ["#29bf12", "#abff4f", "#08bdbd", "#ff9914"];
      const colorId = Math.floor(Math.random() * 4);
      this.color = colorList[colorId];
      this.newNote = true;
    },
    CopyWorkspaceUrl() {
      try {
        const wid = this.$route.query?.workspace_id || this.workspace_id;
        if (wid) {
          const resolved = this.$router.resolve({ path: '/app', query: { workspace_id: wid } });
          const url = window.location.origin + resolved.href;
          copyToClipboard(url)
            .then(() => {
              this.$swal.fire({
                position: "bottom-end",
                icon: "success",
                title: "Workspace link copied.",
                showConfirmButton: false,
                timer: 1500,
              });
            })
            .catch(() => {});
        } else {
          // Fallback: copy current URL if workspace id not yet available
          copyToClipboard(window.location.href)
            .then(() => {
              this.$swal.fire({
                position: "bottom-end",
                icon: "success",
                title: "Current link copied.",
                showConfirmButton: false,
                timer: 1500,
              });
            })
            .catch(() => {});
        }
      } catch (e) {
        // silent
      }
    },
    resetWorkspace() {
      const currentUrl = window.location.href;
      this.$swal
        .fire({
          title: 'Clear workspace? ',
          html:
            `<div style="text-align:left;">
               <div style="font-size:14px; color:#555; margin-bottom:8px;">This will remove your workspace id from session. You will get a fresh workspace afterwards.</div>
               <div style="display:flex; align-items:center; gap:8px; padding:10px; border-radius:8px; background:#f8f9fb;">
                 <span style="flex:1; overflow:auto; white-space:nowrap; font-family:monospace; font-size:12px;" id="current-url">${currentUrl}</span>
                 <button id="copy-url-btn" style="cursor:pointer; border:none; background:#e9ecef; padding:6px 10px; border-radius:6px; font-size:12px;">📋 Copy URL</button>
               </div>
             </div>`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Yes, clear it',
          cancelButtonText: 'Cancel',
          focusCancel: true,
          didOpen: () => {
            const btn = document.getElementById('copy-url-btn');
            if (btn) {
              btn.addEventListener('click', () => {
                try {
                  const toCopy = currentUrl;
                  if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(toCopy)
                      .then(() => this.$swal.fire({ position: 'bottom-end', icon: 'success', title: 'URL copied', showConfirmButton: false, timer: 1200 }));
                  } else {
                    // Fallback using Quasar util
                    copyToClipboard(toCopy)
                      .then(() => this.$swal.fire({ position: 'bottom-end', icon: 'success', title: 'URL copied', showConfirmButton: false, timer: 1200 }))
                      .catch(() => {});
                  }
                } catch (e) { /* ignore */ }
              });
            }
          },
        })
        .then((result) => {
          if (result.isConfirmed) {
            axios
              .get('app/clear-workspace')
              .then(() => { window.location.href = '/app'; })
              .catch(() => { window.location.href = '/app'; });
          }
        });
    },
  },
};
</script>

<style scoped>
.PageHeader {
  background: transparent;
  width: 100%;
}

.HeaderToolbar {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 16px;
  border: 1px solid rgba(173, 181, 189, 0.4);
  color: #495057;
  font-weight: 600;
  margin-top: 5vh;
  box-shadow: 0 6px 20px rgba(31, 45, 61, 0.08);
  backdrop-filter: saturate(150%) blur(8px);
}

.HeaderToolbar .q-toolbar {
  min-height: 56px;
}

.HeaderToolbar .q-btn {
  margin-left: 2px;
  margin-right: 2px;
}

/* Modern modal styles */
.modal-card {
  width: 90vw;
  max-width: 720px;
  color: #1f2d3d;
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(31, 45, 61, 0.18);
  overflow: hidden;
  background: #ffffff;
}

.new-note-card {
  position: relative;
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

/* Input tweaks inside modals */
.modal-card .q-field--filled .q-field__control {
  border-radius: 12px;
}

.modal-card .q-textarea .q-field__native {
  min-height: 120px;
}
</style>
