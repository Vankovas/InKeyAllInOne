import ApiService from '@/common/api.service';

//Actions
import {
  FETCH_ALBUM,
  FETCH_ALL_ALBUMS,
  CREATE_ALBUM,
  UPDATE_ALBUM,
  DELETE_ALBUM,
  REMOVE_ALBUM_DATA,
  FETCH_ALL_SONGS,
  FETCH_FEATURED_CREATOR_ALBUM,
} from './actions.type';
import { SET_SELECTED_ALBUM, SET_ALL_ALBUMS, PURGE_ALBUM_DATA, SET_FEATURED_CREATOR_ALBUM } from './mutations.type';

const state = {
  albums: [],
  selectedAlbum: {},
  featuredCreatorAlbum: {},
};

const getters = {
  allAlbums(state) {
    return state.albums;
  },
  selectedAlbum(state) {
    return state.selectedAlbum;
  },
  featuredCreatorAlbum(state) {
    return state.featuredCreatorAlbum;
  },
};

const actions = {
  [REMOVE_ALBUM_DATA](context) {
    context.commit(PURGE_ALBUM_DATA);
  },
  [FETCH_FEATURED_CREATOR_ALBUM](context, id) {
    //https://inkey-backend.herokuapp.com/creator/albums/?artist__id=9
    const fetchFeaturedCreatorAlbumURL = '/creator/albums/';
    ApiService.getWithParams(fetchFeaturedCreatorAlbumURL, { artist__id: id })
      .then((res) => {
        let album = {};
        if (res.data && res.data[0]) album = res.data[0];
        context.commit(SET_FEATURED_CREATOR_ALBUM, { album, id });
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_ALBUM](context, id) {
    const fetchAlbumURL = `/creator/albums/${id}`;

    ApiService.get(fetchAlbumURL)
      .then((res) => {
        context.commit(SET_SELECTED_ALBUM, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_ALL_ALBUMS](context, id) {
    //https://inkey-backend.herokuapp.com/creator/albums/?artist__id=9
    const fetchAllAlbumsURL = '/creator/albums/';
    ApiService.getWithParams(fetchAllAlbumsURL, { artist__id: id })
      .then((res) => {
        context.commit(SET_ALL_ALBUMS, res.data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [CREATE_ALBUM](context, albumData) {
    const createAlbumURL = '/creator/albums/';
    const { name, description, is_private, cover_image } = albumData;

    let createAlbumForm = new FormData();

    createAlbumForm.append('name', name);
    createAlbumForm.append('description', description);
    createAlbumForm.append('is_private', is_private);
    createAlbumForm.append('cover_image', cover_image);

    //TODO: Test the way this is handled
    // if (!name) throw new Error('album name is required in order to create an ablum');

    ApiService.postWithFormData(createAlbumURL, createAlbumForm)
      .then(() => {
        if (context.rootState.creator.creator.id) {
          context.dispatch(FETCH_ALL_SONGS, context.rootState.creator.creator.id);
          context.dispatch(FETCH_ALL_ALBUMS, context.rootState.creator.creator.id);
        }
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [UPDATE_ALBUM](context, updatedData) {
    const dataKeys = ['id', 'name', 'description', 'is_private', 'cover_image'];

    const updateAlbumURL = `/creator/albums/${updatedData['id']}/`;

    let updateAlbumForm = new FormData();

    dataKeys.forEach((key) => {
      if (key === 'id') return;

      if ((key === 'is_private' && updatedData[key] !== undefined) || updatedData[key]) {
        updateAlbumForm.append(key, updatedData[key]);
      }
    });

    ApiService.patchWithFormData(updateAlbumURL, updateAlbumForm)
      .then(() => {
        context.dispatch(FETCH_ALBUM, updatedData['id']);
        if (context.rootState.creator.creator.id) {
          context.dispatch(FETCH_ALL_SONGS, context.rootState.creator.creator.id);
          context.dispatch(FETCH_ALL_ALBUMS, context.rootState.creator.creator.id);
        }
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [DELETE_ALBUM](context, id) {
    const deleteAlbumURL = `/creator/albums/${id}/`;
    ApiService.delete(deleteAlbumURL)
      .then(() => {
        if (context.rootState.creator.creator.id) {
          context.dispatch(FETCH_ALL_SONGS, context.rootState.creator.creator.id);
          context.dispatch(FETCH_ALL_ALBUMS, context.rootState.creator.creator.id);
        }
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
};

const mutations = {
  [SET_SELECTED_ALBUM](state, data) {
    state.selectedAlbum = data;
  },
  [SET_ALL_ALBUMS](state, data) {
    state.albums = data;
  },
  [PURGE_ALBUM_DATA](state) {
    state.albums = [];
    state.selectedAlbum = {};
  },
  [SET_FEATURED_CREATOR_ALBUM](state, data) {
    const { id, album } = data;
    state.featuredCreatorAlbum = { ...state.featuredCreatorAlbum, [id]: album };
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
