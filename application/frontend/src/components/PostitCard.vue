<template>
  <div class="PostitMain">
    <q-card
      style="
        color: black;
        min-width: 20vh;
        max-width: 500px;
        min-height: 30px;
        border-radius: 15px;
        align-items: center;
      "
      @click="showNote = !this.showNote"
      :style="{
        background: postit?.extra_info?.postit_color ? postit?.extra_info?.postit_color : '#59a5d8',
        opacity: this.active ? 1 : 0.5
      }"
    >
      <!--default view -->
      <q-card-section>
        <div class="row">
          <div class="text-h6 text-black col-9" style="word-break: auto-phrase">
            {{ this.title }} {{this.active}}
          </div>
          <q-space />
          <div
            class="col-3"
            style="display: flex; align-items: baseline; justify-content: end"
          >
            <q-btn rounded flat dense icon="mdi-menu" color="black">
              <q-menu fit anchor="bottom right" self="top right">
                <div class="row no-wrap q-pa-sm">
                  <div class="column">
                    <q-btn
                      size="sm"
                      flat
                      outline
                      rounded
                      align="left"
                      color="grey-7"
                      icon="edit"
                      label="Edit"
                      @click="this.editNoteDialog = true"
                    />
                    <q-btn
                      flat
                      outline
                      rounded
                      align="left"
                      color="grey-7"
                      icon="delete"
                      label="Delete"
                      size="sm"
                      @click="deleteNote"
                    />
                    <q-btn
                      flat
                      outline
                      rounded
                      align="left"
                      color="grey-7"
                      icon="block"
                      label="Disable"
                      size="sm"
                      @click="disableNote"
                    />
                  </div>
                </div>
              </q-menu>
            </q-btn>
          </div>
        </div>
      </q-card-section>
      <template v-if="this.showNote">
        <q-card-section class="q-pt-none text-black">
          <template v-for="note in this.notes_by_line" :key="note">
            <span style="white-space: pre-line">{{ note }}</span>
            <hr />
          </template>
        </q-card-section>
      </template>
    </q-card>
  </div>

  <q-dialog v-model="editNoteDialog">
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
      <q-card-actions class="q-pr-md q-pt-none">
        <q-space />
        <q-btn @click="deleteNote" label="Save" color="black" outline />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
<script>
import axios from "axios";
// axios.defaults.baseURL = "https://notedflow.com";
// axios.defaults.baseURL = "http://127.0.0.1:5000";

export default {
  data() {
    return {
      editNoteDialog: false,
      title: this.postit.title,
      note: this.postit.note,
      active: this.postit.active,
      notes_by_line: this.postit.notes_by_line,
      showNote: false,
      menuButton: false,
    };
  },
  name: "PostitCard",
  props: {
    postit: {
      type: Object,
      required: true,
    },
  },
  emits: ["ok"],
  methods: {
    editNote() {
      const workspace_id = this.$route.query?.workspace_id;

      // Create form data
      const formData = new FormData();
      formData.append("workspace_id", workspace_id);
      formData.append("note_id", this.postit.uuid);
      formData.append("title", this.title);
      formData.append("note", this.note);


      // Axios POST request
      axios
        .post(`edit-note`, formData, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.editNoteDialog = false;
            this.$emit("ok");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    deleteNote() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: this.postit.uuid,
      };
      axios
        .get(`app/delete-note/`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.editNoteDialog = false;
            this.$emit("ok");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    disableNote() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: this.postit.uuid,
      };
      axios
        .get(`app/disable-note/`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.editNoteDialog = false;
            this.$emit("ok");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.PostitMain {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
