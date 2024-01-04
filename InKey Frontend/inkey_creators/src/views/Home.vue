<template>
  <div class="wrapper">
    <section class="section-hero">
      <div class="section-hero__container">
        <div class="section-hero__container--left">
          <h1 class="section-hero__heading">InKey.</h1>
          <h1 class="section-hero__heading">For creators.</h1>
          <h2 class="section-hero__subheading">Upload a track and reach your future fans.</h2>
          <button class="section-hero__cta-btn" @click="uploadHandler">Upload</button>
        </div>
        <div class="section-hero__container--right">
          <div class="section-hero__bubbles">
            <div class="section-hero__bubbles__small-circle">&nbsp;</div>
            <div class="section-hero__bubbles__large-circle">&nbsp;</div>
            <div class="section-hero__bubbles__image-circle">
              <img src="../assets/images/hero-image.jpg" alt="hero-image" class="section-hero__bubbles__image-circle__img" />
            </div>
            <div class="section-hero__bubbles__smallest-circle">&nbsp;</div>
          </div>
        </div>
      </div>
    </section>
    <section class="section-creators">
      <div class="section-creators__container">
        <CreatorsCarousel />
      </div>
    </section>
    <section class="section-features">
      <div class="section-features__container">
        <div class="section-features__feature section-features__feature--left">
          <div class="section-features__feature__card" data-aos="fade-right" data-aos-duration="1000">
            <div class="section-features__feature__text-content">
              <div class="section-features__feature__text-content__heading">
                <h2>Upload your voice, tracks or sound on your own webpage.</h2>
              </div>
              <hr />
              <div class="section-features__feature__text-content__text">
                <p>
                  You can record yourself or upload pre-recorded tracks and sounds. Customize your profile and express yourself in your very own music platform. 
                </p>
              </div>
            </div>
            <div class="section-features__feature__image-content">
              <img class="section-features__feature__image-content__image" src="../assets/images/upload-music.png" alt="music-upload" />
            </div>
          </div>
        </div>
        <div class="section-features__feature section-features__feature--right">
          <div class="section-features__feature__card" data-aos="fade-left" data-aos-duration="1000">
            <div class="section-features__feature__image-content">
              <img class="section-features__feature__image-content__image" src="../assets/images/stream-music.png" alt="music-upload" />
            </div>
            <div class="section-features__feature__text-content">
              <div class="section-features__feature__text-content__heading">
                <h2>Broadcast live audio and notify your fans.</h2>
              </div>
              <hr />
              <div class="section-features__feature__text-content__text">
                <p>Start live audio streams in front of all your fans. Here you can make grand concerts from your home.  </p>
              </div>
            </div>
          </div>
        </div>
        <div class="section-features__feature section-features__feature--left">
          <div class="section-features__feature__card" data-aos="fade-right" data-aos-duration="1000">
            <div class="section-features__feature__text-content">
              <div class="section-features__feature__text-content__heading">
                <h2>Chat with your listeners and see how many are listening live.</h2>
              </div>
              <hr />
              <div class="section-features__feature__text-content__text">
                <p>
                  You are always in contact with your fans. During your streams, you can all chat together and share the experience.
                </p>
              </div>
            </div>
            <div class="section-features__feature__image-content">
              <img class="section-features__feature__image-content__image" src="../assets/images/live-chat.png" alt="music-upload" />
            </div>
          </div>
        </div>
        <div class="section-features__bubble section-features__bubble-1">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-2">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-3">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-4">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-5">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-6">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-7">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-8">&nbsp;</div>
        <div class="section-features__bubble section-features__bubble-9">&nbsp;</div>
      </div>
    </section>
    <footer class="footer">
      <div class="footer__logo">
        <span class="footer__logo__text">
          InKey
        </span>
        <img src="../assets/images/logo.png" alt="" class="footer__logo__image" />
      </div>
      <p class="footer__copyright">Copyright &copy; by InKey team. All rights reserved.</p>
    </footer>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';
import CreatorsCarousel from '../components/CreatorsCarousel.vue';

