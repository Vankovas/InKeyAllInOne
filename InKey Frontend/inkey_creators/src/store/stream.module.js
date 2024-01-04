import ApiService from '@/common/api.service';

//Actions
import {
  CREATE_STREAM,
  DELETE_STREAM
} from './actions.type';
import { SET_STREAM, PURGE_STREAM } from './mutations.type';

const state = {
  stream: undefined,
};

const getters = {
  getStream(state) {
    return state.stream;
  }
};

const actions = {
  [CREATE_STREAM](context) {
    const createStreamURL = `/users-app/stream/`;
    return ApiService.post(createStreamURL)
      .then((res) => {
        context.commit(SET_STREAM, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [DELETE_STREAM](context) {
    let user_id = context.getters.currentUser.id;
    const deleteStreamURL = `/users-app/stream/${user_id}/`;
    return ApiService.delete(deleteStreamURL)
      .then(() => {
        context.commit(PURGE_STREAM);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
};

const mutations = {
  [SET_STREAM](state, data) {
    state.stream = data;
  },
  [PURGE_STREAM](state) {
    state.stream = undefined;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
