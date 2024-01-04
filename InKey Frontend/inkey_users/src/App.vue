<template>
  <div>
    <TopNavigationBar/>
    <SideNavigationBar/>
      <div class="loading" v-if="loading">
        <loading/>
    </div>
    <main class="main-content" v-else>
      <transition>
        <keep-alive>
          <router-view></router-view>
        </keep-alive>
      </transition>
    </main>
    <!-- Audio player at the bottom of the page - fixed -->
    <song-player></song-player>
  </div>
</template>
<script>
import TopNavigationBar from './components/TopNavigationBar'
import SideNavigationBar from './components/SideNavigationBar'
import SongPlayer from './components/SongPlayer'
import { FETCH_TOP_ALBUMS, FETCH_MOST_VIEWED_ALBUMS, FETCH_TRENDING_ALBUMS, FETCH_TOP_SONGS, FETCH_FEATURED_ARTISTS, FETCH_USER_PLAYLISTS } from './store/actions.type';
import loading from './components/Loading'

export default {
  data() {
    return {
      loading: false,
    }
  },
  components: {
    TopNavigationBar,
    SideNavigationBar,
    SongPlayer,
    loading
  },

  mounted() {
    this.initData();
  },
  methods: {
    async initData() {
      this.loading = true;
      await this.$store.dispatch(FETCH_TOP_ALBUMS);
      await this.$store.dispatch(FETCH_MOST_VIEWED_ALBUMS);
      await this.$store.dispatch(FETCH_TRENDING_ALBUMS);
      await this.$store.dispatch(FETCH_TOP_SONGS);
      await this.$store.dispatch(FETCH_FEATURED_ARTISTS);

      // If logged in 
      await this.$store.dispatch(FETCH_USER_PLAYLISTS);

      this.loading = false;
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./scss/_variables.scss";
@import "./scss/_mixins.scss";

.main-content {
  margin-left: 27rem !important;
  margin-right: 5rem !important;
  padding: 10rem 0 !important;

  @include respond(tablet-port) {
    margin-left: 10rem !important;
    margin-right: 3rem !important;
  }
}

.loading {
  position: absolute;
  top: 40%;
  left: 50%;
}
</style>
