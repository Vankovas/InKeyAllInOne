import ApiService from '@/common/api.service';

//Actions
import { FETCH_SONG, FETCH_ALL_SONGS, FETCH_ALL_ALBUM_SONGS, CREATE_SONG, UPDATE_SONG, DELETE_SONG, REMOVE_SONG_DATA } from './actions.type';
import { SET_SELECTED_SONG, SET_ALL_SONGS, SET_ALL_ALBUM_SONGS, PURGE_SONG_DATA } from './mutations.type';

const state = {
  songs: [],
  selectedSong: {},
  mappedSongs: {},
};

const getters = {
  allSongs(state) {
    return state.songs;
  },
  selectedSong(state) {
    return state.selectedSong;
  },
  mappedSongs(state) {
    return state.mappedSongs;
  },
};

const actions = {
  [REMOVE_SONG_DATA](context) {
    context.commit(PURGE_SONG_DATA);
  },
  [FETCH_SONG](context, id) {
    const fetchSongURL = '/creator/songs/' + id;
    ApiService.get(fetchSongURL)
      .then((res) => {
        context.commit(SET_SELECTED_SONG, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_ALL_SONGS](context, id) {
    //https://inkey-backend.herokuapp.com/creator/songs/?album__artist__id=20
    const fetchAllSongsURL = '/creator/songs/';
    ApiService.getWithParams(fetchAllSongsURL, { album__artist__id: id })
      .then((res) => {
        if (res.data) {
          context.commit(
            SET_ALL_SONGS,
            res.data.sort(function(a, b) {
              return a.id - b.id;
            })
          );
        }
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_ALL_ALBUM_SONGS](context, id) {
    const fetchAllSongsURL = '/creator/songs/';
    ApiService.getWithParams(fetchAllSongsURL, { album__id: id })
      .then((res) => {
        context.commit(SET_ALL_ALBUM_SONGS, {
          id,
          data: res.data.sort(function(a, b) {
            return a.id - b.id;
          }),
        });
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [CREATE_SONG](context, songData) {
    const createSongURL = '/creator/songs/';
    const { name, description, album, data } = songData;

    let createSongForm = new FormData();

    createSongForm.append('name', name);
    createSongForm.append('description', description);
    createSongForm.append('album', album);
    createSongForm.append('data', data);

    //TODO: Test the way this is handled
    // if (!name) throw new Error('song name is required in order to create a song');

    ApiService.postWithFormData(createSongURL, createSongForm)
      .then(() => {
        if (context.rootState.creator.creator.id) context.dispatch(FETCH_ALL_SONGS, context.rootState.creator.creator.id);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [UPDATE_SONG](context, songData) {
    const dataKeys = ['id', 'name', 'description', 'data', 'album'];

    const updateSongURL = `/creator/songs/${songData['id']}/`;

    let updateSongForm = new FormData();

    dataKeys.forEach((key) => {
      if (key === 'id') return;

      if (songData[key] || typeof songData[key] === 'number') {
        updateSongForm.append(key, songData[key]);
      }
    });

    ApiService.patchWithFormData(updateSongURL, updateSongForm)
      .then(() => {
        context.dispatch(FETCH_SONG, songData['id']);
        if (context.rootState.creator.creator.id) context.dispatch(FETCH_ALL_SONGS, context.rootState.creator.creator.id);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [DELETE_SONG](context, id) {
    const deleteSongRL = `/creator/songs/${id}/`;
    ApiService.delete(deleteSongRL)
      .then(() => {
        if (context.rootState.creator.creator.id) context.dispatch(FETCH_ALL_SONGS, context.rootState.creator.creator.id);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
};

const mutations = {
  [SET_SELECTED_SONG](state, data) {
    state.selectedSong = data;
  },
  [SET_ALL_SONGS](state, data) {
    state.songs = data;
    const updatedMappedSongs = {};
    data.forEach((song) => {
      if (!updatedMappedSongs[song.album] || updatedMappedSongs[song.album].length < 1) updatedMappedSongs[song.album] = [song];
      else updatedMappedSongs[song.album].push(song);
      state.mappedSongs = updatedMappedSongs;
    });
  },
  [SET_ALL_ALBUM_SONGS](state, payload) {
    const { id, data } = payload;
    state.mappedSongs[id] = data;
  },
  [PURGE_SONG_DATA](state) {
    state.songs = [];
    state.selectedSong = {};
    state.mappedSongs = {};
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
