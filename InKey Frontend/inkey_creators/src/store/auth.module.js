import ApiService from '@/common/api.service';
import JwtService from '@/common/jwt.service';
import { CHECK_AUTH, LOGIN, LOGOUT, REGISTER, REMOVE_CREATOR_DATA, REMOVE_ALBUM_DATA, REMOVE_SONG_DATA, CREATE_ALERT } from './actions.type';
import { SET_AUTH, PURGE_AUTH, SET_ERROR, SET_USER } from './mutations.type';

const state = {
  errors: null,
  user: {},
  isAuthenticated: !!JwtService.getToken(),
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  },
};

const actions = {
  [LOGIN](context, credentials) {
    return new Promise((resolve) => {
      ApiService.post('auth/login/', credentials)
        .then(({ data }) => {
          window.localStorage.setItem('USER_ID', data.user.id);
          context.commit(SET_AUTH, data);
          resolve(data);
        })
        .catch(() => {
          context.dispatch(CREATE_ALERT, { status: 'error', message: 'Unable to log you in, please check your credentials.' });
        });
    });
  },
  [LOGOUT](context) {
    context.commit(PURGE_AUTH);
    context.dispatch(REMOVE_CREATOR_DATA);
    context.dispatch(REMOVE_ALBUM_DATA);
    context.dispatch(REMOVE_SONG_DATA);

    context.dispatch(CREATE_ALERT, { status: 'info', message: 'You have been logged out.' });
  },
  [REGISTER](context, credentials) {
    return new Promise((resolve, reject) => {
      ApiService.post('auth/users/', credentials)
        .then(({ data }) => {
          context.dispatch(LOGIN, { email: credentials.email, password: credentials.password });
          resolve(data);
        })
        .catch((error) => {
          context.dispatch(CREATE_ALERT, { status: 'error', message: 'Unable to complete registration, please check your credentials.' });
          reject(error);
        });
    });
  },
  [CHECK_AUTH](context) {
    const id = window.localStorage.getItem('USER_ID');
    if (JwtService.getToken()) {
      ApiService.setHeader();
      ApiService.get(`auth/users/${id}`)
        .then(({ data }) => {
          context.commit(SET_USER, data);
        })
        .catch(() => {
          context.commit(PURGE_AUTH);
        });
    } else {
      context.commit(PURGE_AUTH);
    }
  },
};

const mutations = {
  [SET_ERROR](state, error) {
    state.errors = error;
  },
  [SET_AUTH](state, data) {
    state.isAuthenticated = true;
    state.user = data.user;
    state.errors = {};
    JwtService.saveToken(data.access);
    JwtService.saveRefreshToken(data.refresh);
  },
  [SET_USER](state, data) {
    state.isAuthenticated = true;
    state.user = data;
    state.errors = {};
  },
  [PURGE_AUTH](state) {
    state.isAuthenticated = false;
    state.user = {};
    state.errors = {};
    JwtService.destroyToken();
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
