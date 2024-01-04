<template>
<div>
          <div class="album-details__loading" v-if="loading">
          <Loading/>
      </div>
  <div class="album-details" v-else>
      <div class="album-details__header" >
          <div class="album-details__header--left">
            <div class="album-details__header__cover-image" :style="{backgroundImage: 'url(' + selectedAlbum.cover_image + ')'}"></div>
            <div class="album-details__header__info">
                <h3><router-link to="/"> {{selectedAlbum.artist_name}} </router-link></h3>
                <h1>{{selectedAlbum.name }}</h1> 
                <h4>{{selectedAlbum.description}}</h4>
            </div>
          </div>
          <div class="album-details__header--right">
              <div class="album-details__header__views">
                  <h2>{{ selectedAlbum.views | formatNumber  }} <span> views</span></h2>
              </div>
          </div>
      </div>
      <div class="album-details__playlist">
        <div v-for="(track, index) in songsAlbum" :key="track.id">
            <TrackBoxAlt :id="track.id" :index="index+1" :name="track.name" :artist="track.artist" 
            :duration="track.duration" :rating="track.rating" :data="track.data"/>
        </div>
      </div>
  </div>
</div>

</template>

<script>
import TrackBoxAlt from '../components/TrackBoxAlt'
import Loading from '../components/Loading'
import numeral from 'numeral'
import { mapGetters } from 'vuex'
import { FETCH_ALBUM, FETCH_SONGS_ALBUM } from '../store/actions.type';

export default {
    data() {
        return {
            id: this.$route.params.id,
            loading: false,        
        }
    },
    
    watch: {
        '$route' (to) {
            if(to.name == 'album') {
                this.id = this.$route.params.id;
                this.initData();
            }
        } 
    },
    methods: {
        async initData() {
            this.loading = true;
            await this.$store.dispatch(FETCH_ALBUM, this.id);
            await this.$store.dispatch(FETCH_SONGS_ALBUM, this.id);
            this.loading = false;
        }
    },

    created() {
        this.initData();
    },
    filters: {
        formatNumber: function (value) {
            return numeral(value).format("0,0");
        }
    },
    computed: {
        ...mapGetters(['selectedAlbum', 'songsAlbum']),
    },
    components: {
        TrackBoxAlt,
        Loading
    }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";
@import "../scss/_mixins.scss";

.album-details{
    &__loading {
        position: absolute;
        top: 40%;
        left: 50%;
    }

    &__header {
        background-image: linear-gradient($color-primary-3, $color-primary-2);
        margin: -2rem -5rem 0 -5rem;
        padding: 7rem 5rem 2rem 5rem;
        display: flex;
        height: 38rem;

        &--left {
            display: flex;
            align-items: center;
        }

        &--right {
            margin-left: auto;
            margin-right: 0;
            display: flex;
            align-items: flex-end;
        }

        &__cover-image {
            width: 25rem;
            height: 25rem;
            background-size: cover;
            background-clip: padding-box;
            background-position: center center;
            box-shadow: 0 0 5rem $color-primary-1;
            border-radius: .3rem;
            margin-right: 3rem;
        }

        &__info {
            max-width: 100rem;
            font-family: inherit;
                @include respond(small-laptop) {
                    max-width: 50rem;
                }
                @include respond(phone) {
                    max-width: 30rem;
                }

            h1 {
                font-size: 7rem;

                @include respond(small-laptop) {
                    font-size: 5rem;
                }
                @include respond(tablet-port) {
                    font-size: 3rem;
                }
            }

            h3 {
                font-size: 2.2rem;
                & > * {
                    color: $color-secondary;
                    display: block;
                    text-decoration: none;
                }
            }

            h4 {
                font-size: 1.6rem;
                color: #bbbbbb;
            }
        }

        &__views {
            font-size: 1.7rem;
            color: #aaaaaa; 
        }
    }

    &__playlist {
        margin-top: 2rem;
        & > * {
            & > * {
                border-bottom: 2px solid $color-primary-2;
            }
        }
    }
}
</style>