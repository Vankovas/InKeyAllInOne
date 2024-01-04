import Vue from 'vue';
import Vuex from 'vuex';

import alert from './alert.module';
import auth from './auth.module';
import upload from './upload.module';
import creator from './creator.module';
import album from './album.module';
import song from './song.module';
import stream from './stream.module';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    alert,
    auth,
    upload,
    creator,
    album,
    song,
    stream,
  },
});
