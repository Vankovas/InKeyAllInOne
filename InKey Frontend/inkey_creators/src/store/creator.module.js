import ApiService from '@/common/api.service';

//Actions
import { FETCH_CREATOR, UPDATE_CREATOR, REMOVE_CREATOR_DATA, FETCH_FEATURED_CREATORS } from './actions.type';
import { SET_CREATOR, PURGE_CREATOR_DATA, SET_FEATURED_CREATORS } from './mutations.type';

const state = {
  creator: {},
  featuredCreators: [],
};

const getters = {
  currentCreator(state) {
    return state.creator;
  },
  featuredCreators(state) {
    return state.featuredCreators;
  },
};

const actions = {
  [REMOVE_CREATOR_DATA](context) {
    context.commit(PURGE_CREATOR_DATA);
  },
  [FETCH_FEATURED_CREATORS](context) {
    const fetchFeaturedArtistsURL = '/auth/users/';
    ApiService.getWithParams(fetchFeaturedArtistsURL, { ordering: '-id' })
      .then((res) => {
        const data = res.data || [];
        context.commit(SET_FEATURED_CREATORS, data);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [FETCH_CREATOR](context, id) {
    const fetchCreatorURL = '/auth/users/' + id;
    ApiService.get(fetchCreatorURL)
      .then((res) => {
        if (res.data) {
          console.log(res.data);
          const { id, username, email, firstname, lastname, description, profile_picture, settings } = res.data;
          const userData = {
            id: id || null,
            username: username || '',
            email: email || '',
            firstname: firstname || '',
            lastname: lastname || '',
            description: description || '',
            profile_picture: profile_picture || null,
            settings: settings || null,
          };

          context.commit(SET_CREATOR, userData);
        } else throw 'Could not fetch creator';
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
  [UPDATE_CREATOR](context, creatorData) {
    console.log(creatorData);
    const dataKeys = ['id', 'username', 'firstname', 'lastname', 'email', 'password', 'confirmPassword', 'description', 'profile_picture'];

    const updateSongURL = `/auth/users/${creatorData['id']}/`;

    console.log(updateSongURL);
    let updateCreatorForm = new FormData();

    dataKeys.forEach((key) => {
      if (key === 'id') return;

      if (creatorData[key] || typeof creatorData[key] === 'number') {
        updateCreatorForm.append(key, creatorData[key]);
      }
    });

    ApiService.patchWithFormData(updateSongURL, updateCreatorForm)
      .then(() => {
        context.dispatch(FETCH_CREATOR, creatorData['id']);
      })
      .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
  },
};

const mutations = {
  [SET_CREATOR](state, data) {
    state.creator = data;
  },
  [PURGE_CREATOR_DATA](state) {
    state.creator = {};
  },
  [SET_FEATURED_CREATORS](state, data) {
    state.featuredCreators = data;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
