import Vue from 'vue';
import Vuex from 'vuex';
import auth from './auth.module';
import album from './album.module';
import song from './song.module';
import artist from './artist.module';
import playlist from './playlist.module';
import stream from './stream.module';
import search from './search.module';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    album,
    song,
    artist,
    playlist,
    stream,
    search,
  },
});
