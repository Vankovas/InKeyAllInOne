import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import JwtService from '@/common/jwt.service';
import router from '../router/index';
import store from '../store/auth.module';
import { LOGOUT } from '../store/actions.type';
import { API_URL } from '@/common/config';

const ApiService = {
  init() {
    Vue.use(VueAxios, axios);
    axios.defaults.baseURL = API_URL;
    this.setRefreshTokenInterceptor();
  },

  setHeader() {
    axios.defaults.headers.common['Authorization'] = `Bearer ${JwtService.getToken()}`;
  },

  setRefreshTokenInterceptor() {
    axios.interceptors.response.use(
      (response) => {
        return response;
      },
      (err) => {
        const {
          config,
          response: { status, data },
        } = err;
        const isTokenValidError = status === 401 && data.code === 'token_not_valid';
        const refreshTokenErrorDetail = 'Token is invalid or expired';
        const accessTokenErrorDetail = 'Given token not valid for any token type';
        // if its not a token valid error, continue
        if (!isTokenValidError) {
          return Promise.reject(err);
        }
        // if it's a refresh token error, log out user
        if (data.detail === refreshTokenErrorDetail) {
          store.dispatch(LOGOUT);
          router.push({ name: 'login' });
          return Promise.reject(err);
        }
        // if its an access token error, try to refresh the token
        if (data.detail === accessTokenErrorDetail) {
          return this.refreshToken() // create a method that sends to /auth/token/refresh/
            .then(() => {
              const token = JwtService.getToken();
              config.headers['Authorization'] = `Bearer ${token}`;
              return new Promise((resolve, reject) => {
                axios
                  .request(config)
                  .then((response) => {
                    resolve(response);
                  })
                  .catch((error) => {
                    reject(error);
                  });
              });
            })
            .catch((error) => {
              Promise.reject(error);
            });
        }
      }
    );
  },

  refreshToken() {
    return new Promise((resolve, reject) => {
      axios
        .post('auth/token/refresh/', { refresh: JwtService.getRefreshToken() })
        .then((response) => {
          JwtService.saveToken(response.data.access);
          resolve();
        })
        .catch((err) => reject(err));
    });
  },

  query(resource, params) {
    return axios.get(resource, params).catch((error) => {
      throw new Error(`[InKey] ApiService ${error}`);
    });
  },

  get(resource, slug = '') {
    let url = slug !== ''? `${resource}/${slug}` : resource; 
    return axios.get(url).catch((error) => {
      throw new Error(`[InKey] ApiService ${error}`);
    });
  },

  getWithParams(resource, data) {
    return axios.get(`${resource}`, {
      params: data
    }).catch((error) => {
      throw new Error(`[InKey] ApiService ${error}`);
    });
  },

  post(resource, params) {
    return axios.post(`${resource}`, params);
  },

  postWithFormData(resource, data) {
    return axios.post(`${resource}`, data, { headers: { 'Content-Type': 'multipart/form-data' } });
  },

  update(resource, slug, params) {
    return axios.put(`${resource}/${slug}`, params);
  },

  put(resource, params) {
    return axios.put(`${resource}`, params);
  },

  patchWithFormData(resource, data) {
    return axios.patch(`${resource}`, data, { headers: { 'Content-Type': 'multipart/form-data' } });
  },

  delete(resource) {
    return axios.delete(resource).catch((error) => {
      throw new Error(`[InKey] ApiService ${error}`);
    });
  },
};

export const TrackUploadService = {
  setHeader() {
    axios.defaults.headers.common['Authorization'] = `Bearer ${JwtService.getToken()}`;
  },

  post(resource, data) {
    return axios.post(`${resource}`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export default ApiService;
