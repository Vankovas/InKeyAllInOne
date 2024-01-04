import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import { CHECK_AUTH } from './store/actions.type';
import ApiService from './common/api.service';
import './scss/base.scss';
import VueAwesomeSwiper from 'vue-awesome-swiper';
import 'swiper/css/swiper.css';
import AudioRecorder from 'vue-audio-recorder';
import Numeral from 'numeral';
import AOS from 'aos';
import 'aos/dist/aos.css';
import Vuelidate from 'vuelidate';

Vue.use(Vuelidate);

Vue.use(Numeral);

Vue.use(VueAwesomeSwiper);
Vue.use(AudioRecorder);

Vue.config.productionTip = false;

ApiService.init();

router.beforeEach((to, from, next) => {
  Promise.all([store.dispatch(CHECK_AUTH)]).then(() => {
    if ((store.getters.isAuthenticated && (to.name == 'login' || to.name == 'register')) || (!store.getters.isAuthenticated && to.name == 'upload')) {
      // forbid routes that can't be accessed without authentication // 1===2 ){
      next({ path: 'login' });
    } else {
      next();
    }
  });
});


new Vue({
  created() {
    AOS.init({ disable: 'phone' });
  },

  router,
  store,
  render: (h) => h(App)
}).$mount('#app');

