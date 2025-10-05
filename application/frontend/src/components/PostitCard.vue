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
      @click="onCardClick"
      :style="{
        background: postit?.extra_info?.postit_color ? postit?.extra_info?.postit_color : '#59a5d8',
        opacity: this.active ? 1 : 0.5
      }"
    >
      <!--default view -->
      <q-card-section>
        <div class="row">
          <div class="col-9">
            <div class="text-h6 text-black">{{ this.title }}</div>
            <div class="q-mt-xs rank-inline">
              <MinimalStars
                v-model="cardRank"
                :max="5"
                size="22px"
                class="minimal-stars"
                @update:model-value="updateRank"
              />
            </div>
          </div>
          <q-space />
          <div
            class="col-3"
            style="display: flex; flex-direction: column; align-items: flex-end; justify-content: flex-start; gap: 6px;"
          >
            <div style="display: flex; flex-direction: row; align-items: center; justify-content: flex-end; gap: 6px; width: 100%;">
              <q-btn
                id="play"
                flat
                dense
                round
                size="sm"
                icon="volume_up"
                color="black"
                @click.stop="speakTitleAndNote"
                aria-label="Speak"
              />
              <CardMenu
                @edit="this.editNoteDialog = true"
                @delete="deleteNote"
                @disable="disableNote"
              />
            </div>
            <DoneCheck
              :show="((currentStatus === 2) || (currentStatus === undefined && postit && postit.status === 2))"
              color="black"
              size="20px"
            />
          </div>
        </div>
      </q-card-section>
      <transition name="card-expand">
        <q-card-section v-show="this.showNote" class="q-pt-none text-black card-content">
          <template v-for="(note, idx) in this.notes_by_line" :key="'line-'+idx">
            <div class="note-row row items-center no-wrap justify-between">
              <div class="line-left ellipsis">
                <span class="note-line text-black">
                  {{ lineStates[idx]?.showingOriginal ? lineStates[idx].original : (lineStates[idx]?.translated || note) }}
                </span>
                <q-spinner v-if="lineStates[idx]?.loading" size="14px" color="black" class="q-ml-xs" />
              </div>
              <div class="line-actions row items-center no-wrap">
                <q-btn
                  v-if="!lineStates[idx]?.translated || lineStates[idx]?.showingOriginal"
                  flat
                  dense
                  round
                  size="sm"
                  icon="translate"
                  color="black"
                  :disable="lineStates[idx]?.loading"
                  @click.stop="translateLine(idx)"
                  :aria-label="'Translate line ' + (idx + 1)"
                >
                  <q-tooltip anchor="top middle" self="bottom middle" class="bg-grey-9 text-white">Translate</q-tooltip>
                </q-btn>
                <q-btn
                  v-else
                  flat
                  dense
                  round
                  size="sm"
                  icon="visibility"
                  color="black"
                  :disable="lineStates[idx]?.loading"
                  @click.stop="toggleOriginal(idx)"
                  :aria-label="'View original for line ' + (idx + 1)"
                >
                  <q-tooltip anchor="top middle" self="bottom middle" class="bg-grey-9 text-white">View original</q-tooltip>
                </q-btn>
                <q-btn
                  flat
                  dense
                  round
                  icon="content_copy"
                  color="black"
                  size="sm"
                  class="q-ml-xs"
                  @click.stop="copyLine(lineStates[idx]?.showingOriginal ? lineStates[idx].original : (lineStates[idx]?.translated || note))"
                  :aria-label="'Copy line ' + (idx + 1)"
                >
                  <q-tooltip anchor="top middle" self="bottom middle" class="bg-grey-9 text-white">Copy</q-tooltip>
                </q-btn>
              </div>
            </div>
            <hr />
          </template>
          <div class="card-footer row items-center justify-between no-wrap q-mt-sm">
            <div class="status-left">
              <StatusPicker
                v-model="currentStatus"
                @update:modelValue="val => updateStatus(val)"
              />
            </div>
            <div v-if="formattedCreatedAt" class="created-at text-black">{{ formattedCreatedAt }}</div>
          </div>
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
      <!-- Color & Rank pickers (responsive, match add note modal) -->
      <q-card-section class="q-pt-none q-px-md">
        <div class="picker-grid">
          <!-- Color picker: preset swatches -->
          <div class="picker-block">
            <ColorSwatches v-model="color" :options="presetColors" label="Color" />
          </div>

          <!-- Rank picker: 5-star selection -->
          <div class="picker-block rank-block">
            <div class="row items-center no-wrap">
              <MinimalStars
                v-model="editRank"
                :max="5"
                size="28px"
                class="minimal-stars"
              />
            </div>
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
/* global puter */
import axios from "axios";
import { copyToClipboard } from "quasar";
// axios.defaults.baseURL = "https://notedflow.com";
// axios.defaults.baseURL = "http://127.0.0.1:5000";
import MinimalStars from './MinimalStars.vue';
import StatusPicker from './StatusPicker.vue';
import ColorSwatches from './ColorSwatches.vue';
import CardMenu from './CardMenu.vue';
import DoneCheck from './DoneCheck.vue';

