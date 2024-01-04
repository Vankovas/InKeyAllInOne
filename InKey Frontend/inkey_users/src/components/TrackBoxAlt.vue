<template>
<div>
    <div class="track-box-alt" @mouseleave="hide">
        <h2 class="track-box-alt__index" v-if="!isPlaying"> {{ index | twoDigits }}</h2>
        <h2 class="track-box-alt__index" v-else><font-awesome-icon icon="stop-circle"/></h2>
        <div class="track-box-alt__track" @click="play()">
            <h3>{{name}}</h3>
            <h4>{{artist}}</h4>
        </div>
        <div class="track-box-alt__more">
            <div class="track-box-alt__more__duration">
                <h3>{{duration}}</h3>
            </div>
            <star-rating v-model="ratingData"
                v-if="isAuthenticated"
                :star-size="15"
                :show-rating="false"
                active-color="#ffc300"
                inactive-color="#4f4f4f"
                :border-width="1"
                border-color="#330d28"
                @rating-selected ="setRating"
                :glow="2"
                glow-color="#ffc300"
            ></star-rating>
            <slot></slot>
            <div class="track-box-alt__more__settings">
                <button type="button" class="track-box-alt__more__settings__btn" @click="showSettings = !showSettings"><font-awesome-icon icon="ellipsis-h"/></button>
            </div>
            <div class="track-box-alt__more__options-list" v-if="showSettings" v-click-outside="hide">
                <ul>
                    <li :class="{disabled : !isAuthenticated}" @click="addToFavourites"><a><font-awesome-icon icon="heart"/> Add To Favourites</a></li>
                    <li @click="addToQueue"><a><font-awesome-icon icon="plus-square"/> Add To Queue</a></li>
                    <li :class="{disabled : !isAuthenticated}" @click="showPlaylistModal = true"><a><font-awesome-icon icon="plus"/> Add To Playlist</a></li>
                </ul>
            </div>
            
        </div>
    </div>

      <div v-if="showPlaylistModal" class="modal">
        <div v-if="loading" class="modal__loading">
          <Loading/>
        </div>
        <div class="modal__content" v-else>
          <div class="modal__form" v-if="userPlaylists.length > 0">
            <div class="modal__form__header">
              <h1>Select Playlist</h1>
            </div>
            <form @submit.prevent="addToPlaylist" class="form" >
              <div class="form__form-group">
                <label for="selectPlaylist">Playlist:</label>
                <select name="selectPlaylist" class="input-primary" v-model="selectedPlaylist" >                    
                    <option  v-for="playlist in userPlaylists" :key="playlist.id" :value="playlist.id"> {{playlist.name}} </option>
                </select>
              </div>
              <button class="form__btn btn-primary">
                Add
              </button>
            </form>
          </div>
            <div v-else>
                <h1 style="font-size: 1.6rem; text-align: center;">Currently you don't have any playlists to add this song to. Go to <router-link to="/create_playlists" style="color:#ffc300">Create Playlists</router-link> to create a new one.</h1>
            </div>
          <div class="modal__close">
            <button type="btn" @click="showPlaylistModal = false">
              <font-awesome-icon icon="times" /></button>
          </div>
        </div>
      </div>
</div>

</template>

<script>
import StarRating from 'vue-star-rating'
import { ADD_REMOVE_USER_FAVOURITE_SONG, SEND_VOTE, ADD_SONG_PLAYLIST} from '../store/actions.type'; //
import { mapGetters } from 'vuex'
import Loading from '../components/Loading'
import { EventBus } from '../common/event-bus'


