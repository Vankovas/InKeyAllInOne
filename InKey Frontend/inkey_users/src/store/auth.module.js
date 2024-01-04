import ApiService from "@/common/api.service";
import JwtService from "@/common/jwt.service";
import {
  CHECK_AUTH,
  LOGIN,
  LOGOUT,
  REGISTER
} from "./actions.type";
import { SET_AUTH, PURGE_AUTH, SET_ERROR, SET_USER } from "./mutations.type";

const state = {
  errors: null,
  user: {},
  isAuthenticated: !!JwtService.getToken()
};

const getters = {
  currentUser(state) {
    return state.user;
  },
  isAuthenticated(state) {
    return state.isAuthenticated;
  },
  getErrors(state){
    return state.errors;
  }
};

const actions = {
  [LOGIN](context, credentials) {
    return ApiService.post("auth/login/", credentials)
        .then(({ data }) => {
          console.log({data: data.user});
          window.localStorage.setItem('USER_ID', data.user.id);
          context.commit(SET_AUTH, data);
        })
        .catch(({response}) => {
          context.commit(SET_ERROR, response.data);
        });
  },
  [LOGOUT](context) {
    context.commit(PURGE_AUTH);
  },
  [REGISTER](context, credentials) {
      return ApiService.post("auth/users/", credentials)
        .then(() => {
          context.dispatch(LOGIN, { email: credentials.email, password: credentials.password });
        })
        .catch(({ response }) => {
          context.commit(SET_ERROR, response.data);
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
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};
