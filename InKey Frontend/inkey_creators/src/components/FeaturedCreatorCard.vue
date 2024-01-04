<template>
  <div class="card">
    <div class="card__heading">
      <div class="card__heading__follows">
        <div class="card__heading__follows__icon">
          <img src="../assets/images/follow.png" alt="follow" />
        </div>
        <div class="card__heading__follows__content">
          {{ $props.follows | formatNumber }}
        </div>
      </div>
      <div class="card__bubbles">
        <div class="card__bubbles__small">&nbsp;</div>
        <div class="card__bubbles__medium">&nbsp;</div>
        <div class="card__bubbles__large">&nbsp;</div>
      </div>
      <div class="card__heading__avatar" :style="{ 'background-image': 'url(' + $props.imageUrl + ')' }"></div>
    </div>
    <div class="card__body">
      <div class="card__body__name">
        {{ $props.creatorName }}
        <!-- 15 characters limit-->
      </div>
      <div v-if="featuredCreatorAlbum[this.$props.creatorId] && featuredCreatorAlbum[this.$props.creatorId]['name']" class="card__body__album">
        <div class="card__body__album__icon">
          <img src="../assets/images/music-note.png" alt="music-note" />
        </div>
        <div class="card__body__album__content">
          {{ featuredCreatorAlbum[this.$props.creatorId]['name'] }}
          <!-- 40 characters limit-->
        </div>
      </div>
    </div>
    <div class="card__footer">
      <div class="card__footer__likes">
        <div class="card__footer__likes__icon">
          <img src="../assets/images/heart.png" alt="heart" />
        </div>
        <div class="card__footer__likes__content">
          {{ $props.likes | formatNumber }}
        </div>
      </div>
      <div class="card__footer__more-info">
        <router-link class="card__footer__more-info__btn" exact :to="{ name: 'profile', params: { id: this.$props.creatorId } }">
          See Profile&rarr;
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { FETCH_FEATURED_CREATOR_ALBUM } from '../store/actions.type';

import numeral from 'numeral';

export default {
  mounted() {
    this.loadFeaturedCreatorAlbum(0, 10);
  },
  computed: {
    ...mapGetters(['featuredCreatorAlbum']),
  },
  data() {
    return {
      fetchedAlbumName: 'No Album',
    };
  },
  props: {
    creatorId: Number,
    creatorName: String,
    albumName: String,
    likes: Number,
    follows: Number,
    imageUrl: String,
  },
  filters: {
    formatNumber: function(value) {
      return numeral(value).format('0,0');
    },
  },
  methods: {
    loadFeaturedCreatorAlbum(attemptNo, maxAttempts) {
      const userId = this.$props.creatorId;
      this.$store.dispatch(FETCH_FEATURED_CREATOR_ALBUM, userId);

      if (attemptNo >= maxAttempts) throw 'Could not load featured creator album on time';
      if (!this.featuredCreatorAlbum[userId])
        return setTimeout(() => {
          this.loadFeaturedCreatorAlbum(attemptNo + 1, maxAttempts);
        }, 500);
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';

.card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: $color-white;
  border-radius: 0.5rem;

  &__heading {
    width: 100%;
    height: 18.5rem;
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
    background-image: linear-gradient(-90deg, $color-tertiary 0, $color-primary 100%);
    position: relative;

    &__avatar {
      background-image: url(https://media.nu.nl/m/utfx1mpa5ljy_wd640.jpeg);
      background-size: cover;
      background-repeat: no-repeat;
      width: 18rem;
      height: 18rem;
      border-radius: 50%;
      position: absolute;
      top: 2.5rem;
      left: 7rem;
      z-index: 20;
    }

    &__follows {
      display: flex;
      align-items: center;
      position: absolute;
      top: 1rem;
      right: 1rem;
      background-color: $color-white;
      padding: 0.2rem 0.8rem;
      border-radius: 1.5rem;

      &__icon {
        width: 2rem;
        margin-right: 0.5rem;
      }

      &__icon > * {
        width: 100%;
      }

      &__content {
        font-family: inherit;
        font-weight: 500;
        font-size: 1.4rem;
        line-height: 2.3rem;
        text-align: center;
        color: #000;
      }
    }
  }

  &__bubbles {
    position: relative;
    &__small {
      opacity: 0.8;
      background-image: linear-gradient(100deg, $color-primary 0, $color-tertiary 100%);
      width: 2rem;
      height: 2rem;
      border-radius: 50%;
      position: absolute;
      top: 23rem;
      left: 10rem;
      z-index: 21;
    }
    &__medium {
      opacity: 0.4;
      background-image: linear-gradient(-100deg, $color-primary 0, $color-tertiary 100%);
      width: 7rem;
      height: 7rem;
      border-radius: 50%;
      position: absolute;
      top: 5rem;
      left: 2rem;
      z-index: 21;
    }
    &__large {
      opacity: 0.9;
      background-image: linear-gradient(-150deg, $color-primary 0, $color-tertiary 100%);
      width: 20rem;
      height: 20rem;
      border-radius: 50%;
      position: absolute;
      top: 3rem;
      left: 8rem;
      z-index: 19;
    }
  }

  &__body {
    width: 100%;
    height: 12.5rem;
    padding-top: 6.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;

    &__name {
      font-family: inherit;
      font-weight: 600;
      font-size: 3.5rem;
      color: #000;
    }

    &__album {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 5rem;

      &__icon {
        width: 2rem;
        height: 2rem;
        margin-right: 1rem;
      }

      &__icon > * {
        width: 100%;
      }

      &__content {
        font-family: inherit;
        font-weight: 500;
        font-size: 1.8rem;
        line-height: 2.3rem;
        text-align: center;
        color: #000;
      }
    }
  }

  &__footer {
    border-top: 1px solid $color-gray-light-1;
    width: 80%;
    flex: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;

    &__likes {
      display: flex;
      align-items: center;

      &__icon {
        width: 2rem;
        height: 2rem;
        margin-right: 1rem;
      }

      &__icon > * {
        width: 100%;
      }

      &__content {
        font-family: inherit;
        font-weight: 500;
        font-size: 1.6rem;
        line-height: 2.3rem;
        text-align: center;
        color: #000;
      }
    }

    &__more-info {
      &__btn {
        cursor: pointer;
        outline: none;
        white-space: nowrap;
        border: none;
        font-family: inherit;
        font-size: 1.7rem;
        font-weight: 600;
        letter-spacing: 0.1rem;
        height: 5rem;
        width: 10rem;
        border-radius: 6.4rem;
        background-color: transparent;
        color: $color-primary;
        transition: all 0.2s;

        &:hover {
          text-decoration: underline;
          color: $color-secondary;
        }

        &:active {
          text-decoration: underline;
          color: $color-tertiary;
          transform: translateY(1px);
        }
      }
    }
  }
}
</style>
