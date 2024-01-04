import ApiService from '@/common/api.service';
import {
    FETCH_PLAYLIST,
    CREATE_PLAYLIST,
    DELETE_PLAYLIST,
    FETCH_USER_PLAYLISTS,
    ADD_SONG_PLAYLIST,
    DELETE_SONG_PLAYLIST,
    FETCH_POPULAR_PLAYLISTS,
    FETCH_TRENDING_PLAYLISTS,
} from './actions.type';
import {
    SET_PLAYLIST,
    SET_USER_PLAYLISTS,
    SET_POPULAR_PLAYLISTS,
    SET_TRENDING_PLAYLISTS,
} from './mutations.type';

const state = {
    selectedPlaylist: {},
    userPlaylists: [],
    popularPlaylists: [],
    trendingPlaylists: [],
};
const getters = {
    selectedPlaylist(state) {
        return state.selectedPlaylist;
    },
    userPlaylists(state) {
        return state.userPlaylists;
    },
    popularPlaylists(state) {
        return state.popularPlaylists;
    },
    trendingPlaylists(state) {
        return state.trendingPlaylists;
    },
};

const actions = {
    [FETCH_PLAYLIST](context, id) {
        const fetchPlaylistURL = `/users-app/playlists/${id}`;
        return ApiService.get(fetchPlaylistURL)
            .then((res) => {
                context.commit(SET_PLAYLIST, res.data);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },
    [FETCH_USER_PLAYLISTS](context) {
        const fetchUserPlaylistsURL = `/users-app/playlists?user=${context.getters.currentUser.id}`;
        return ApiService.get(fetchUserPlaylistsURL)
            .then((res) => {
                context.commit(SET_USER_PLAYLISTS, res.data);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },
    [CREATE_PLAYLIST](context, payload) {
        const createPlaylistURL = '/users-app/playlists/';
        return ApiService.post(createPlaylistURL, {
                name: payload.name,
                description: payload.description,
                add_songs: [],
                delete_songs: [],
            })
            .then(() => {
                return context.dispatch(FETCH_USER_PLAYLISTS);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },
    [DELETE_PLAYLIST](context, id) {
        const deletePlaylistURL = `/users-app/playlists/${id}/`;
        return ApiService.delete(deletePlaylistURL)
            .then(() => {
                return context.dispatch(FETCH_USER_PLAYLISTS);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },
    [ADD_SONG_PLAYLIST](context, payload) {
        const addSongPlaylistURL = `/users-app/playlists/${payload.id}/`;
        return ApiService.patch(addSongPlaylistURL, {
                add_songs: payload.songs
            })
            .then(() => {
                return context.dispatch(FETCH_USER_PLAYLISTS);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },
    [DELETE_SONG_PLAYLIST](context, payload) {
        const addSongPlaylistURL = `/users-app/playlists/${payload.id}/`;
        return ApiService.patch(addSongPlaylistURL, {
                delete_songs: payload.songs
            })
            .then(() => {
                return context.dispatch(FETCH_USER_PLAYLISTS);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },

    // FOR PLAYLISTS PAGE
    [FETCH_POPULAR_PLAYLISTS](context) {
        const fetchMostViewedPlaylistsURL = '/users-app/playlists/';
        return ApiService.getWithParams(fetchMostViewedPlaylistsURL, { ordering: "-views"})
          .then((res) => {
            context.commit(SET_POPULAR_PLAYLISTS, res.data);
          })
          .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
      },
    [FETCH_TRENDING_PLAYLISTS](context) {
        const fetchTrendingPlaylistsURL = '/users-app/playlists/';
        return ApiService.getWithParams(fetchTrendingPlaylistsURL, {ordering: "-created_at"})
          .then((res) => {
            context.commit(SET_TRENDING_PLAYLISTS, res.data);
          })
          .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
      },
};

const mutations = {
    [SET_PLAYLIST](state, data) {
        state.selectedPlaylist = {};
        state.selectedPlaylist = data;
    },
    [SET_USER_PLAYLISTS](state, data) {
        state.userPlaylists = data;
    },
    [SET_POPULAR_PLAYLISTS](state, data) {
        state.popularPlaylists = data;
    },
    [SET_TRENDING_PLAYLISTS](state, data) {
        state.trendingPlaylists = data;
    },
};

export default {
    state,
    actions,
    mutations,
    getters,
};