<template>
  <div id="app">
    <div class="toast-alerts">
      <template v-for="alert in alerts">
        <ToastAlert :key="alert.uuid" :alert="alert" />
      </template>
    </div>
    <Header />
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

import Header from '@/components/Header';
import ToastAlert from '@/components/common/ToastAlert';

export default {
  name: 'App',
  components: {
    Header,
    ToastAlert,
  },
  computed: {
    ...mapGetters(['alerts']),
  },
};
</script>