export default {
    props: ['id', 'index', 'name', 'artist', 'duration', 'rating', 'data'],

    data() {
        return {
            showSettings: false,
            isPlaying: false,
            ratingData: this.rating,
            showPlaylistModal: false,
            selectedPlaylist: null,
            loading: false,
        }
    },
    computed: {
      ...mapGetters(['userPlaylists', 'isAuthenticated']),
    },
    methods: {
        hide() {
            this.showSettings = false;
        },
        setRating() {
            if(this.isAuthenticated) {
                this.$store.dispatch(SEND_VOTE, { id: this.$props.id, rating: this.ratingData });
            } else {
                console.log("DISPLAY AN ERROR");
            }     
        },
        addToFavourites() {
            this.$store.dispatch(ADD_REMOVE_USER_FAVOURITE_SONG, this.$props.id);
            this.$router.push({ name: 'favourites' });
        },
        async addToPlaylist() {
            if(this.selectedPlaylist) {
                this.loading = true;
                await this.$store.dispatch(ADD_SONG_PLAYLIST, { id: this.selectedPlaylist, songs: [this.$props.id]});
                this.loading = false;
                this.showPlaylistModal = false;
                this.$toasted.show("The song was added to the playlist!");
                //SUCCESS MESSAGE
            }
        },
        play(){
          if(!this.isPlaying){
            EventBus.$emit("set-to-not-playing");
            let song = {
              name: this.name,
              artist: this.artist,
              data: this.data,
              singleTime: true
            }
            this.isPlaying = true;
            EventBus.$emit("add-song", song, true);
          }else{
            this.isPlaying = false;
            EventBus.$emit("remove-song");
          }
        },
        addToQueue(){
            let song = {
              id: this.id,
              name: this.name,
              artist: this.artist,
              data: this.data,
              duration: this.duration,
              rating: this.rating,
            }
            EventBus.$emit("add-song", song);
            this.$toasted.show("The song has been added to your queue!");
        }
    },
    mounted(){
      EventBus.$on("set-to-not-playing", ()=>{
        this.isPlaying = false;
      });
    },

    filters: {
        twoDigits: function (value) {
            if (!value) return ''
            value = value.toString()
            if (value.length < 2) {
                value = ['0', value.slice(0)].join('');
            }
            return value;
        }
    },
    watch: {
        '$route' () {
            this.showPlaylistModal = false;
        } 
    },
    directives: {
        clickOutside: {
            bind: function (el, binding, vnode) {
                    el.clickOutsideEvent = function (event) {
                    // here I check that click was outside the el and his children
                    if (!(el == event.target || el.contains(event.target))) {
                        if(event.target.className != "track-box-alt__more__settings__btn" && event.target.localName != "svg" && event.target.tagName != "path"){
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
        Loading
    }
} 
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.track-box-alt {
    cursor: default;
    display: flex;
    align-items: center;
    min-width: 50rem;
    height: 5rem;
    width: 100%;
    position: relative;
    transition: all .1s ease-in;
    border-bottom: 1px solid $color-primary-2;

    &:hover &__track > h3{
        color: $color-secondary;
    }
    &:hover &__index {
        color: $color-secondary;
    }

    &__index {
        font-size: 2.3rem;
        font-weight: 500;
        margin-right: 2rem;
        transition: all .2s ease-in;
    }

    &__track {
        display: flex;
        align-items: center;
        margin-right: auto;

        & > h3 {
            cursor: pointer;
            font-size: 2rem;
            transition: all .2s ease-in;
        }

        & > h4 {
            margin-left: 1rem;
            font-size: 1.6rem;
            color: #bbbbbb;
        }
    }

    &__more {
        display: flex;
        align-items: center;
        position: relative;

        &__duration {
            margin-right: 2rem;

            & > * {
                font-size: 2rem;
            }
        }
        &__settings {
            &__btn {
                cursor: pointer;
                color: $color-white;
                background-color: transparent;
                padding: .5rem;
                outline: none;
                border: none;
                font-size: 2.5rem;
            }
        }

        &__options-list {
            background-color: $color-gray-light-1;
            padding: .5rem;
            border-radius: 1rem;
            position: absolute;
            top: -3.1rem;
            right: 4rem;
            width: 18rem;
            z-index: 20;

            &::after {
                content: '';
                position: absolute;
                top: 39%;
                right: -.5rem;
                width: 0; 
                height: 0; 
                border-top: 5px solid transparent;
                border-bottom: 5px solid transparent;
                border-left: 5px solid $color-gray-light-1;
            }

            &>ul {
                & > li {
                    cursor: pointer;
                    list-style: none;
                    transition: all .1s ease-in;
                    padding: .5rem 1rem;
                    border-radius: 1rem;

                    & > a {
                        font-size: 1.5rem;
                        font-weight: 400;
                        color: $color-primary-1;

                        & > * {
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
}


.modal {
  position: fixed;
  z-index: 1000;
  padding-top: 100px;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);

  &__loading {
    position: absolute;
    left: 50%;
    top: 40%;
    transform: translate(-50%, -50%);
  }

  &__content {
    position: absolute;
    background-color: darken($color: $color-primary-3, $amount: 7);
    left: 50%;
    top: 40%;
    transform: translate(-50%, -50%);
    border-radius: .2rem;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    padding: 5rem;
    display: flex;
    justify-content: center;
    max-width: 50rem;
  }

  &__form {
    min-width: 35rem;

    &__header>* {
      font-size: 4rem;
      text-align: center;
    }
  }

  &__close {
    position: absolute;
    top: 1rem;
    right: 1.5rem;

    &>button {
      cursor: pointer;
      outline: none;
      border: none;
      background-color: transparent;

      &>* {
        font-size: 2.3rem;
        color: $color-white;

        &:hover {
          color: $color-primary-1;
        }
      }
    }
  }
}

.form {
  margin-top: 2rem;

  &__form-group {
    margin-bottom: 2rem;

    &>label {
      font-size: 2.2rem;
      font-family: inherit;
      font-weight: 500;
    }
  }

  &__btn {
    padding: 1rem 3rem;
    font-size: 1.8rem;
    font-weight: 500;
    width: 100%;
    margin-top: 2rem;
  }

  &__footer {
    font-size: 1.6rem;
    text-align: center;

    &>span {
      margin-right: .5rem;
    }

    &>a {
      cursor: pointer;
      font-size: 1.7rem;
      font-family: inherit;
      font-weight: 500;
      transition: all .2s;

      &:hover {
        text-decoration: underline;
        color: $color-primary-1;
      }
    }
  }
}

.disabled {
  pointer-events:none; 
  opacity:0.6; 
}
</style>