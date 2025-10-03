<template>
  <div class="PostitMain">
    <q-card
      style="
        color: black;
        width: 100%;
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
          <div class="text-h6 text-black col-9">
            {{ this.title }}
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
      <transition name="card-expand">
        <q-card-section v-show="this.showNote" class="q-pt-none text-black card-content">
          <template v-for="note in this.notes_by_line" :key="note">
            <span class="note-line">{{ note }}</span>
            <hr />
          </template>
          <div v-if="formattedCreatedAt" class="created-at text-black">{{ formattedCreatedAt }}</div>
        </q-card-section>
      </transition>
    </q-card>
  </div>

  <q-dialog v-model="editNoteDialog" transition-show="jump-down" transition-hide="jump-up">
    <q-card ref="editNoteCard" class="modal-card edit-note-card">
      <div class="modal-accent" :style="{ background: color || postit?.extra_info?.postit_color || '#4dabf7' }"></div>
      <q-card-section class="modal-header">
        <div class="row items-center no-wrap justify-between">
          <div class="row items-center no-wrap">
            <q-avatar size="28px" class="q-mr-sm" :style="{ background: color || postit?.extra_info?.postit_color || '#4dabf7' }">
              <q-icon name="edit" color="white" size="18px" />
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
          label="Write your note..."
          filled
          standout="bg-grey-2 text-dark"
          type="textarea"
          autogrow
        />
      </q-card-section>
      <!-- Color picker: preset swatches -->
      <q-card-section class="q-pt-none q-px-md">
        <div class="text-caption text-grey-7 q-mb-sm">Color</div>
        <div class="row items-center q-gutter-sm">
          <div
            v-for="c in presetColors"
            :key="c"
            class="color-swatch"
            :style="{ background: c, outlineColor: c }"
            :aria-label="'Select color ' + c"
            :class="{ selected: color === c }"
            role="button"
            tabindex="0"
            @click="color = c"
            @keydown.enter.prevent="color = c"
          >
            <q-icon v-if="color === c" name="check" color="white" size="16px" />
          </div>
        </div>
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md">
        <q-btn flat color="grey-7" label="Cancel" v-close-popup />
        <q-btn unelevated color="primary" label="Save" icon="save" @click="editSingleNote" />
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
      color: (this.postit && this.postit.extra_info && this.postit.extra_info.postit_color) ? this.postit.extra_info.postit_color : '#4dabf7',
      presetColors: ["#29bf12", "#abff4f", "#08bdbd", "#ff9914", "#4dabf7", "#845ef7", "#e64980", "#ffa94d"],
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
  watch: {
    editNoteDialog(val) {
      if (val) {
        // Sync fields from current postit when opening dialog
        this.title = this.postit.title;
        this.note = this.postit.note;
        this.color = (this.postit && this.postit.extra_info && this.postit.extra_info.postit_color) ? this.postit.extra_info.postit_color : this.color;
      }
    }
  },
  computed: {
    formattedCreatedAt() {
      try {
        const iso = this.postit && this.postit.extra_info ? this.postit.extra_info.created_at : null;
        if (!iso) return '';
        const d = new Date(iso);
        if (isNaN(d.getTime())) return '';
        return `${d.toLocaleDateString()} ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
      } catch (e) { return ''; }
    }
  },
  methods: {
    // editNote() {
    //   const workspace_id = this.$route.query?.workspace_id;
    //
    //   // Create form data
    //   const formData = new FormData();
    //   formData.append("workspace_id", workspace_id);
    //   formData.append("note_id", this.postit.uuid);
    //   formData.append("title", this.title);
    //   formData.append("note", this.note);
    //
    //
    //   // Axios POST request
    //   axios
    //     .post(`edit-note`, formData, { withCredentials: true })
    //     .then((response) => {
    //       if (response.status === 200) {
    //         this.editNoteDialog = false;
    //         this.$emit("ok");
    //       }
    //     })
    //     .catch((error) => {
    //       console.log(error);
    //     });
    // },
    editSingleNote() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: this.postit.uuid,
        title: this.title,
        note: this.note,
        color: this.color,
      };
      axios.get(`app/edit-note`, { params }, { withCredentials: true })
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
  display: flow-root;
  align-items: center;
  justify-content: center;
  padding: 8px;
}

.PostitMain .q-card {
  border-radius: 16px;
  box-shadow: 0 10px 24px rgba(31, 45, 61, 0.12);
  transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.35);
}

.PostitMain .q-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 32px rgba(31, 45, 61, 0.18);
}

.PostitMain .text-h6 {
  color: #1f2d3d;
  font-weight: 700;
  letter-spacing: 0.2px;
}

.PostitMain hr {
  border: none;
  height: 1px;
  background: rgba(0, 0, 0, 0.08);
  margin: 6px 0;
}
.created-at {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 8px;
  text-align: right;
}

/* Ensure flex children can shrink and cards don't overflow */
.PostitMain { min-width: 0; }
.PostitMain .q-card { max-width: 100%; min-width: 0; box-sizing: border-box; }

/* Robust text wrapping for titles and note content */
/* Title should break by words, not inside words */
.PostitMain .text-h6 { white-space: normal; overflow-wrap: normal; word-break: keep-all; hyphens: manual; }
/* Keep note content resilient (allow breaking inside very long tokens) */
.card-content { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
.card-content .note-line { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; display: block; }
.card-content img, .card-content video, .card-content iframe { max-width: 100%; height: auto; }
</style>

<style scoped>
/* Simple expand/collapse animation for card content */
.card-expand-enter-active, .card-expand-leave-active {
  transition: opacity 160ms ease, transform 160ms ease;
}
.card-expand-enter-from, .card-expand-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.98);
}
.card-expand-enter-to, .card-expand-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>


<style scoped>
/* Modern modal styles for edit dialog (match create new note modal) */
.modal-card {
  width: 90vw;
  max-width: 720px;
  color: #1f2d3d;
  border-radius: 18px;
  box-shadow: 0 20px 50px rgba(31, 45, 61, 0.18);
  overflow: hidden;
  background: #ffffff;
}
.edit-note-card { position: relative; }
.modal-accent { height: 4px; width: 100%; background: #4dabf7; }
.modal-header { padding-top: 14px; padding-bottom: 8px; }
.modal-card .q-field--filled .q-field__control { border-radius: 12px; }
.modal-card .q-textarea .q-field__native { min-height: 120px; }
</style>


<style scoped>
/* Color swatch styles for edit modal */
.color-swatch {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
  box-shadow: 0 0 0 2px #fff inset, 0 2px 6px rgba(0,0,0,0.15);
  outline: 2px solid transparent;
}
.color-swatch:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 0 2px #fff inset, 0 4px 10px rgba(0,0,0,0.18);
}
.color-swatch.selected {
  box-shadow: 0 0 0 2px rgba(255,255,255,0.9) inset, 0 0 0 3px rgba(0,0,0,0.08), 0 6px 14px rgba(0,0,0,0.18);
}
</style>
