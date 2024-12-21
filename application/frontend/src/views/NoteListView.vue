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

  <q-dialog @hide="editNote(noteId)" v-model="editNoteDialog">
    <q-card
      style="color: black; width: 90vh; min-height: 220px; border-radius: 15px"
      :style="{ background: postit?.extra_info?.postit_color }"
    >
      <q-card-section>
        <div class="row full-width">
          <q-input v-model="title" label="Title" class="full-width" />
        </div>
      </q-card-section>
      <q-card-section class="q-pt-none text-black">
        <div class="full-width">
          <q-input
            v-model="note"
            outlined
            type="textarea"
            style="min-height: 100px !important"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import PageHeader from "@/components/PageHeader.vue";
import axios from "axios";

axios.defaults.baseURL = "https://notedflow.com";
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
      const params = { workspace_id: workspace_id };
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
  .page-header {
    height: 55px;
  }
  padding-top: 5vh;
}
</style>
