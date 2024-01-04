<template>
  <div>
    <section class="section-hero">
      <div class="section-hero__image">
        <img src="../assets/images/hero-image.png" alt="" />
        <div class="section-hero__image__layer"></div>
      </div>
      <div class="section-hero__content">
        <div class="section-hero__content__headings">
          <h1 class="section-hero__content__heading section-hero__content__heading--1">InKey Music Player</h1>
          <h1 class="section-hero__content__heading section-hero__content__heading--2">Explore, Organize and Enjoy Your Music Collection.</h1>
        </div>
        <div class="section-hero__content__text">
          <p>
            Here you can have all your favorite tracks in one place. Explore all kinds of genres, make your own playlists, and discover new artists. With InKey you can even watch live streams from your favorite musicians.
          </p>
        </div>
        <div class="section-hero__content__cta">
          <a href="http://inkeycreators.surge.sh/" target="_blank"><button class="section-hero__content__cta__btn btn-secondary" type="button">Become A Creator</button></a>
          <button class="section-hero__content__cta__btn btn-secondary" type="button" @click="$router.push('live')">Listen Live</button>
        </div>
      </div>
    </section>
    <section class="section-top-albums">
      <h2 class="main-heading">Top 10 Albums</h2>
      <!-- [[2500, 6],[2100, 5],[1600, 4],[1300, 3],[700, 2], [500, 1], [300, 1]] -->
      <Carousel
        :perPageCustom="[
          [2500, 6],
          [2100, 5],
          [1600, 4],
          [1300, 3],
          [700, 2],
          [500, 1],
          [300, 1],
        ]"
        :paginationEnabled="false"
      >
        <Slide v-for="album in topAlbums" :key="album.id">
          <AlbumBox :id="album.id" :name="album.name" :artist_id="album.artist" :artist_name="album.artist_name" :coverImage="album.cover_image" :rating="album.rating"/>
        </Slide>
      </Carousel>
    </section>
    <section class="section-top-tracks">
      <h2 class="main-heading">Top 15 Tracks</h2>
      <div class="section-top-tracks__group">
        <div v-for="(track, index) in topSongs" :key="track.id">
          <TrackBox
            :id="track.id"
            :index="index + 1"
            :name="track.name"
            :artist="track.artist"
            :duration="track.duration"
            :rating="track.rating"
            :data="track.data"
          />
        </div>
      </div>
    </section>
    <section class="section-featured-artists">
      <h2 class="main-heading">Featured Artists</h2>
      <Carousel
        :perPageCustom="[
          [2500, 6],
          [2100, 5],
          [1600, 4],
          [1300, 3],
          [700, 2],
          [500, 1],
          [300, 1],
        ]"
        :paginationEnabled="false"
      >
        <Slide v-for="artist in featuredArtists" :key="artist.id">
          <ArtistBox :id="artist.id" :name="artist.firstname" :coverImage="artist.profile_picture" />
        </Slide>
      </Carousel>
    </section>
    <section class="section-genres">
      <h2 class="main-heading">Genres</h2>
      <div class="section-genres__group">
        <div class="genre genre--edm">
          <div class="genre__overlay">
            <div class="genre__overlay__highlight"></div>
            <button class="genre__overlay__more-btn btn-secondary" type="button"><font-awesome-icon icon="eye" /></button>
          </div>
          <h2 class="genre__name">EDM</h2>
        </div>
        <div class="genre genre--rock">
          <div class="genre__overlay">
            <div class="genre__overlay__highlight"></div>
            <button class="genre__overlay__more-btn btn-secondary" type="button"><font-awesome-icon icon="eye" /></button>
          </div>
          <h2 class="genre__name">Rock</h2>
        </div>
        <div class="genre genre--hiphop">
          <div class="genre__overlay">
            <div class="genre__overlay__highlight"></div>
            <button class="genre__overlay__more-btn btn-secondary" type="button"><font-awesome-icon icon="eye" /></button>
          </div>
          <h2 class="genre__name">Hip Hop</h2>
        </div>
        <div class="genre genre--pop">
          <div class="genre__overlay">
            <div class="genre__overlay__highlight"></div>
            <button class="genre__overlay__more-btn btn-secondary" type="button"><font-awesome-icon icon="eye" /></button>
          </div>
          <h2 class="genre__name">Pop</h2>
        </div>
        <div class="genre genre--jazz">
          <div class="genre__overlay">
            <div class="genre__overlay__highlight"></div>
            <button class="genre__overlay__more-btn btn-secondary" type="button"><font-awesome-icon icon="eye" /></button>
          </div>
          <h2 class="genre__name">Jazz</h2>
        </div>
      </div>
    </section>
    <footer class="footer"></footer>
  </div>
</template>