export default {
  methods: {
    uploadHandler() {
      this.$router.push({ name: 'profile', params: { id: this.currentUser.id } }).catch(() => {});
    },
  },

  components: {
    CreatorsCarousel,
  },
  computed: {
    ...mapGetters(['currentUser']),
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_animations.scss';
@import '../scss/_mixins.scss';

.wrapper {
  min-height: 100%;
  margin: 0 auto -10rem;
}

.section-hero {
  background-image: linear-gradient(-137deg, $color-tertiary 0, $color-primary 100%);
  height: 60vh;
  border-bottom-left-radius: 30% 10%;
  border-bottom-right-radius: 30% 10%;
  position: relative;

  &::after {
    content: '';
    background-color: $color-gray-light-1;
    width: 100%;
    height: 10vh;
    position: absolute;
    bottom: 0;
    z-index: -10;
  }

  &__container {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 65%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: space-between;

    &--left {
      flex: 1;
      @include respond(tablet-port) {
        font-size: 50% !important;
      }
    }

    &--right {
      flex: 1;
      @include respond(small-laptop) {
        display: none;
      }
    }
  }

  &__heading {
    color: $color-white;
    font-size: 8rem;
    line-height: 9.5rem;
    font-family: inherit;
    font-weight: 500;
  }

  &__subheading {
    color: $color-white;
    font-size: 3.2rem;
    margin-top: 3.2rem;
    font-family: inherit;
    font-weight: 500;
  }

  &__cta-btn {
    cursor: pointer;
    outline: none;
    white-space: nowrap;
    border: none;
    font-family: inherit;
    font-size: 2.1rem;
    font-weight: 500;
    letter-spacing: 0.15rem;
    height: 6.4rem;
    width: 16rem;
    border-radius: 6.4rem;
    background-color: $color-secondary;
    color: $color-white;
    margin-top: 3.2rem;
    transition: all 0.2s;

    &:hover {
      background-color: $color-white;
      color: $color-primary;
      transform: translateY(-2px);
      box-shadow: 0 1rem 3.2rem rgba(black, 0.4);
    }

    &:active {
      transform: translateY(2px);
      box-shadow: 0 1rem 1rem rgba(black, 0.1);
    }
  }

  &__bubbles {
    position: relative;

    &__small-circle {
      opacity: 0.6;
      background-image: linear-gradient(42deg, $color-primary 0, $color-tertiary 100%);
      box-shadow: 0 3.2rem 8rem 0 rgba(185, 0, 103, 0.27);
      width: 15rem;
      height: 15rem;
      border-radius: 50%;
      position: absolute;
      z-index: 6;
      top: 23rem;
      left: 42rem;
    }
    &__large-circle {
      background-image: linear-gradient(-199deg, $color-primary 0, $color-tertiary 100%);
      box-shadow: 0 3.2rem 8rem 0 rgba(185, 0, 103, 0.27);
      width: 32rem;
      height: 32rem;
      border-radius: 50%;
      position: absolute;
      z-index: 1;
      top: -4rem;
      left: 48rem;
    }
    &__image-circle {
      position: absolute;
      top: 1rem;
      left: 37rem;
      z-index: 5;
      animation: rotation 50s infinite linear;

      &__img {
        width: 43rem;
        clip-path: circle(40%);
      }
    }
    &__smallest-circle {
      opacity: 0.8;
      background-image: linear-gradient(100deg, $color-primary 0, $color-tertiary 100%);
      box-shadow: 0 3.2rem 8rem 0 rgba(185, 0, 103, 0.27);
      width: 7rem;
      height: 7rem;
      border-radius: 50%;
      position: absolute;
      z-index: 6;
      top: -3rem;
      left: 75rem;
    }
  }
}

.section-creators {
  background-color: $color-gray-light-1;
  height: 80rem;
  display: flex;
  justify-content: center;

  &__container {
    width: 80%;
    height: 80%;
    margin-top: 18rem;
    display: flex;
    justify-content: center;
  }
}
.section-features {
  &__container {
    width: 100%;
    position: relative;
  }

  &__feature {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 5rem 0 10rem 0;

    &__card {
      box-shadow: 0 1rem 3rem rgba($color: $color-tertiary, $alpha: 0.1);
      background-color: $color-white;
      margin-top: 10rem;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 0 8rem;
      border-radius: 2rem;
    }

    &--left {
      padding-right: 20rem;
    }

    &--right {
      padding-left: 20rem;
    }

    &__text-content {
      max-width: 70rem;

      &__heading {
        font-size: 3rem;

        @include respond(tablet-land) {
          font-size: 2rem;
        }
      }

      &__text {
        margin-top: 5rem;
        font-size: 2rem;
        font-weight: 500;
        line-height: 4rem;
        color: black;

        @include respond(tablet-land) {
          line-height: 3.5rem;
          margin-bottom: 1rem;
        }
      }
    }

    &__image-content {
      max-width: 70rem;

      &__image {
        width: 50rem;

        @include respond(tablet-land) {
          width: 30rem;
        }

        @include respond(tablet-port) {
          display: none;
        }
      }
    }
  }

  .section-features__bubble {
    border-radius: 50%;
    position: absolute;
    z-index: -1;

    &-1 {
      opacity: 0.9;
      background-image: linear-gradient(42deg, $color-primary 0, $color-tertiary 100%);
      width: 80rem;
      height: 80rem;
      top: -20rem;
      right: -60rem;
      z-index: 2;
    }

    &-2 {
      opacity: 0.75;
      background-image: linear-gradient(0deg, $color-primary 0, $color-tertiary 100%);
      width: 20rem;
      height: 20rem;
      top: 40rem;
      right: 5rem;
      z-index: 3;
    }

    &-3 {
      opacity: 0.8;
      background-image: linear-gradient(210deg, $color-primary 0, $color-tertiary 100%);
      width: 5rem;
      height: 5rem;
      top: -12rem;
      right: 15rem;
      z-index: 2;
    }

    &-4 {
      opacity: 0.8;
      background-image: linear-gradient(250deg, $color-primary 0, $color-tertiary 100%);
      width: 50rem;
      height: 50rem;
      top: 80rem;
      left: -30rem;
    }

    &-5 {
      opacity: 0.9;
      background-image: linear-gradient(250deg, $color-primary 0, $color-tertiary 100%);
      width: 15rem;
      height: 15rem;
      top: 60rem;
      left: 10rem;
    }

    &-6 {
      opacity: 0.8;
      background-image: linear-gradient(300deg, $color-primary 0, $color-tertiary 100%);
      width: 15rem;
      height: 15rem;
      top: 60rem;
      left: 10rem;
    }

    &-7 {
      opacity: 0.8;
      background-image: linear-gradient(360deg, $color-primary 0, $color-tertiary 100%);
      width: 35rem;
      height: 35rem;
      bottom: -35rem;
      right: -5rem;
    }

    &-8 {
      opacity: 0.9;
      background-image: linear-gradient(180deg, $color-primary 0, $color-tertiary 100%);
      width: 10rem;
      height: 10rem;
      bottom: 15rem;
      right: 5rem;
    }

    &-9 {
      opacity: 0.7;
      background-image: linear-gradient(60deg, $color-primary 0, $color-tertiary 100%);
      width: 5rem;
      height: 5rem;
      bottom: 5rem;
      right: 25rem;
    }
  }

  hr {
    margin: 1.5rem 0 3.5rem 0;
  }
}
.footer {
  margin-top: 20rem;
  padding: 5rem 0;
  height: 100%;
  background-color: darken($color: $color-tertiary, $amount: 5);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 7;
  min-height: calc(100vh - 1px);

  &__logo {
    display: flex;
    align-items: center;
    padding-right: 10rem;
    border-right: 1px solid $color-white;

    &__text {
      color: $color-white;
      font-size: 4rem;
      margin-right: 1rem;
    }

    &__image {
      width: 3.5rem;
      height: 3.5rem;
    }
  }

  &__copyright {
    color: $color-white;
    font-size: 1.6rem;
    padding-left: 10rem;
  }
}
</style>
