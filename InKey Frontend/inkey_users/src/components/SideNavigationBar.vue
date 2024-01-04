<template>
  <div class="side-navigation">
      <div class="side-navigation__logo-box">
        <span class="side-navigation__logo-box__text">InKey</span>
        <img src="../assets/images/logo.png" alt="" class="side-navigation__logo-box__image">
      </div>
      <nav class="side-navigation__items">
        <ul>
          <li :class="{ 'active': activeIndex === 1 }" @click="setActive(1)"><router-link to="/" ><font-awesome-icon icon="home" class="side-navigation__items__icon" /><span class="side-navigation__items__text">Home</span></router-link></li> 
          <li :class="{ 'active': activeIndex === 2 }" @click="setActive(2)"><router-link to="/albums"><font-awesome-icon icon="compact-disc" class="side-navigation__items__icon" /><span class="side-navigation__items__text">Albums</span></router-link></li>
          <li :class="{ 'active': activeIndex === 3 }" @click="setActive(3)" v-if="isAuthenticated"><router-link to="/favourites"><font-awesome-icon icon="heart" class="side-navigation__items__icon" /><span class="side-navigation__items__text">Favourites</span></router-link></li>
          <li :class="{ 'active': activeIndex === 4 }" @click="setActive(4)"><router-link to="/live"><font-awesome-icon icon="broadcast-tower" class="side-navigation__items__icon" /><span class="side-navigation__items__text">Live</span></router-link></li>
          <li :class="{ 'active': activeIndex === 5 }" @click="setActive(5)"><router-link to="/playlists" ><font-awesome-icon icon="list" class="side-navigation__items__icon" /><span class="side-navigation__items__text"> Playlists</span></router-link></li>
          <li :class="{ 'active': activeIndex === 6 }" @click="setActive(6)" v-if="isAuthenticated"><router-link to="/create_playlists"><font-awesome-icon icon="list-alt" class="side-navigation__items__icon" /><span class="side-navigation__items__text">Create Playlist</span></router-link></li>
        </ul>
      </nav>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      activeIndex: 1,
    }
  },
  mounted() {
    this.setMenu();
  },
    computed: {
        ...mapGetters(['isAuthenticated']),
    },
    watch: {
        '$route' () {
            this.setMenu();
        } 
    },
  methods: {
    setActive(index) {
      if(index === 3 && !this.isAuthenticated || index === 6 && !this.isAuthenticated) {
        // NOTIFY USER TO BE LOGGED IN.
        
        this.activeIndex = 1;
        return;
      }
      this.activeIndex = index;
    },
    setMenu() {
      let routerPath = window.location.pathname;
      switch(routerPath) {
        case "/": 
          this.activeIndex = 1;
          break;
        case "/albums": 
          this.activeIndex = 2;
          break;
        case "/favourites": 
          this.activeIndex = 3;
          break;
        case "/live": 
          this.activeIndex = 4;
          break;
        case "/playlists": 
          this.activeIndex = 5;
          break;
        case "/create_playlists": 
          this.activeIndex = 6;
          break;
        default: 
          this.activeIndex = 1;
          break;
      }
    }

  }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_mixins.scss";

.side-navigation {
  background-color: $color-primary-2;
  width: 22rem;
  height: 100vh;
  position: fixed;
  z-index: 501;
  box-shadow: 0px 0px 24px 6px rgba(black, 0.25);

  @include respond(tablet-port) {
      width: 6rem;
  }

  &__logo-box {
    text-decoration: none;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 9rem;
          @include respond(tablet-port) {
              display: none;
          }
    &__text {
      font-size: 3.3rem;
      font-family: inherit;
      line-height: 0;
      color: $color-white;
      text-shadow: 0 0 2rem rgba($color-white, .9);
      margin-right: .8rem;
    }

    &__image {
      height: 3.5rem;
    }
  }
 
  &__items {
    font-size: 1.7rem;
    margin-top: 7rem;

    & > ul {
      & > li {
        cursor: pointer;
        list-style: none;
        transition: all .1s;
        
        & > * {
          text-decoration: none;
          color: white;
          padding: 1rem 2rem;
          display: flex;
          align-items: center;

          @include respond(tablet-port) {
            & > span {
              display: none;
            }
          }
        }

        &:hover {
          background-color: $color-primary-3;
        }
      }

      & > li:nth-child(4) {
        margin-bottom: 3rem;
      }
    }

    &__icon {
      font-size: 2rem;
      width: 2rem;
      color: $color-gray-light-1;

      @include respond(tablet-port) {
        font-size: 5rem;
      }
    }

    &__text {
      margin-left: 2rem;
    }
  }
}
.active {
  background-color: $color-primary-3;
}
</style>
