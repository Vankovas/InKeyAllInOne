import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './scss/base.scss';
import ApiService from './common/api.service';
import { CHECK_AUTH } from './store/actions.type';
import VueCarousel from 'vue-carousel';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faPlayCircle,
  faStopCircle,
  faPauseCircle,
  faRandom,
  faRedo,
  faVolumeMute,
  faVolumeUp,
  faStepForward,
  faStepBackward,
  faHome,
  faCompactDisc,
  faHeart,
  faBroadcastTower,
  faList,
  faListAlt,
  faEye,
  faEllipsisH,
  faPlus,
  faPlusSquare,
  faPlay,
  faTimes,
  faSearch,
  faAngleDoubleRight,
  faTrashAlt,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Toasted from 'vue-toasted';

library.add(
  faPlayCircle,
  faPauseCircle,
  faStopCircle,
  faRandom,
  faRedo,
  faVolumeMute,
  faVolumeUp,
  faStepForward,
  faStepBackward,
  faHome,
  faCompactDisc,
  faHeart,
  faBroadcastTower,
  faList,
  faListAlt,
  faEye,
  faEllipsisH,
  faPlus,
  faPlusSquare,
  faPlay,
  faTimes,
  faSearch,
  faAngleDoubleRight,
  faTrashAlt
);


// plugin installation
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.use(VueCarousel);
Vue.use(Toasted, {position: 'top-center', duration: 2000, theme: 'toasted-primary'});

Vue.config.productionTip = false;

ApiService.init();

router.beforeEach((to, from, next) => {
  Promise.all([store.dispatch(CHECK_AUTH)]).then(() => {
    if (!store.getters.isAuthenticated && (to.name == 'favourites' || to.name == 'create_playlists')) {
      next({ path: '/' });
    } else {
      next();
    }
  });
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
