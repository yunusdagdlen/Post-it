import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import NoteListView from "@/views/NoteListView.vue";

const routes = [
  {
    path: "/app",
    name: "home",
    component: HomeView,
  },
  {
    path: "/note-list",
    name: "Note List",
    component: NoteListView,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
