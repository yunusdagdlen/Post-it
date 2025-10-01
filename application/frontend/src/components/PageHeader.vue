<template class="">
  <div class="PageHeader">
    <div class="HeaderToolbar q-mx-xl bordered bg-white">
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
            @click="newNoteDialog"
          />
          <q-btn
            rounded
            flat
            dense
            icon="list"
            class="q-px-md"
            :to="{
              path: 'note-list',
              query: { workspace_id: workspace_id },
            }"
          >
          </q-btn>
          <q-btn
            rounded
            flat
            dense
            icon="save"
            class="q-px-md"
            @click="CopyWorkspaceUrl"
          />
          <q-btn
            rounded
            flat
            dense
            icon="disabled_visible"
            class="q-px-md"
            @click="ChangeViewMode"
          />
        </div>
      </q-toolbar>
    </div>
  </div>

  <q-dialog v-model="newNote">
    <q-card
      style="color: black; width: 90vh; min-height: 220px; border-radius: 15px"
      :style="{ background: this.color }"
    >
      <q-card-section>
        <div class="row full-width">
          <q-input v-model="title" label="Title" class="full-width" />
        </div>
      </q-card-section>
      <q-card-section class="q-pt-none text-black">
        <div class="full-width">
          <q-input
            v-model="content"
            outlined
            type="textarea"
            style="min-height: 100px !important"
          />
        </div>
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          outline
          color="grey-6"
          label="Save"
          icon="save"
          @click="saveNewNote()"
        />
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
  emits: ["success", "viewMode"],
  props: {
    postitList: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  methods: {
    ChangeViewMode() {
      this.$emit("viewMode");
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
      const path = this.$route.fullPath;
      const url = "http://localhost:8080" + path;
      copyToClipboard(url)
        .then(() => {
          this.$swal.fire({
            position: "bottom-end",
            icon: "success",
            title: "Your Workspace Link ,Copy to Clipboard",
            showConfirmButton: false,
            timer: 1500,
          });
        })
        .catch(() => {
          // fail
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
  margin-left: 6px;
  margin-right: 6px;
}
</style>