export default {
  components: { MinimalStars, StatusPicker, ColorSwatches, CardMenu, DoneCheck },
  data() {
    return {
      editNoteDialog: false,
      title: this.postit.title,
      note: this.postit.note,
      color: (this.postit && this.postit.extra_info && this.postit.extra_info.postit_color) ? this.postit.extra_info.postit_color : '#4dabf7',
      editRank: (this.postit && this.postit.rank !== null && this.postit.rank !== undefined && this.postit.rank !== '') ? this.postit.rank : 1,
      cardRank: (this.postit && this.postit.rank !== null && this.postit.rank !== undefined && this.postit.rank !== '') ? this.postit.rank : 1,
      currentStatus: (this.postit && this.postit.status !== null && this.postit.status !== undefined && this.postit.status !== '') ? this.postit.status : 0,
      presetColors: ["#29bf12", "#abff4f", "#08bdbd", "#ff9914", "#4dabf7", "#845ef7", "#e64980", "#ffa94d"],
      active: this.postit.active,
      notes_by_line: this.postit.notes_by_line,
      lineStates: (this.postit.notes_by_line || []).map(t => ({ original: t, translated: null, showingOriginal: false, loading: false })),
      showNote: false,
      menuButton: false,
      puterSignedIn: false, 
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
        const r = this.postit ? this.postit.rank : undefined;
        this.editRank = (r === null || r === undefined || r === '') ? 1 : r;
      }
    },
    'postit.notes_by_line': {
      handler(newVal) {
        this.notes_by_line = newVal || [];
        this.lineStates = (this.notes_by_line || []).map(t => ({ original: t, translated: null, showingOriginal: false, loading: false }));
      },
      immediate: false
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
    },
    displayRank() {
      const r = this.postit ? this.postit.rank : undefined;
      return (r === null || r === undefined || r === '') ? 1 : r;
    },
    displayStatus() {
      const s = (this.currentStatus === null || this.currentStatus === undefined || this.currentStatus === '') ? 0 : this.currentStatus;
      return s === 2 ? 'Done' : (s === 1 ? 'In progress' : 'New');
    },
    statusIcon() {
      const s = (this.currentStatus === null || this.currentStatus === undefined || this.currentStatus === '') ? 0 : this.currentStatus;
      return s === 2 ? 'check_circle' : (s === 1 ? 'autorenew' : 'fiber_new');
    },
    statusTextColor() {
      // keep neutral readable color; background is handled by .status-chip style
      return 'grey-9';
    }
  },
  methods: {
      async translateLine(idx) {
        try {
          const state = this.lineStates[idx];
          if (!state || state.loading) return;
          // If we already have a translation but user is on original view, just toggle to translation
          if (state.translated && state.showingOriginal) {
            state.showingOriginal = false;
            return;
          }
          state.loading = true;
          const payload = { text: state.original, source: 'auto', target: 'tr' };
          const res = await axios.post('/app/translate', payload, { withCredentials: true });
          if (res && res.data && (res.data.translation || res.data.translatedText)) {
            state.translated = res.data.translation || res.data.translatedText;
            state.showingOriginal = false; // switch to translation view
          }
        } catch (e) {
          // silent fail; optionally show a toast later
          console.error(e);
        } finally {
          const st = this.lineStates[idx];
          if (st) st.loading = false;
        }
      },
      toggleOriginal(idx) {
        const st = this.lineStates[idx];
        if (!st) return;
        st.showingOriginal = true;
      },
      async playPuterSpeak(text) {
        try {
          if (!text || typeof text !== 'string') return;
          const win = typeof window !== 'undefined' ? window : undefined;
          const p = (win && typeof win.puter !== 'undefined') ? win.puter : (typeof puter !== 'undefined' ? puter : null);

          // IMPORTANT: Do NOT trigger Puter sign-in from a simple click.
          // Some environments open a blocking overlay/modal that can swallow further clicks.
          // We'll only try TTS if the SDK is present and functional; otherwise we fall back.

          // Try Puter TTS if available (without forcing sign-in)
          if (p && p.ai?.txt2speech) {
            try {
              // Race txt2speech with a timeout so we never hang the UI if SDK stalls
              const timeout = new Promise((_, rej) => setTimeout(() => rej(new Error('Puter TTS timeout')), 3000));
              const audio = await Promise.race([p.ai.txt2speech(text,
                  {
                    voice: "Amy",
                    engine: "standard",
                    language: "en-GB"
                  }),
                  timeout]);
              if (audio?.play) {
                audio.play();
                return;
              }
            } catch (ttsErr) {
              console.error('Puter TTS failed:', ttsErr);
            }
          }

          // Fallback: Web Speech API
          if (win && 'speechSynthesis' in win && typeof win.SpeechSynthesisUtterance !== 'undefined') {
            const utter = new win.SpeechSynthesisUtterance(text);
            utter.lang = 'en-US';
            win.speechSynthesis.cancel(); // stop any existing speech
            win.speechSynthesis.speak(utter);
          } else {
            console.warn('No speech synthesis available.');
          }
        } catch(e) {
          console.error(e);
        }
      },
      speakTitleAndNote() {
        const title = typeof this.title === 'string' ? this.title.trim() : '';
        const note = typeof this.note === 'string' ? this.note.trim() : '';
        const combined = [title, note].filter(Boolean).join('. ');
        if (combined) {
          this.playPuterSpeak(combined);
        }
      },
    onCardClick() {
      const wasOpen = this.showNote;
      this.showNote = !this.showNote;
      if (!wasOpen && this.showNote) {
        // when opening first time, if status is NEW (0), set to In progress (1) silently (no list reload)
        const s = (this.currentStatus === null || this.currentStatus === undefined)
          ? (this.postit && this.postit.status !== undefined ? this.postit.status : 0)
          : this.currentStatus;
        if (s === 0) {
          this.updateStatus(1, { silent: true });
        }
      }
    },
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
        rank: this.editRank,
      };
      axios.get(`/app/edit-note/`, { params, withCredentials: true })
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

    updateRank(val) {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: this.postit.uuid,
        rank: val,
      };
      axios.get(`/app/edit-note/`, { params, withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.cardRank = val;
            // optionally refresh parent list
            this.$emit('ok');
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    updateStatus(val, options = {}) {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: this.postit.uuid,
        status: val,
      };
      // Optimistically update UI immediately
      this.currentStatus = val;
      const isSilent = options && options.silent === true;
      // Fire request without blocking UI; emit refresh only if not silent
      axios.get(`/app/edit-note/`, { params, withCredentials: true })
        .then((response) => {
          if (!isSilent && response && response.status === 200) {
            // notify parent to refresh list; avoid mutating props directly
            this.$emit('ok');
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    copyLine(line) {
      try {
        const text = (line === null || line === undefined) ? '' : String(line);
        if (!text) return;
        // Quasar utility returns a Promise
        copyToClipboard(text).catch(() => {});
      } catch (e) {
        // no-op
      }
    },

    deleteNote() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        workspace_id: workspace_id,
        note_id: this.postit.uuid,
      };
      axios
        .get(`/app/delete-note/`, { params, withCredentials: true })
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
        .get(`/app/disable-note/`, { params, withCredentials: true })
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
  position: relative;
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

/* Line rows inside expanded card */
.note-row { width: 100%; }
.note-line { flex: 1 1 auto; margin-right: 8px; white-space: pre-wrap; word-break: break-word; }

/* Ensure flex children can shrink and cards don't overflow */
.PostitMain { min-width: 0; }
.PostitMain .q-card { max-width: 100%; min-width: 260px; box-sizing: border-box; }

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

/* Minimal star style to remove shadows/glows for rating icons and force single-line layout */
.minimal-stars {
  display: inline-flex;
  flex-wrap: nowrap;
}
.minimal-stars .q-rating__icon,
.minimal-stars .q-rating__icon:before,
.minimal-stars .q-rating__icon--selected,
.minimal-stars .q-focus-helper {
  text-shadow: none !important;
  box-shadow: none !important;
  filter: none !important;
}
</style>


<style scoped>
/* Responsive layout for color and rank pickers (match add note modal) */
.picker-grid {
  display: grid;
  grid-template-columns: 1fr;
  row-gap: 12px;
}
@media (min-width: 768px) {
  .picker-grid {
    grid-template-columns: 1fr auto;
    column-gap: 16px;
    align-items: end;
  }
  .rank-block { justify-self: start; }
}
</style>


<style scoped>
/* Keep the star row under the title always on a single line */
.rank-inline { white-space: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch; }
</style>


<style scoped>
/* Footer row with status (left) and date (right) */
.card-footer { font-size: 12px; display: flex; align-items: center; justify-content: space-between; gap: 8px; width: 100%; }
/* Minimal, background-less status trigger */
.status-chip {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 0;
  line-height: 18px;
  color: #1f2d3d;
  min-height: 0;
  box-shadow: none;
}
/* Tidy up icon/text spacing and add subtle affordance on hover */
.status-chip .q-icon { font-size: 16px; }
.status-chip:hover { text-decoration: underline; }
/* Ensure clicks on the status chip don't propagate to card */
.status-chip, .status-chip * { pointer-events: auto; }
</style>



<style scoped>
/* Line row and inline actions for translate button */
.note-row { gap: 6px; padding: 2px 0; }
.line-left { flex: 1; display: inline-flex; align-items: center; min-width: 0; }
.note-line { white-space: pre-wrap; word-break: break-word; }
.line-actions { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 2px; }
/* Make action buttons appear like small letters next to the text */
.line-actions .q-btn { font-size: 12px; width: 22px; height: 22px; }
.line-actions .q-btn .q-icon { font-size: 16px; }
</style>
