<template>
  <div id="UserBanner">
    <div class="user-banner">
      <div class="user-banner__image">
        <img
          v-bind:style="{
            backgroundImage: 'url(' + (currentCreator.profile_picture || require('../assets/images/hero-image.jpg')) + ')',
          }"
        />
      </div>
      <div class="user-banner__info">
        <div class="user-banner__info__person">
          <div v-if="currentCreator.firstname || currentCreator.lastname">
            <h1>{{ `${currentCreator.firstname} ${currentCreator.lastname}` }}</h1>
            <h3>{{ currentCreator.username }}</h3>
          </div>
          <h1 v-else>{{ currentCreator.username }}</h1>
          <p>{{ currentCreator.description }}</p>
        </div>
        <div class="user-banner__info__content">
          <div class="user-banner__info__content__panel">
            <!-- //TODO: Icon or img and add panel data -->
            {{ (Math.random(0, 1) * 10000) | formatNumber }} Follows
            <img src alt />
            <p></p>
          </div>
          <!-- Likes Panel -->
          <div class="user-banner__info__content__panel">
            <!-- //TODO: Icon or img and add panel data -->
            {{ (Math.random(0, 1) * 10000) | formatNumber }} Likes
            <img src alt />
            <p></p>
          </div>
        </div>
      </div>
      <div class="user-banner__edit">
        <template v-if="currentCreator.id && currentUser.id && currentCreator.id === currentUser.id">
          <button type="button" class="user-banner__edit__btn btn-secondary" @click="this.showEditUserModal">Edit profile</button>
        </template>
      </div>
    </div>
    <EditUser @hideModal="this.hideEditUserModal" v-if="isModalVisible === true" v-bind:user="this.currentCreator"></EditUser>
  </div>
</template>

<script>
import numeral from 'numeral';

import { mapGetters } from 'vuex';

import EditUser from '../components/EditUser';
export default {
  data() {
    return {
      isModalVisible: false,
    };
  },

  methods: {
    showEditUserModal() {
      this.isModalVisible = true;
    },

    hideEditUserModal() {
      this.isModalVisible = false;
    },
  },

  components: {
    EditUser,
  },

  computed: {
    ...mapGetters(['currentCreator', 'currentUser']),
  },

  filters: {
    formatNumber: function(value) {
      return numeral(value).format('0,0');
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

#UserBanner {
  width: 100%;
}

.user-banner {
  display: flex;
  align-items: center;
  margin: auto;
  width: 100rem;

  @include respond(tablet-land) {
    width: 100%;
  }

  &__image {
    img {
      width: 20rem;
      height: 20rem;
      background-size: cover;
      background-clip: padding-box;
      background-position: center center;
      border-radius: 50%;
    }
  }

  &__info {
    font-size: 1.6rem;
    font-family: inherit;
    font-weight: 500;
    color: $color-white;
    margin-left: 2rem;

    &__person {
      max-width: 50rem;
      display: flex;
      flex-direction: column;
      justify-content: center;

      h3,
      p {
        padding-left: 0.5rem;
      }
    }

    &__content {
      display: flex;
      align-items: center;
      margin-top: 2rem;

      &__panel {
        margin-right: 2rem;
        font-size: 2rem;
      }
    }
  }

  &__edit {
    margin-left: auto;

    &__btn {
      font-size: 1.6rem;
      font-family: inherit;
      font-weight: 500;
      color: $color-white;
      border: 1px solid $color-white;
      padding: 1rem 2rem;
      border-radius: 2rem;

      &:hover {
        background-color: $color-white;
        color: $color-tertiary;
      }

      &:active {
        transform: translateY(2px);
      }
    }
  }
}
</style>
