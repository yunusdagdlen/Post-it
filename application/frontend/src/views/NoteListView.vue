<template class="q-px-xl">
  <div class="home q-mx-xl">
    <div class="page-header q-mb-xl full-width bg-white">
      <page-header @success="fetchAllNotes" :postitList="this.postitList" />
    </div>

    <div>
      <q-markup-table class="q-mb-xl">
        <thead>
          <tr>
            <th class="text-left">Title</th>
            <th class="text-left">Notes</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="postit in this.postitList" :key="postit">
            <tr>
              <td class="text-left" style="width: 15%">{{ postit.title }}</td>
              <td class="text-left">
                <q-list separator>
                  <template v-for="line in postit.note.split('\n')" :key="line">
                    <q-item clickable v-ripple>
                      <q-item-section>{{ line }}</q-item-section>
                    </q-item>
                  </template>
                </q-list>
              </td>
              <td class="text-center" style="width: 200px">
                <q-btn
                  flat
                  outline
                  round
                  color="black"
                  icon="mdi-content-copy"
                  size="sm"
                />
                <q-btn
                  size="sm"
                  flat
                  outline
                  round
                  color="grey-7"
                  icon="edit"
                  @click="
                    openEditDialog(postit.uuid, postit.title, postit.note)
                  "
                />
                <q-btn
                  flat
                  outline
                  round
                  color="grey-7"
                  icon="delete"
                  size="sm"
                  @click="deleteNote(postit.uuid)"
                />
                <q-btn
                  flat
                  outline
                  round
                  color="grey-7"
                  icon="block"
                  size="sm"
                  @click="disableNote(postit.uuid)"
                />
              </td>
            </tr>
          </template>
        </tbody>
      </q-markup-table>
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
import axios from "axios";

//axios.defaults.baseURL = "https://notedflow.com";
//axios.defaults.baseURL = "http://127.0.0.1:5000";

export default {
  name: "NoteListView",
  components: { PageHeader },
  data() {
    return {
      postitList: [],
      editNoteDialog: false,
      title: null,
      note: null,
      noteId: null,
    };
  },
  methods: {
    openEditDialog(noteId, title, note) {
      this.noteId = noteId;
      this.title = title;
      this.note = note;
      this.editNoteDialog = true;
    },
    fetchAllNotes() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = { workspace_id: workspace_id, mode: 'active' };
      axios
        .get(`app/list_postits`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.postitList = response.data.postits;
          }
        })
        .catch((error) => {
          console.log(error);
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
        .get(`app/edit-note`, { params }, { withCredentials: true })
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
        .get(`app/delete-note/`, { params }, { withCredentials: true })
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
        .get(`app/disable-note/`, { params }, { withCredentials: true })
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
