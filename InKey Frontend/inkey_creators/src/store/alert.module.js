import { uuid } from 'uuidv4';

import { CREATE_ALERT, REMOVE_ALERT } from './actions.type';
import { ADD_ALERT, DELETE_ALERT } from './mutations.type';

const state = {
  alerts: [],
};

const getters = {
  alerts(state) {
    return state.alerts;
  },
};

const actions = {
  [CREATE_ALERT](context, alert) {
    const { status, message } = alert;
    const newAlert = {
      uuid: uuid(),
      status,
      message,
    };
    console.log(newAlert);
    context.commit(ADD_ALERT, newAlert);
  },
  [REMOVE_ALERT](context, id) {
    context.commit(DELETE_ALERT, id);
  },
};

const mutations = {
  [ADD_ALERT](state, alert) {
    const updatedAlerts = [...state.alerts, alert];
    state.alerts = updatedAlerts;
  },
  [DELETE_ALERT](state, id) {
    const filteredAlerts = state.alerts.filter((alert) => alert.uuid !== id);
    state.alerts = filteredAlerts;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
