<template>
  <div class="artist-box">
      <div class="artist-box__cover">
          <div class="artist-box__cover__image" :style="coverImage ? { backgroundImage: 'url(' + coverImage + ')'} : { backgroundImage: 'url(' + 'https://portal.staralliance.com/cms/aux-pictures/prototype-images/avatar-default.png/@@images/image.png' + ')'}"></div>
          <div class="artist-box__overlay">
              <slot></slot>
              <div class="artist-box__overlay__highlight"></div>
              <button class="artist-box__overlay__more-btn btn-secondary" type="button" @click="routeToArtistDetails"><font-awesome-icon icon="eye"/></button>
          </div>
      </div>
      <h3 class="artist-box__name" @click="routeToArtistDetails">{{name}}</h3>
  </div>
</template>

<script>
export default {
    props: ['id', 'name', 'coverImage',],

    data() {
        return {
        }
    },

    methods: {
        routeToArtistDetails() {
            const artistId = this.$props.id;
            this.$router.push({ name: 'artist', params: { id: artistId } })
        }
    },
} 
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.artist-box {
    width: 100%;
    display: inline-block;
    margin-top: 2rem;

    &__cover {
        position: relative;
        min-width: 25rem;

        &__image {
            width: 30rem;
            height: 30rem;
            background-size: cover;
            background-clip: padding-box;
            background-position: center center;
            border-radius: 50%;
        }
    }

    &:hover &__overlay__more-btn {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }

    &:hover &__name{
        color: $color-secondary;
    }

    &:hover &__overlay__highlight {
        opacity: 1;
        background-image: -webkit-linear-gradient(90deg, $color-gray-dark-1 0%, $color-primary-1 0%, $color-secondary 0%, rgba($color-secondary, 0) 100%);
    }

    &__overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 30rem;
        height: 100%;

        &__highlight {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            opacity: 0;
            transition: all .2s ease-in;
        }

        &__more-btn {
            cursor: pointer;
            font-size: 2rem;
            font-weight: 400;
            padding: 1rem;
            border: 2px solid $color-white;
            border-radius: 50%;
            box-shadow: 0 0 2rem rgba($color: $color-white, $alpha: .2);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(3);
            transition: all .2s ease-in;
            opacity: 0;

            &:hover {
                box-shadow: 0 0 2rem rgba($color: $color-white, $alpha: .8);
                background-color: $color-white;
            }

            & > * {
                display: flex;
                align-items: center;
                justify-content: center;
            }
        }
    }

    &__name {
        cursor: pointer;
        font-size: 2rem;
        margin-top: 2rem;
        margin-right: 7rem;
        text-align: center;
    }
}

</style>