<template>
  <nav class="navbar" :class="{ change_color: (scrollPosition > 50 || this.$route.name !== 'home') && !burgerMenuOpened }">
    <div class="navbar__container">
      <router-link class="navbar__logo-box" :to="{ name: 'home' }">
        <span class="logo logo__text">
          InKey
        </span>
        <img src="../assets/images/logo.png" alt="" class="logo logo__image" />
      </router-link>
      <ul v-if="!isAuthenticated" class="navbar__menu">
        <li class="navbar__menu__item">
          <a class="navbar__menu__link" active-class="active" href="http://inkeyusers.surge.sh/">
            Users App
          </a>
        </li>
        <li class="navbar__menu__item">
          <router-link class="navbar__menu__link navbar__button" active-class="active" exact :to="{ name: 'login' }">
            Sign in
          </router-link>
        </li>
        <li class="navbar__menu__item">
          <router-link class="navbar__menu__link navbar__button" active-class="active" exact :to="{ name: 'register' }">
            Sign up
          </router-link>
        </li>
      </ul>
      <div v-else class="navbar__menu-wrapper">
        <div class="navbar__username">
          <div class="navbar__username__icon">
            <img src="../assets/images/user.png" alt="" />
          </div>
          <router-link class="navbar__username__link" active-class="active" exact :to="{ name: 'profile', params: { id: currentUser.id } }">
            {{ currentUser.username }}
          </router-link>
        </div>
        <div class="navbar__burger-menu">
          <input type="checkbox" class="navbar__burger-menu__checkbox" id="nav-toggle" v-model="burgerMenuOpened" />
          <label for="nav-toggle" class="navbar__burger-menu__button">
            <span class="navbar__burger-menu__icon">&nbsp;</span>
          </label>
          <div class="navbar__burger-menu__background">&nbsp;</div>
          <div class="navbar__burger-menu__nav" v-if="burgerMenuOpened">
            <ul class="navbar__burger-menu__list">
              <li class="navbar__burger-menu__item">
                <a class="navbar__burger-menu__link" active-class="active" href="http://inkeyusers.surge.sh/">Users App</a>
              </li>
              <li class="navbar__burger-menu__item">
                <router-link
                  class="navbar__burger-menu__link"
                  active-class="active"
                  exact
                  @click.native="closeMenu()"
                  :to="{ name: 'profile', params: { id: currentUser.id } }"
                  >Profile
                </router-link>
              </li>
              <li class="navbar__burger-menu__item">
                <a
                  href="#"
                  @click="
                    logout();
                    closeMenu();
                  "
                  class="navbar__burger-menu__link"
                  >Logout</a
                >
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';
import { LOGOUT } from '@/store/actions.type';

export default {
  name: 'Header',

  data() {
    return {
      scrollPosition: null,
      burgerMenuOpened: false,
    };
  },

  mounted() {
    window.addEventListener('scroll', this.updateScroll);
  },

  computed: {
    ...mapGetters(['currentUser', 'isAuthenticated']),
  },

  methods: {
    logout() {
      this.$store.dispatch(LOGOUT).then(() => {
        this.$router.push({ name: 'login' }).catch(() => {});
      });
    },
    updateScroll() {
      this.scrollPosition = window.scrollY;
    },
    closeMenu() {
      this.burgerMenuOpened = false;
    },
  },
};
</script>
<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_mixins.scss';

