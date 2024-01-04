import ApiService from '@/common/api.service';
import { FETCH_ALBUM, FETCH_TOP_ALBUMS, FETCH_MOST_VIEWED_ALBUMS, FETCH_TRENDING_ALBUMS, FETCH_USER_FAVOURITE_ALBUMS, ADD_REMOVE_USER_FAVOURITE_ALBUM, FETCH_SONGS_ALBUM, SEND_ALBUM_VOTE } from './actions.type';
import { SET_SELECTED_ALBUM, SET_TOP_ALBUMS, SET_MOST_VIEWED_ALBUMS, SET_TRENDING_ALBUMS, SET_USER_FAVOURITE_ALBUMS, SET_SONGS_ALBUM } from './mutations.type';

const state = {
  selectedAlbum: {},
  topAlbums: [],
  mostViewedAlbums: [],
  trendingAlbums: [],
  userFavouriteAlbums: [],
  songsAlbum: [],
};

const getters = {
  selectedAlbum(state) {
    return state.selectedAlbum;
  },
  topAlbums(state) {
    return state.topAlbums;
  },
  mostViewedAlbums(state) {
    return state.mostViewedAlbums;
  },
  trendingAlbums(state) {
    return state.trendingAlbums;
  },
  userFavouriteAlbums(state) {
    return state.userFavouriteAlbums;
  },
  songsAlbum(state) {
    return state.songsAlbum;
  },
};

const actions = {
  [FETCH_ALBUM](context, id) {
    const fetchAlbumURL = `/creator/albums/${id}`;
    return ApiService.get(fetchAlbumURL)
      .then((res) => {
        context.commit(SET_SELECTED_ALBUM, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_TOP_ALBUMS](context) {
    const fetchTopAlbumsURL = '/creator/albums/';
    return ApiService.getWithParams(fetchTopAlbumsURL, { ordering: "-rating"})
      .then((res) => {
        context.commit(SET_TOP_ALBUMS, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_MOST_VIEWED_ALBUMS](context) {
    const fetchMostViewedAlbumsURL = '/creator/albums/';
    return ApiService.getWithParams(fetchMostViewedAlbumsURL, { ordering: "-views"})
      .then((res) => {
        context.commit(SET_MOST_VIEWED_ALBUMS, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_TRENDING_ALBUMS](context) {
    const fetchTrendingAlbumsURL = '/creator/albums/';
    return ApiService.getWithParams(fetchTrendingAlbumsURL, { ordering: "-created_at"})
      .then((res) => {
        context.commit(SET_TRENDING_ALBUMS, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
	[FETCH_USER_FAVOURITE_ALBUMS](context) {
		const fetchUserFavouriteAlbumsURL = `/users-app/favorite/albums`;
		return ApiService.get(fetchUserFavouriteAlbumsURL) // auto detect the logged user
			.then((res) => {
				context.commit(SET_USER_FAVOURITE_ALBUMS, res.data );
			})
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
	// If no album with that id - add, if album exists - delete
	[ADD_REMOVE_USER_FAVOURITE_ALBUM](context, id) {
		const addRemoveUserFavouriteAlbumsURL = `/users-app/favorite/albums/`;  // IF THIS DONT WORK - TRY WITH PARAMETER
    return ApiService.post(addRemoveUserFavouriteAlbumsURL, { album_id: id })
			.then(() => {
				return context.dispatch(FETCH_USER_FAVOURITE_ALBUMS); // TODO: CHECK IF WORKS !
			})
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_SONGS_ALBUM](context, id) {
    const fetchAlbumsSongsURL = `/creator/songs/`;
    return ApiService.getWithParams(fetchAlbumsSongsURL,  { album__id: id })
        .then((res) => {
          context.commit(SET_SONGS_ALBUM, res.data );
        })
        .catch((err) => console.error(err));
  },
	[SEND_ALBUM_VOTE](context, payload) {
		const sendAlbumVoteURL = `/creator/rate/albums/`;
		return ApiService.post(sendAlbumVoteURL, { album: payload.id, rating: payload.rating })
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
	}
};

const mutations = {
  [SET_SELECTED_ALBUM](state, data) {
    state.selectedAlbum = {};
    state.selectedAlbum = data;
  },
  [SET_TOP_ALBUMS](state, data) {
    state.topAlbums = data.slice(0,10);
  },
  [SET_MOST_VIEWED_ALBUMS](state, data) {
    state.mostViewedAlbums = data.slice(0,10);
  },
  [SET_TRENDING_ALBUMS](state, data) {
    state.trendingAlbums = data.slice(0,10);
  },
  [SET_USER_FAVOURITE_ALBUMS](state, data) {
    state.userFavouriteAlbums = data;
  },
  [SET_SONGS_ALBUM](state, data) {
    state.songsAlbum = [];
    state.songsAlbum = data;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
