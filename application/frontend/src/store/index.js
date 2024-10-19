import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    postitList: [],
  },
  getters: {
    postitList: (state) => state.postitList,
  },
  mutations: {
    postitList: (state, payload) => {
      state.postitList = payload;
    },
  },
  actions: {
    fetchAllNotes() {
      const workspace_id = this.$route.query?.workspace_id;
      const params = { workspace_id: workspace_id };
      axios
        .get(`http://127.0.0.1:5000/`, { params }, { withCredentials: true })
        .then((response) => {
          if (response.status === 200) {
            this.commit("postitList", response.data);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  modules: {},
});
