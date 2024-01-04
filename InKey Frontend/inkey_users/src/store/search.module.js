import ApiService from '@/common/api.service';
import { FETCH_SEARCH_RESULTS } from './actions.type';
import { SET_SEARCH_RESULTS } from './mutations.type';

const state = {
  artists: [],
  songs: [],
  albums: [],
};

const getters = {
  allSongs(state) {
    return state.songs;
  },
  allArtists(state) {
    return state.artists;
  },
  allAlbums(state) {
    return state.albums;
  },
};

const actions = {
  [FETCH_SEARCH_RESULTS](context, inputMessage) {
    const message = encodeURI(inputMessage);
    console.log('message -> ', message);

    const fetchAlbumsURL = `/creator/albums/?search=${message}`;
    const fetchSongsURL = `/creator/songs/?search=${message}`;
    const fetchArtistsURL = `/auth/users/?search=${message}`;

    return Promise.all([ApiService.get(fetchAlbumsURL), ApiService.get(fetchSongsURL), ApiService.get(fetchArtistsURL)])
      .then(([albums, songs, artists]) => {
        context.commit(SET_SEARCH_RESULTS, { albums: albums.data, songs: songs.data, artists: artists.data });
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
};

const mutations = {
  [SET_SEARCH_RESULTS](state, data) {
    const { albums, songs, artists } = data;
    state.albums = albums;
    state.songs = songs;
    state.artists = artists;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
