<template>
  <div id="Search">
    <div v-if="isLoading" class="load-circle">
      <Loading></Loading>
    </div>
    <template v-else>
      <h1 class="main-heading" v-if="allSongs.length > 0">Song results:</h1>
      <div class="songs">
        <template v-for="(track, index) in allSongs">
          <TrackBoxAlt
            :id="track.id"
            :index="index + 1"
            :name="track.name"
            :artist="track.artist"
            :duration="track.duration"
            :rating="track.rating"
            :key="index"
          ></TrackBoxAlt>
        </template>
      </div>
      <h1 class="main-heading" v-if="allArtists.length > 0">Artist results:</h1>
      <div class="artists">
        <template v-for="(artist, index) in allArtists">
          <ArtistBox :id="artist.id" :name="artist.firstname" :coverImage="artist.profile_picture" :key="index"> </ArtistBox>
        </template>
      </div>
      <h1 class="main-heading" v-if="allAlbums.length > 0">Albums results:</h1>
      <div class="albums">
        <template v-for="(album, index) in allAlbums">
          <AlbumBox
            :id="album.id"
            :name="album.name"
            :artist_id="album.artist"
            :artist_name="album.artist_name"
            :coverImage="album.cover_image"
            :key="index"
          ></AlbumBox>
        </template>
      </div>
      <h1 v-if="allAlbums.length == 0 && allSongs.length == 0 && allArtists.length == 0">There are no results!</h1>
    </template>
  </div>
</template>

<script>
import TrackBoxAlt from '../components/TrackBoxAlt';
import ArtistBox from '../components/ArtistBox';
import AlbumBox from '../components/AlbumBox';
import Loading from '../components/Loading';
import { FETCH_SEARCH_RESULTS } from '../store/actions.type';
import { mapGetters } from 'vuex';

export default {
  name: 'Search',
  components: { TrackBoxAlt, ArtistBox, AlbumBox, Loading },
  data() {
    return {
      searchInput: '',
      isLoading: true,
    };
  },

  mounted() {
    this.fetchData();
  },

  watch: {
    $route(to) {
      if (this.searchInput !== this.$route.params.input && this.$route.params.input !== '' && to.name === 'search') this.fetchData();
    },
  },

  methods: {
    async fetchData() {
      this.isLoading = true;
      this.searchInput = this.$route.params.input;
      await this.$store.dispatch(FETCH_SEARCH_RESULTS, this.searchInput);
      this.isLoading = false;
    },
  },

  computed: {
    ...mapGetters(['allSongs', 'allAlbums', 'allArtists']),
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';

.load-circle {
  position: absolute;
  top: 40%;
  left: 50%;
}

.songs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(70rem, 2fr));
  column-gap: 5rem;
}

.albums,
.artists {
  display: grid;
  grid-template-columns: repeat(auto-fit, 35rem);
  grid-template-rows: auto;
  gap: 2rem;
}

.main-heading {
  font-size: 2.5rem;
  color: darken($color: $color-secondary, $amount: 10);
  margin-bottom: 2rem;
  display: block;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: 0rem;
    left: 0;
    width: 100%;
    border: 0;
    height: 1px;
    background: linear-gradient(to left, transparent, $color-secondary, transparent);
  }

  &:not(:first-child) {
    margin-top: 5rem;
  }
}
</style>
