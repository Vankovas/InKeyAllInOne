<template>
  <div class="album-box" @mouseleave="hide">
      <div class="album-box__cover">
          <img :src="coverImage || 'https://vinylboutique.co.uk/wp-content/uploads/2017/05/default-release-cd.png'" alt="Cover Photo">
          <div class="album-box__overlay">
              <div class="album-box__overlay__highlight"></div>
              <button class="album-box__overlay__options-btn btn-secondary" type="button" @click="showSettings = !showSettings"><font-awesome-icon icon="ellipsis-h"/></button>
              <div class="album-box__overlay__options-list" v-if="showSettings" v-click-outside="hide">
                <ul>
                    <li @click="hide"><router-link :to="{ name: 'album', params: { id: id }}"><font-awesome-icon icon="angle-double-right"/>Open</router-link></li>
                    <li @click="hide(); addToFavourites()"><a><font-awesome-icon icon="heart"/>Add To Favourites</a></li>
                </ul>
              </div>
              <!-- Used for functionalities like remove album, etc. -->
              <slot></slot>
          </div>
      </div>
      <div class="album-box__info">
          <div class="album-box__info__title">
              <h3 @click="routeToAlbumDetails">{{name}}</h3>
          </div>
            <star-rating v-model="ratingData" v-if="isAuthenticated" :star-size="20" :show-rating="false"
          active-color="#ffc300" inactive-color="#4f4f4f" :border-width="1" border-color="#330d28"
          @rating-selected="setRating" :glow="2" glow-color="#ffc300"></star-rating>
          <div class="album-box__info__artist">
              <h3 @click="routeToArtistDetails">{{artist_name || artist_id}}</h3>
          </div>
      </div>
  </div>
</template>

<script>
import { ADD_REMOVE_USER_FAVOURITE_ALBUM } from '../store/actions.type';
import StarRating from 'vue-star-rating'
import { mapGetters } from 'vuex'
import { SEND_ALBUM_VOTE } from '../store/actions.type'; 

export default {
    props: ['id', 'name', 'artist_id', 'artist_name', 'coverImage', 'rating'],

    data() {
        return {
            showSettings: false,
            ratingData: this.rating,
        }
    },

    created() {
        this.hide();
    },
    computed: {
      ...mapGetters(['isAuthenticated']),
    },
    methods: {
        hide() {
            this.showSettings = false;
        },
        routeToAlbumDetails() {
            const albumId = this.$props.id;
            this.$router.push({ name: 'album', params: { id: albumId } })
        },
        routeToArtistDetails() {
            const artistId = this.$props.artist_id;
            this.$router.push({ name: 'artist', params: { id: artistId } })
        },
        addToFavourites() {
            this.$store.dispatch(ADD_REMOVE_USER_FAVOURITE_ALBUM, this.$props.id);
            this.$router.push({ name: 'favourites' });
        },

        setRating() {
            if(this.isAuthenticated) {
                this.$store.dispatch(SEND_ALBUM_VOTE, { id: this.$props.id, rating: this.ratingData });
            }  
        },
    },

    directives: {
        clickOutside: {
            bind: function (el, binding, vnode) {
                    el.clickOutsideEvent = function (event) {
                    // here I check that click was outside the el and his children
                    if (!(el == event.target || el.contains(event.target))) {
                        if(event.target.className != "album-box__overlay__options-btn btn-secondary" && event.target.localName !="svg" && event.target.tagName != "path"){
                            vnode.context[binding.expression](event);
                        }     
                    }
                    };
                    document.body.addEventListener('click', el.clickOutsideEvent)
            },
            unbind: function (el) {
                document.body.removeEventListener('click', el.clickOutsideEvent)
            },
        }
    },
    components: {
        StarRating,
    }
} 
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";
.album-box {

    width: 100%;
    display: inline-block;

    &__cover {
        position: relative;
        min-width: 25rem;

        &>img {
            width: 35rem;
            height: 35rem;
            border-radius: 1rem;
        }
    }

    &:hover &__overlay__options-btn {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }

    &:hover &__info__title {
        color: $color-secondary;
    }

    &:hover &__overlay__highlight {
        opacity: 1;
        background-image: -webkit-linear-gradient(90deg, $color-gray-dark-1 0%, $color-primary-1 0%, $color-secondary 0%, rgba($color-secondary, 0) 100%);
    }

    &__overlay {
        position: absolute;
        top: -.5rem;
        left: 0;
        width: 35rem;
        height: 100%;

        &__highlight {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 1rem;
            opacity: 0;
            transition: all .2s ease-in;
        }


        &__options-btn {
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


        &__options-list {
            background-color: $color-gray-light-1;
            padding: .5rem;
            border-radius: 1rem;
            position: absolute;
            top: 58%;
            left: 25%;
            width: 18rem;

            &::after {
                content: '';
                position: absolute;
                top: -.5rem;
                left: 46%;
                width: 0; 
                height: 0; 
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 5px solid $color-gray-light-1;
            }

            &>ul {
                &>li {
                    cursor: pointer;
                    list-style: none;
                    transition: all .1s ease-in;
                    border-radius: 1rem;

                    & > * {
                        font-size: 1.5rem;
                        font-weight: 400;
                        color: $color-primary-1;
                        text-decoration: none;
                        display: block;
                        padding: .5rem 1rem;

                        &>* {
                            margin-right: .5rem;
                        }
                    }

                    &:hover {
                        background-color: $color-primary-3;
                    }
                }
            }
        }
    }

    &__info {
        &__title {
            margin-top: 1rem;
            cursor: pointer;

            &>* {
                font-size: 1.8rem;
            }
        }

        &__artist {
            &>* {
                font-size: 1.6rem;
                color: #bbbbbb;
            }
            &:hover {
                cursor: pointer;
                text-decoration: underline;
            }
        }
    }
}

</style>