.navbar {
  position: fixed;
  width: 100%;
  padding: 3.2rem 0;
  z-index: 100;
  transition: all 0.5s;

  &__container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 90%;
    margin: auto;

    @include respond(tablet-port) {
      width: 80%;
    }
  }

  &__logo-box {
    text-decoration: none;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  &__menu {
    font-size: 1.5rem;
    font-weight: 500;
    display: flex;
    justify-content: space-between;
    align-items: center;
    list-style-type: none;
    width: 32rem;

    &__item {
      text-transform: uppercase;
    }

    &__link {
      color: $color-white;
      letter-spacing: 0.15rem;
      text-decoration: none;
      transition: all 0.1s;
      display: block;

      &:hover {
        color: $color-primary;
      }
    }
  }

  &__button {
    border: 2px solid $color-white;
    padding: 0.8rem 1.6rem;
    border-radius: 6.4rem;
    transition: all 0.1s;

    &:hover {
      border-color: $color-primary;
      transform: translateY(-1px);
    }
    &:active {
      filter: brightness(80%);
      transform: translateY(1px);
    }
  }

  &__menu-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  &__username {
    cursor: pointer;
    min-width: 13rem;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba($color: $color-white, $alpha: 0.04);
    padding: 1.1rem 1.5rem;
    margin-right: 1rem;
    border-radius: 2.5rem;
    transition: all 0.2s;

    &__icon {
      width: 2rem;
      margin-right: 0.5rem;

      & > * {
        width: 100%;
      }
    }

    &__link {
      font-size: 1.7rem;
      font-family: inherit;
      font-weight: 500;
      text-decoration: none;
      color: $color-white;
    }

    &:hover,
    &:active {
      background-color: rgba($color: $color-white, $alpha: 0.1);
    }
  }

  &__burger-menu {
    position: relative;
    top: -1.5rem;

    &__checkbox {
      display: none;
    }

    &__button {
      cursor: pointer;
      background-color: transparent;
      height: 5rem;
      width: 5rem;
      border-radius: 50%;
      border: 2px solid $color-white;
      position: absolute;
      top: -1rem;
      z-index: 200;
      box-shadow: 0 1rem 3rem rgba($color: #000000, $alpha: 0.1);
      text-align: center;
      transition: all 0.2s;

      &:hover,
      &:active {
        background-color: $color-secondary;
        border: 2px solid $color-secondary;
      }
    }

    &__background {
      height: 5rem;
      width: 5rem;
      border-radius: 50%;
      background-image: radial-gradient($color-primary, $color-tertiary);
      position: absolute;
      z-index: 150;
      top: -1rem;
      opacity: 0;
      transition: transform 0.5s cubic-bezier(0.86, 0, 0.07, 1);
    }

    &__nav {
      height: 100vh;
      position: fixed;
      top: 0;
      left: 0;
      z-index: 199;
      width: 0;
      opacity: 0;
      transition: all 0.3s;
    }

    &__list {
      position: absolute;
      top: 40%;
      left: 50%;
      transform: translate(-50%, -50%);
      list-style: none;
      text-align: center;
    }

    &__item {
      margin: 2rem;
    }

    &__link {
      font-size: 3rem;
      font-family: inherit;
      font-weight: 500;
      text-decoration: none;
      color: $color-white;
      text-transform: uppercase;
      transition: all 0.2s;

      &:hover,
      &:active {
        color: darken($color-primary, 0);
        box-shadow: 0 3.2rem 8rem 0 rgba(185, 0, 103, 0.27);
      }
    }

    &__checkbox:checked ~ &__background {
      opacity: 1;
      transform: scale(120);
    }

    &__checkbox:checked ~ &__nav {
      width: 100%;
      opacity: 1;
    }

    &__icon {
      position: relative;
      margin-top: 2.2rem;

      &,
      &::before,
      &::after {
        width: 2.4rem;
        height: 2px;
        background-color: $color-white;
        display: inline-block;
      }
      &::before,
      &::after {
        content: '';
        position: absolute;
        left: 0;
        transition: all 0.3s;
      }

      &::before {
        top: -0.8rem;
      }

      &::after {
        top: 0.8rem;
      }
    }

    &__checkbox:checked + &__button &__icon {
      background-color: transparent;
    }
    &__checkbox:checked + &__button &__icon::before {
      top: 0;
      transform: rotate(45deg);
    }
    &__checkbox:checked + &__button &__icon::after {
      top: 0;
      transform: rotate(-45deg);
    }
  }
}

.logo {
  &__text {
    font-size: 2.7rem;
    font-family: inherit;
    line-height: 0;
    color: $color-white;
    margin-right: 0.8rem;
  }
  &__image {
    height: 3.2rem;
  }
}

.change_color {
  background-color: $color-tertiary;
  opacity: 0.98;
  padding: 1.3rem 0;
  box-shadow: 0 3px 10px -5px $color-tertiary;
  transition: all 0.5s;
}
</style>
