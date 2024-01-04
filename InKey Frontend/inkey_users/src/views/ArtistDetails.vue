<template>
  <div>
    <div class="artist-details-loading" v-if="loading">
      <Loading />
    </div>
    <div class="artist-details" v-else>
      <div class="artist-details__header"
        :style="selectedArtist.profile_picture ? { backgroundImage: 'url(' + selectedArtist.profile_picture + ')'} : { backgroundImage: 'url(' + 'https://houstoncertifiedmidwife.com/wp-content/uploads/2016/05/orange-profile-background-1.png' + ')'}">
        <div class="artist-details__header__wrapper">
          <div class="artist-details__header__info">
            <h1>{{ selectedArtist.firstname }}</h1>
          </div>
        </div>
      </div>
      <button type="button" class="btn-secondary" v-if="isAuthenticated"
        @click="addRemoveFavouriteArtist">{{addedToFavourites ? 'Remove From ' : 'Add To '}} Favourites</button>
      <h1>Albums</h1>
      <hr>
      <div class="artist-details__albums">
        <AlbumBox v-for="album in albumsArtist" :key="album.id" :id="album.id" :name="album.name"
          :artist_id="album.artist" :artist_name="album.artist_name" :coverImage="album.cover_image">
        </AlbumBox>
      </div>
      <h1>Tracks</h1>
      <hr>
      <div class="artist-details__playlist">
        <div v-for="(track, index) in songsArtist" :key="track.id">
          <TrackBoxAlt :id="track.id" :index="index+1" :name="track.name" :artist="track.artist"
            :duration="track.duration" :rating="track.rating"  :data="track.data" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TrackBoxAlt from '../components/TrackBoxAlt'
import Loading from '../components/Loading'
import AlbumBox from '../components/AlbumBox'
import numeral from 'numeral'
import { mapGetters } from 'vuex'
import { FETCH_SONGS_ARTIST, FETCH_ALBUMS_ARTIST, FETCH_ARTIST, ADD_REMOVE_USER_FAVOURITE_ARTIST } from '../store/actions.type';

export default {
    data() {
        return {
            id: this.$route.params.id,
            addedToFavourites: false,
            loading: false,

            //MOCK DATA
            mockData: {
                username: "Eminem",
                profile_picture: "https://en.festileaks.com/wp-content/uploads//2018/01/eminem-e1517088059245.jpg",
            },
            albums: [
              {
                id: 1,
                name: "The Slim Shady LP",
                artist: "Eminem",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/515qfLDCFdL._SY400_.jpg"
              },
              {
                id: 4,
                name: "Recovery",
                artist: "Eminem",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/61fXEwg-lAL._SL1400_.jpg"
              },
              { id: 8,
                name: "The Slim Shady LP",
                artist: "Eminem",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/515qfLDCFdL._SY400_.jpg"
              },
            ],
            tracks: [
                    {
                    id: 1,
                    name: "The Way I Am",
                    artist: "Eminem",
                    duration: "2:24",
                    rating: 4.2,
                    data: null
                    },
                    {
                    id: 2,
                    name: "You Gon' Learn",
                    artist: "Eminem",
                    duration: "3:41",
                    rating: 3.2,
                    data: null
                    },
                    {
                    id: 3,
                    name: "Little Engine",
                    artist: "Eminem",
                    duration: "2:53",
                    rating: 5,
                    data: null
                    },
                    {
                    id: 4,
                    name: "Moana",
                    artist: "Eminem",
                    duration: "3:11",
                    rating: 3.6,
                    data: null
                    },
                ],
        
        }
    },
    watch: {
        '$route' (to) {
            if(to.name == 'artist') {
                this.id = this.$route.params.id;
                this.initData();
                this.addedToFavourites = false;
                this.userFavouriteArtists.forEach(element => {
                  if(element.id == this.selectedArtist.id) {
                    this.addedToFavourites = true;
                  }
                });
            }
        },
    },
    mounted() {
      this.initData();
      this.addedToFavourites = false;
      this.userFavouriteArtists.forEach(element => {
        if (element.id == this.selectedArtist.id) {
          this.addedToFavourites = true;
        }
      });
    },
    methods: {
      async initData() {
        this.loading = true;
        await this.$store.dispatch(FETCH_ARTIST, this.id);
        await this.$store.dispatch(FETCH_SONGS_ARTIST, this.id);
        await this.$store.dispatch(FETCH_ALBUMS_ARTIST, this.id);
        this.loading = false;
      },
      async addRemoveFavouriteArtist() {
        this.loading = true;
        await this.$store.dispatch(ADD_REMOVE_USER_FAVOURITE_ARTIST, this.id);
        this.loading = false;
        this.addedToFavourites = !this.addedToFavourites;
      },
    },
    computed: {
      ...mapGetters(['selectedArtist','albumsArtist', 'songsArtist', 'userFavouriteArtists', 'isAuthenticated']),
    },
    filters: {
        formatNumber: function (value) {
            return numeral(value).format("0,0");
        }
    },
    components: {
        TrackBoxAlt,
        AlbumBox,
        Loading,
    }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";
@import "../scss/_mixins.scss";

.artist-details-loading {
  position: absolute;
  top: 40%;
  left: 50%;
}

.artist-details{
    &__header {
        background-image: linear-gradient($color-primary-3, $color-primary-2);
        margin: -2rem -5rem 0 -5rem;
        padding: 0 5rem;
        display: flex;
        justify-content: flex-end;
        flex-direction: column;
        height: 40rem;
        background-size: cover;
        background-clip: padding-box;
        background-position: center;

        &__wrapper {
          display: inline-flex;
        }

        &__info {
            padding: 0 7rem;
            font-family: inherit;
            background-image: linear-gradient( rgba($color-primary-3, .6), rgba($color-primary-2, 1));
            border-top-left-radius: .3rem;
            border-top-right-radius: .3rem;
            display: flex;
            align-items: baseline;

            h1 {
                font-size: 8rem;
            }
        }
    }
            & > button {
              display: flex;
              align-items: center;
              padding: 1rem 2rem;
              margin-top: 2rem;
              border-radius: .5rem;

              & > * {
                font-size: 2rem;
              }
            }
    & > h1 {
      font-size: 2.5rem;
      color: $color-white;
      margin-top: 5rem;
    }

    & > hr {
      margin-bottom: 3rem;
      background-color: rgba($color: #cccccc, $alpha: .2);
      border: none;
      height: 2px;
    }

    &__albums {
      display: grid;
      grid-template-columns: repeat( auto-fit, 35rem );
      grid-template-rows: auto;
      gap: 2rem;
      margin-top: 4rem;
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