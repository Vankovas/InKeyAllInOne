import TrackUploadService from "@/common/api.service";
import { UPLOAD_AUDIO } from "./actions.type";
import { SET_UPLOAD, SET_ERROR } from "./mutations.type";

const state = {
  error: null,
  fileUploaded: false,
};

const getters = {
  getError(state) {
    return state.error;
  },
  isFileUploaded(state) {
    return state.fileUploaded;
  }
};

const actions = {
  [UPLOAD_AUDIO](context, data) { 
    TrackUploadService.setHeader();
    return new Promise(resolve => {
        TrackUploadService.post("upload/file", data)
        .then(({ data }) => {
          context.commit(SET_UPLOAD);
          resolve(data);
        })
        .catch(({ response }) => {
          context.commit(SET_ERROR, response.data.errors);
        });
    });

    // TESTING
    // setTimeout(()=> {
    //     context.commit(SET_ERROR, "some stupid shit error");
    //     console.log("done");
    // }, 1000)
  },

};

const mutations = {
  [SET_ERROR](state, error) {
    state.error = error;
    state.fileUploaded = false;
  },
  [SET_UPLOAD](state) {
    state.fileUploaded = true;
  },

};

export default {
  state,
  actions,
  mutations,
  getters
};
