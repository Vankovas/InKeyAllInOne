import ApiService from '@/common/api.service';
import { FETCH_SONG, FETCH_TOP_SONGS, FETCH_USER_FAVOURITE_SONGS, ADD_REMOVE_USER_FAVOURITE_SONG, SEND_VOTE } from './actions.type';
import { SET_SELECTED_SONG, SET_TOP_SONGS, SET_USER_FAVOURITE_SONGS } from './mutations.type';

const state = {
	topSongs: [],
	userFavouriteSongs: [],
	selectedSong: {},
};

const getters = {
	topSongs(state) {
		return state.topSongs;
	},
	selectedSong(state) {
		return state.selectedSong;
	},
	favouriteSongs(state) {
		return state.userFavouriteSongs;
	}
};

const actions = {
	[FETCH_SONG](context, id) {
		const fetchSongURL = `/creator/songs/${id}/`;
		return ApiService.get(fetchSongURL)
			.then((res) => {
				context.commit(SET_SELECTED_SONG, res.data);
			})
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
	},
	[FETCH_TOP_SONGS](context) {
		const fetchTopSongsURL = '/creator/songs/';
		return ApiService.getWithParams(fetchTopSongsURL, { ordering: '-rating' })
			.then((res) => {
				context.commit(SET_TOP_SONGS, res.data); // List of songs;
			})
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
	},
	[FETCH_USER_FAVOURITE_SONGS](context) {
		const fetchUserFavouriteSongsURL = '/users-app/favorite/songs/';
		return ApiService.getWithParams(fetchUserFavouriteSongsURL, {}) // auto detect the logged user
			.then((res) => {

				context.commit(SET_USER_FAVOURITE_SONGS, res.data);
			})
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
	},
	[ADD_REMOVE_USER_FAVOURITE_SONG](context, id) {
		const addRemoveUserFavouriteSongsURL = `/users-app/favorite/songs/`;
		return ApiService.post(addRemoveUserFavouriteSongsURL, { song_id: id })
			.then(() => {
				return context.dispatch(FETCH_USER_FAVOURITE_SONGS);
			})
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
	},
	[SEND_VOTE](context, payload) {
		const sendVoteURL = `/creator/rate/songs/`;
		return ApiService.post(sendVoteURL, { song: payload.id, rating: payload.rating })
			.catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
	}
	
};

const mutations = {
	[SET_SELECTED_SONG](state, data) {
		state.selectedSong = data;
	},
	[SET_TOP_SONGS](state, data) {
		state.topSongs = data.slice(0,15); // no more than 15 songs
	},
	[SET_USER_FAVOURITE_SONGS](state, data) {
		state.userFavouriteSongs = data;
	},
};

export default {
	state,
	actions,
	mutations,
	getters,
};
