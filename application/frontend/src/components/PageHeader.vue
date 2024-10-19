<template class="">
  <div class="PageHeader">
    <q-header class="HeaderToolbar bordered bg-white">
      <q-toolbar class="q-px-xl rounded bordered">
        <q-toolbar-title class="text-weight-medium">NotedFlow</q-toolbar-title>
        <div class="q-mr-md">
          <q-btn
            rounded
            flat
            dense
            icon="mdi-pencil-plus-outline"
            class="q-px-md"
            @click="newNoteDialog"
          />
        </div>
        <div>
          <q-btn rounded flat dense icon="mdi-menu" class="q-px-md">
            <q-menu
              fit
              anchor="bottom start"
              self="top start"
              transition-show="jump-down"
              transition-hide="jump-up"
            >
              <q-list style="min-width: 100px">
                <q-item clickable>
                  <q-item-section> Note List </q-item-section>
                </q-item>
                <q-item clickable>
                  <q-item-section>Save Workspace</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>
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
  <q-dialog v-model="a" :position="position">
    <q-card style="width: 350px">
      <q-linear-progress :value="0.6" color="pink" />

      <q-card-section class="row items-center no-wrap">
        <div>
          <div class="text-weight-bold">The Walker</div>
          <div class="text-grey">Fitz & The Tantrums</div>
        </div>

        <q-space />

        <q-btn flat round icon="fast_rewind" />
        <q-btn flat round icon="pause" />
        <q-btn flat round icon="fast_forward" />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import axios from "axios";

export default {
  name: "PageHeader",
  data() {
    return {
      newNote: false,
      content: "",
      title: "",
      color: "",
    };
  },
  emits: ["success"],
  methods: {
    saveNewNote() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = {
        note: this.content,
        title: this.title,
        color: this.color,
        workspace_id: workspace_id,
      };
      console.log(params);
      axios
        .get(`http://127.0.0.1:5000/add`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.newNote = false;
            this.content = "";
            this.title = "";
            this.color = "";
            this.$emit("success");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    newNoteDialog() {
      console.log("here");
      const colorList = ["#00BFB2", "#55dde0", "#8ac926", "#04395e", "#f26419"];
      const colorId = Math.floor(Math.random() * 6);
      this.color = colorList[colorId];
      this.newNote = true;
    },
  },
};
</script>

<style scoped>
.PageHeader {
  background: transparent;
  width: 100%;
  height: 20px;
  .HeaderToolbar {
    background: none;
    border-radius: 15px;
    border: 2px solid #adb5bd;
    color: #adb5bd;
    font-weight: 700;
    margin-left: 10vh;
    margin-right: 10vh;
    margin-top: 5vh;
  }
}
</style>
