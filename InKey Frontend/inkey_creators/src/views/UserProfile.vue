<template>
  <div class="user-profile">
    <div class="user-profile-container">
      <div class="user-profile__header">
        <UserBanner></UserBanner>
      </div>
      <div class="user-profile__content">
        <tabs>
          <tab name="Songs" :selected="true">
            <UserSongsAlt :creatorId="this.id"></UserSongsAlt>
          </tab>
          <tab name="Albums" class="user-profile__content__tabs user-profile__content__tabs--album">
            <UserAlbumsAlt :creatorId="this.id"></UserAlbumsAlt>
          </tab>
          <tab v-if="currentUser && currentUser.id == this.id" name="Stream" class="user-profile__content__tabs user-profile__content__tabs--stream">
            <Stream></Stream>
          </tab>
        </tabs>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { FETCH_CREATOR } from '../store/actions.type';

import UserBanner from '../components/UserBanner';
import UserAlbumsAlt from '../components/UserAlbumsAlt';
import UserSongsAlt from '../components/UserSongsAlt';
import Tabs from '../components/common/Tabs';
import Tab from '../components/common/Tab';
import Stream from '../views/Stream';

export default {
  created() {
    this.loadCreator(0, 10);
  },

  data() {
    return {
      id: this.$route.params.id,
    };
  },

  name: 'UserProfile',
  components: {
    UserBanner,
    UserAlbumsAlt,
    UserSongsAlt,
    Tabs,
    Tab,
    Stream,
  },

  watch: {
    $route() {
      this.id = this.$route.params.id;
      this.loadCreator(0, 10);
    },
  },

  methods: {
    loadCreator(attemptNo, maxAttempts) {
      const userId = this.$route.params.id; //TODO: If profile -> currentuser.id | If other profile get user id from route

      if (attemptNo >= maxAttempts) throw 'Could not load user data on time';
      if (userId === null || userId === undefined)
        return setTimeout(() => {
          this.loadCreator(attemptNo + 1, maxAttempts);
        }, 500);

      this.$store.dispatch(FETCH_CREATOR, userId);
    },
  },
  computed: {
    ...mapGetters(['currentUser']),
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

.user-profile-container {
  background-color: $color-white;
  width: 80%;
  height: 100%;
  border-radius: 1.5rem;
  margin: 0 auto;
  box-shadow: 0 1rem 3rem rgba($color: #0000, $alpha: 0.1);

  @include respond(tablet-port) {
    width: 100%;
  }
}

.user-profile {
  padding-top: 10rem;
  padding-bottom: 2rem;
  overflow: hidden;
  height: 100vh;
  background-color: #eeeeee;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100%25' height='100%25' viewBox='0 0 800 800'%3E%3Cg fill-opacity='0.07'%3E%3Ccircle fill='%23eeeeee' cx='400' cy='400' r='600'/%3E%3Ccircle fill='%23c6bbca' cx='400' cy='400' r='500'/%3E%3Ccircle fill='%239e89a8' cx='400' cy='400' r='400'/%3E%3Ccircle fill='%23785a86' cx='400' cy='400' r='300'/%3E%3Ccircle fill='%23522e65' cx='400' cy='400' r='200'/%3E%3Ccircle fill='%232c0046' cx='400' cy='400' r='100'/%3E%3C/g%3E%3C/svg%3E");
  background-attachment: fixed;
  background-size: cover;

  &__header {
    background-image: linear-gradient(-137deg, $color-tertiary 0, $color-primary 100%);
    width: 100%;
    border-top-left-radius: 1.5rem;
    border-top-right-radius: 1.5rem;
    padding: 3rem 5rem;
    display: flex;
    align-items: center;
  }

  &__content {
    height: 72%;
    padding: 0 5rem;

    &__tabs {
      &--album {
        display: flex;
      }
    }
  }
}

#UserProfile {
  padding-top: 15rem;
  .profile-content {
    display: flex;
  }
}
</style>
