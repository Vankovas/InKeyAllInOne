<template>
<div>
    <div class="playlist-details-loading" v-if="loading">
      <Loading />
    </div>
  <div class="playlist-details" v-else>
      <div class="playlist-details__header">
        <div class="playlist-details__header__wrapper">
            <div class="playlist-details__header__info">
                <div class="playlist-details__header__info__play">
                  <button type="button" @click="playAllSongs"><font-awesome-icon icon="play"/></button>
                  <h1>{{selectedPlaylist.name}}</h1>
                </div>
                <div class="playlist-details__header__info__subheadings">
                  <h3>By {{selectedPlaylist.user_name}}</h3>
                  <h3>{{selectedPlaylist.description}}</h3> 
                </div>
            </div>
        </div>
      </div>
      <div v-if="selectedPlaylist.songs">
        <div class="playlist-details__playlist" v-if="selectedPlaylist.songs.length > 0">
          <div v-for="(track, index) in selectedPlaylist.songs" :key="track.id">
              <TrackBox :id="track.id" :index="index+1" :name="track.name" :artist="track.artist" 
              :duration="track.duration" :rating="track.rating" :data="track.data">
                <div v-if="selectedPlaylist.user == currentUser.id">
                  <button type="button" class="playlist-details__playlist__remove-btn" @click="removeTrackFromPlaylist(track.id)"><font-awesome-icon icon="times"/></button>
                </div>
              </TrackBox>
          </div>
        </div>
        <div v-else class="playlist-details__playlist-alt">
          <h1>There are no tracks in this playlist.</h1>
        </div>    
      </div>
      <div v-else>
        <h1>There are no tracks in this playlist.</h1>
      </div>    
  </div>
</div>

</template>

<script>
import TrackBox from '../components/TrackBox'
import numeral from 'numeral'
import { mapGetters } from 'vuex'
import { FETCH_PLAYLIST, DELETE_SONG_PLAYLIST } from '../store/actions.type'
import Loading from '../components/Loading'
import { EventBus } from '../common/event-bus'

export default {
    data() {
        return {
          id: this.$route.params.id,
          loading: false,
        }
    },
    mounted() {
      this.fetchData();
    },
    computed: {
      ...mapGetters(['selectedPlaylist', 'currentUser']),
    },
    filters: {
        formatNumber: function (value) {
            return numeral(value).format("0,0");
        }
    },
    watch: {
        '$route' (to) {
            if(to.name == 'playlist') {
                this.id = this.$route.params.id;
                this.fetchData();
            }
        } 
    },
    methods: {
      playAllSongs() {
        EventBus.$emit("set-songs", this.selectedPlaylist.songs, true);
      },
      async fetchData() {
            this.loading = true;
            await this.$store.dispatch(FETCH_PLAYLIST, this.id);
            this.loading = false;
      },
      async removeTrackFromPlaylist(trackId) {
            await this.$store.dispatch(DELETE_SONG_PLAYLIST, { id: this.id, songs: [trackId]});
            this.fetchData();
      },

    },

    components: {
        TrackBox,
        Loading,
    }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.playlist-details-loading {
  position: absolute;
  top: 40%;
  left: 50%;
}

.playlist-details{
    &__header {
        background-image: linear-gradient($color-primary-3, $color-primary-2);
        margin: -2rem -5rem 0 -5rem;
        padding: 0 5rem;
        display: flex;
        justify-content: flex-end;
        flex-direction: column;
        height: 30rem;

        &__wrapper {
          display: inline-flex;
          padding-bottom: 1rem;
        }

        &__info {

          &__play {
            display: flex;
            align-items: center;

            & > button {
              cursor: pointer;
              background-color: transparent;
              border: none;
              outline: none;
              margin-right: 2rem;
              margin-bottom: 1rem;
              transition: all .1s ease-in;

              &:hover, &:active {
                transform: scale(1.2);
              }

              & > * {
                font-size: 5rem;
                color: $color-secondary;
              }
            }
          }

            h1 {
                font-size: 8rem;
            }

          &__subheadings {
            display: flex;
            align-items: center;

            & > *:first-child {
              font-size: 2rem;
              margin-right: 2rem;
            }

            & > *:last-child {
              font-size: 1.5rem;
              color: #cccccc;
            }
          }
        }
    }

    &__playlist {
        margin-top: 2rem;
        & > * {
            & > * {
                border-bottom: 2px solid $color-primary-2;
            }
        }

    &__remove-btn {
        cursor: pointer;
        margin-right: 1.5rem;
        margin-left: 1rem;
        width: 3rem;
        height: 3rem;
        border: none;
        outline: none;
        border-radius: .3rem;
        background-color: $color-primary-2;
        transition: all .2s ease-in;

        &:hover, &:active {
            background-color: $color-secondary;
        }

        & > * {
            color: $color-primary-3;
            font-size: 1.8rem;
        }
    }
    }

    &__playlist-alt {
      margin-top: 2rem;

      & > h1 {
        font-size: 2.6rem;
        color: #cccccc;
      }
    }
}
</style>