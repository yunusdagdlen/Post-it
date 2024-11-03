const state = {
  baseUrl: "http://localhost:8080",

  // baseUrl: "http://127.0.0.1:5000",
};

const getters = {
  baseUrl: (state) => state.baseUrl,
};

const mutations = {
  baseUrl: (state, payload) => {
    state.baseUrl = payload;
  },
};

const actions = {};

export default {
  state,
  getters,
  mutations,
  actions,
};
