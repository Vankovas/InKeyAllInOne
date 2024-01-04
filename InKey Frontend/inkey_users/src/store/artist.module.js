import ApiService from '@/common/api.service';
import { FETCH_ARTIST, FETCH_FEATURED_ARTISTS, FETCH_USER_FAVOURITE_ARTISTS, ADD_REMOVE_USER_FAVOURITE_ARTIST, FETCH_SONGS_ARTIST, FETCH_ALBUMS_ARTIST } from './actions.type';
import { SET_SELECTED_ARTIST, SET_FEATURED_ARTISTS, SET_USER_FAVOURITE_ARTISTS, SET_SONGS_ARTIST, SET_ALBUMS_ARTIST } from './mutations.type';


const state = {
  selectedArtist: {},
  featuredArtists: [],
  userFavouriteArtists: [],
  songsArtist: [],
  albumsArtist: [],
};

const getters = {
  selectedArtist(state) {
    return state.selectedArtist;
  },
  featuredArtists(state) {
    return state.featuredArtists;
  },
  userFavouriteArtists(state) {
    return state.userFavouriteArtists;
  },
  songsArtist(state) {
    return state.songsArtist;
  },
  albumsArtist(state) {
    return state.albumsArtist;
  },
};

const actions = {
  [FETCH_ARTIST](context, id) {
    const fetchArtistURL = `/auth/users/${id}`;
    return ApiService.get(fetchArtistURL)
      .then((res) => {
        context.commit(SET_SELECTED_ARTIST, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_FEATURED_ARTISTS](context) {
    const fetchFeaturedArtistsURL = '/auth/users/'; 
    return ApiService.getWithParams(fetchFeaturedArtistsURL, { ordering: '-id' })
      .then((res) => {
        context.commit(SET_FEATURED_ARTISTS, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_USER_FAVOURITE_ARTISTS](context, id) {
    const fetchUserFavouriteArtistsURL = '/users-app/favorite/artists/'; 
    return ApiService.getWithParams(fetchUserFavouriteArtistsURL, { artist__id: id })
      .then((res) => {
        context.commit(SET_USER_FAVOURITE_ARTISTS, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [ADD_REMOVE_USER_FAVOURITE_ARTIST](context, id) {
    const addRemoveUserFavouriteArtistsURL = `/users-app/favorite/artists/`;
    return ApiService.post(addRemoveUserFavouriteArtistsURL, { artist_id: id })
        .then(() => {
            return context.dispatch(FETCH_USER_FAVOURITE_ARTISTS);
        })
        .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_SONGS_ARTIST](context, id) {
    const fetchArtistSongsURL = `/creator/songs/`;
    return ApiService.getWithParams(fetchArtistSongsURL, { album__artist__id: id } )
        .then((res) => {
          context.commit(SET_SONGS_ARTIST, res.data );
        })
        .catch((err) => console.error(err));
  },
  [FETCH_ALBUMS_ARTIST](context, id) {
    const fetchAlbumsArtistURL = `/creator/albums/`;
    return ApiService.getWithParams(fetchAlbumsArtistURL, { artist__id: id })
        .then((res) => {
          context.commit(SET_ALBUMS_ARTIST, res.data );
        })
        .catch((err) => console.error(err));
  }
};

const mutations = {
  [SET_SELECTED_ARTIST](state, data) {
    state.selectedArtist = {};
    state.selectedArtist = data;
  },
  [SET_FEATURED_ARTISTS](state, data) {
    state.featuredArtists = data.slice(0,10);
  },
  [SET_USER_FAVOURITE_ARTISTS](state, data) {
    state.userFavouriteArtists = data;
  },
  [SET_SONGS_ARTIST](state, data) {
    state.songsArtist = [];
    state.songsArtist = data;
  },
  [SET_ALBUMS_ARTIST](state, data) {
    state.albumsArtist = [];
    state.albumsArtist = data;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