<script>
import AlbumBox from '../components/AlbumBox';
import ArtistBox from '../components/ArtistBox';
import TrackBox from '../components/TrackBox';
import { Carousel, Slide } from 'vue-carousel';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {};
  },
  computed: {
    ...mapGetters(['topAlbums', 'topSongs', 'featuredArtists']),
  },

  methods: {},

  components: {
    AlbumBox,
    TrackBox,
    ArtistBox,
    Carousel,
    Slide,
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

.section-hero {
  display: flex;

  &__image {
    position: relative;

    & > img {
      width: 90rem;

      @include respond(desktop) {
        width: 80rem;
      }
      @include respond(laptop) {
        width: 70rem;
      }
      @include respond(small-laptop) {
        display: none;
      }
      @include respond(tablet-land) {
        display: none;
      }
      @include respond(tablet-port) {
        display: none;
      }
    }

    &__layer {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
      background-color: $color-primary-1;
      opacity: 0.4;
    }
  }

  &__content {
    max-width: 80rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-top: 5rem;

    &__headings {
      margin-bottom: 3rem;
    }

    &__heading {
      font-family: inherit;
      font-size: 6rem;
      line-height: 7rem;

      &--2 {
        color: $color-secondary;
      }
    }

    &__text {
      color: #aaaaaa;
      font-size: 2rem;
      font-weight: 400;
      margin-bottom: 2rem;
    }

    &__cta {
      margin-top: 2rem;

      & > *:first-child {
        margin-right: 3rem;
      }

      &__btn {
        padding: 1rem 2rem;
        font-size: 2rem;
        width: 22rem;
        box-shadow: 0 0 1rem 0 rgba($color-white, 0.3);
      }
    }
  }
}

.main-heading {
  font-size: 3.5rem;
  text-shadow: 0 0 2rem rgba($color-white, 0.5);
  margin-bottom: 1rem;
}

.section-top-albums {
  margin-top: 3rem;
}

.section-top-tracks {
  margin-top: 10rem;

  &__group {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(5, 1fr);
    grid-auto-flow: column;
    grid-column-gap: 15rem;

    @include respond(desktop) {
      grid-column-gap: 10rem;
    }

    @include respond(laptop) {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(8, 1fr);
      grid-column-gap: 10rem;
    }

    @include respond(small-laptop) {
      grid-template-columns: repeat(1, 1fr);
      grid-template-rows: repeat(15, 1fr);
      grid-column-gap: 5rem;
    }

    & > * {
      border-bottom: 2px solid $color-primary-2;
    }
  }
}

.section-featured-artists {
  margin-top: 10rem;
}

.section-genres {
  margin-top: 10rem;

  &__group {
    margin-top: 3rem;
    height: 80rem;
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 3rem;

    @include respond(desktop) {
      grid-column-gap: 2rem;
    }

    @include respond(laptop) {
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      grid-column-gap: 2rem;
    }

    @include respond(small-laptop) {
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      grid-column-gap: 2rem;
    }
  }
}

.genre {
  border-radius: 2rem;
  cursor: pointer;
  position: relative;

  &:hover &__overlay__more-btn {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }

  &:hover &__name {
    color: $color-secondary;
  }

  &:hover &__overlay__highlight {
    opacity: 1;
    background-image: linear-gradient(0deg, $color-gray-dark-1 0%, $color-primary-1 0%, $color-primary-3 0%, rgba($color-secondary, 0) 100%);
  }

  &__overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    &__highlight {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border-radius: 2rem;
      opacity: 1;
      transition: all 0.2s ease-in;
    }

    &__more-btn {
      cursor: pointer;
      font-size: 2rem;
      font-weight: 400;
      padding: 1rem;
      border: 2px solid $color-white;
      border-radius: 50%;
      box-shadow: 0 0 2rem rgba($color: $color-white, $alpha: 0.2);
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(3);
      transition: all 0.2s ease-in;
      opacity: 0;

      &:hover {
        box-shadow: 0 0 2rem rgba($color: $color-white, $alpha: 0.8);
        background-color: $color-white;
      }

      & > * {
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }
  }

  & > h2 {
    font-size: 2rem;
    position: absolute;
    top: 1rem;
    left: 2rem;
  }

  &--edm {
    grid-column: 1 / 3;
    grid-row: 1 / 3;

    @include respond(laptop) {
      grid-column: 1 / 2;
      grid-row: 1 / 2;
    }

    background-image: url('../assets/images/edm.jpg');
    background-size: cover;
    background-position: center center;
  }

  &--rock {
    grid-column: 3 / 4;
    grid-row: 1 / 2;

    @include respond(laptop) {
      grid-column: 2 / 3;
      grid-row: 1 / 2;
    }

    background-image: url('../assets/images/rock.jpg');
    background-size: cover;
    background-position: center center;
  }

  &--hiphop {
    grid-column: 3 / 6;
    grid-row: 2 / 3;

    @include respond(laptop) {
      grid-column: 3 / 4;
      grid-row: 1 / 2;
    }

    background-image: url('../assets/images/hiphop.jpg');
    background-size: cover;
    background-position: center center;
  }

  &--pop {
    grid-column: 4 / 6;
    grid-row: 1 / 2;

    @include respond(laptop) {
      grid-column: 2 / 4;
      grid-row: 2 / 3;
    }

    background-image: url('../assets/images/pop.jpg');
    background-size: cover;
    background-position: center center;
  }

  &--jazz {
    grid-column: 6 / 7;
    grid-row: 1 / 3;

    @include respond(laptop) {
      grid-column: 1 / 2;
      grid-row: 2 / 3;
    }

    background-image: url('../assets/images/jazz.jpg');
    background-size: cover;
    background-position: left center;
  }
}

.footer {
  height: 40rem;
}
</style>
