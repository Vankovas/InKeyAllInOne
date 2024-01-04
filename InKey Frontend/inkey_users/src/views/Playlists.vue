<template>
<div>
    <div v-if="isLoading" class="loading">
        <Loading/>
    </div>
    <div v-else>
        <section class="popular-playlists">
            <h1 class="playlists-heading">Popular Playlists</h1>
            <div class="playlists__wrapper">
                <PlaylistBox v-for="playlist in popularPlaylists" :key="playlist.id" :id="playlist.id" :name="playlist.name" :creator="playlist.user_name"/>
            </div>
        </section>
        <section class="trending-playlists">
            <h1 class="playlists-heading">Trending Playlists</h1>
            <div class="playlists__wrapper">
                <PlaylistBox v-for="playlist in trendingPlaylists" :key="playlist.id" :id="playlist.id" :name="playlist.name" :creator="playlist.user_name"/>
            </div>
        </section>
    </div>
</div>

</template>

<script>
import PlaylistBox from '../components/PlaylistBox'
import Loading from '../components/Loading'
import { FETCH_POPULAR_PLAYLISTS, FETCH_TRENDING_PLAYLISTS } from '../store/actions.type';
import { mapGetters } from 'vuex';

export default {

    data() {
        return {
            isLoading: false,
        }
    },
    mounted() {
        this.initData();
    },
    watch: {
        '$route' (to) {
            if(to.name == 'playlists') {
                this.initData();
            }
        } 
    },
    computed: {
        ...mapGetters(['popularPlaylists', 'trendingPlaylists']),
    },
    methods: {
        async initData() {
            this.isLoading = true;
            await this.$store.dispatch(FETCH_POPULAR_PLAYLISTS);
            await this.$store.dispatch(FETCH_TRENDING_PLAYLISTS);
            this.isLoading = false;
        }
    },
    components: {
        PlaylistBox,
        Loading,
    }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.loading {
    position: absolute;
    top: 40%;
    left: 50%;
}

.playlists-heading {
  font-size: 2.5rem;
  color: darken($color: $color-secondary, $amount: 10);
  margin-bottom: 2rem;
  display: inline-block;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px; 
    background: linear-gradient(to left, transparent , $color-secondary, transparent);
  }
}

.playlists__wrapper {
    margin: 2rem 0 3.5rem 0;
    display: grid;
    grid-template-columns: repeat( auto-fit, 20rem );
    grid-template-rows: auto;
    gap: 3rem;

}
</style>