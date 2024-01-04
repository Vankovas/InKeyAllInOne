import ApiService from '@/common/api.service';
import {FETCH_ALL_STREAMS} from './actions.type';
import {SET_ALL_STREAMS} from './mutations.type';

const state = {
    allStreams: [],
};
const getters = {
    allStreams(state) {
        return state.allStreams;
    },
};

const actions = {
    [FETCH_ALL_STREAMS](context) {
        const fetchPlaylistURL = `/users-app/stream/`;
        return ApiService.get(fetchPlaylistURL)
            .then((res) => {
                console.log(res);
                context.commit(SET_ALL_STREAMS, res.data);
            })
            .catch((err) => console.error(err)); //TODO: Throw an error to a global error variable ?
    },
};

const mutations = {
    [SET_ALL_STREAMS](state, data) {
        state.allStreams = data;
    },
};

export default {
    state,
    actions,
    mutations,
    getters,
};