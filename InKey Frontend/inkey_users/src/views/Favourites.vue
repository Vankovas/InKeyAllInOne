<template>
<div>
    <div v-if="loading" class="favourites-loading">
        <loading/>
    </div>
    <div v-else>
        <section class="section-favourite-tracks">
            <h2 class="main-heading">Favourite Tracks</h2>
            <div class="section-favourite-tracks__wrapper" v-if="favouriteSongs.length > 0">
                <div>
                    <TrackBoxAlt v-for="(track, index) in favouriteSongs" :key="track.id" :id="track.id" :index="index+1"
                        :name="track.name" :artist="track.artist" :duration="track.duration" :rating="track.rating" :data="track.data">
                        <button type="button" class="section-favourite-tracks__remove-btn"
                            @click="removeTrackFromFavouriteTracks(track.id)">
                            <font-awesome-icon icon="times" /></button>
                    </TrackBoxAlt>
                </div>
            </div>
            <div class="section-favourite-artists__wrapper" v-else>
                <h1> You dont have any favourite tracks at the moment.</h1>
            </div>
        </section>
        <section class="section-favourite-albums">
            <h2 class="main-heading">Favourite Albums</h2>
            <div class="section-favourite-albums__wrapper" v-if="userFavouriteAlbums.length > 0">
                <AlbumBox class="section-favourite-albums__album" v-for="album in userFavouriteAlbums" :key="album.id" :id="album.id"
                    :name="album.name" :artist_id="album.artist" :artist_name="album.artist_name" :coverImage="album.cover_image">
                    <button type="button" class="section-favourite-albums__album__remove-btn"
                        @click="removeAlbumFromFavouriteAlbums(album.id)">
                        <font-awesome-icon icon="times" /></button>
                </AlbumBox>
            </div>
            <div class="section-favourite-artists__wrapper" v-else>
                <h1> You dont have any favourite albums at the moment.</h1>
            </div>
        </section>
        <section class="section-favourite-artists">
            <h2 class="main-heading">Favourite Artists</h2>
            <div class="section-favourite-artists__wrapper" v-if="userFavouriteArtists.length > 0">
                <ArtistBox v-for="artist in userFavouriteArtists" :key="artist.id" :id="artist.id" :name="artist.firstname" :coverImage="artist.profile_picture">
                    <button type="button" class="section-favourite-artists__remove-btn"
                        @click="removeArtistFromFavouriteArtists(artist.id)">
                        <font-awesome-icon icon="times" /></button>
                </ArtistBox>
            </div>
            <div class="section-favourite-artists__wrapper" v-else>
                <h1> You dont have any favourite artists at the moment.</h1>
            </div>
        </section>
    </div>
</div>

</template>

<script>
import AlbumBox from '../components/AlbumBox'
import TrackBoxAlt from '../components/TrackBoxAlt'
import ArtistBox from '../components/ArtistBox'
import { mapGetters } from 'vuex'
import { ADD_REMOVE_USER_FAVOURITE_ALBUM, FETCH_USER_FAVOURITE_ALBUMS, ADD_REMOVE_USER_FAVOURITE_SONG, FETCH_USER_FAVOURITE_SONGS, ADD_REMOVE_USER_FAVOURITE_ARTIST, FETCH_USER_FAVOURITE_ARTISTS } from '../store/actions.type';
import Loading from '../components/Loading'

export default {
    data() {
        return {
            loading: false,

            albums: [
                {
                id: 1,
                name: "The Slim Shady LP",
                artist: "Eminem",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/515qfLDCFdL._SY400_.jpg"
                },
                {
                id: 2,
                name: "2014 Forest Hills Drive",
                artist: "J. Cole",
                cover_image: "https://www.hiphopinjesmoel.com/wp-content/uploads/2014/12/forest.jpeg"
                },
                {
                id: 3,
                name: "ADHD",
                artist: "Joyner Lucas",
                cover_image: "https://images.genius.com/d0eb2b80d212b93b097d604c4c6af62e.680x680x1.jpg"
                },
                {
                id: 4,
                name: "Recovery",
                artist: "Eminem",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/61fXEwg-lAL._SL1400_.jpg"
                },
                        {
                id: 5,
                name: "The Warm Up",
                artist: "J. Cole",
                cover_image: "https://m.media-amazon.com/images/I/71UcCxHKbEL._SS500_.jpg"
                },
                {
                id: 6,
                name: "21",
                artist: "Adele",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/61lMwNQGYbL._AC_SL1200_.jpg"
                },
                        {
                id: 7,
                name: "Natural Causes",
                artist: "Skylar Grey",
                cover_image: "https://img.discogs.com/FV19_bOhu9RfacoWVCCKSEWjTpA=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-9112864-1474991187-5089.jpeg.jpg"
                },
                { id: 8,
                name: "The Slim Shady LP",
                artist: "Eminem",
                cover_image: "https://images-na.ssl-images-amazon.com/images/I/515qfLDCFdL._SY400_.jpg"
                },
                {
                id: 9,
                name: "2014 Forest Hills Drive",
                artist: "J. Cole",
                cover_image: "https://www.hiphopinjesmoel.com/wp-content/uploads/2014/12/forest.jpeg"
                },
                {
                id: 10,
                name: "ADHD",
                artist: "Joyner Lucas",
                cover_image: "https://images.genius.com/d0eb2b80d212b93b097d604c4c6af62e.680x680x1.jpg"
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
                artist: "G-Easy",
                duration: "3:11",
                rating: 3.6,
                data: null
                },
                {
                id: 5,
                name: "Clout",
                artist: "Offset",
                duration: "3:45",
                rating: 3.1,
                data: null
                },
                {
                id: 6,
                name: "Leaving Heaven",
                artist: "Eminem",
                duration: "3:12",
                rating: 4.4,
                data: null
                },
                {
                id: 7,
                name: "Life is Good",
                artist: "Future",
                duration: "5:36",
                rating: 4.8,
                data: null
                },
                {
                id: 8,
                name: "Keanu Reaves",
                artist: "Logic",
                duration: "4:07",
                rating: 1.2,
                data: null
                },
                {
                id: 9,
                name: "Kamikaze",
                artist: "Eminem",
                duration: "3:37",
                rating: 4.2,
                data: null
                },
                {
                id: 10,
                name: "Still Be Friends",
                artist: "G-Easy",
                duration: "3:57",
                rating: 2.2,
                data: null
                },
                {
                id: 11,
                name: "Lotto",
                artist: "Joyner Lucas",
                duration: "3:45",
                rating: 4.2,
                data: null
                },
                {
                id: 12,
                name: "Still D.R.E.",
                artist: "Snoop Dogg",
                duration: "4:52",
                rating: 5,
                data: null
                },
                {
                id: 13,
                name: "Riders On The Storm",
                artist: "Snoop Dogg",
                duration: "5:12",
                rating: 3,
                data: null
                },
                        {
                id: 14,
                name: "Praise The Lord",
                artist: "A$AP Rocky",
                duration: "3:36",
                rating: 2,
                data: null
                },
                        {
                id: 15,
                name: "Next Episode",
                artist: "Snoop Dogg",
                duration: "3:19",
                rating: 1,
                data: null
                },
            ],
            artists: [
                {
                id: 1,
                name: "Eminem",
                cover_image: "https://www.rollingstone.com/wp-content/uploads/2020/01/eminem-review.jpg"
                },
                {
                id: 2,
                name: "50 Cent",
                cover_image: "https://images2.persgroep.net/rcs/gQ4_1AQ4yyWYk15LFEWGL7qXx2Q/diocontent/135007819/_fitwidth/694/?appId=21791a8992982cd8da851550a453bd7f&quality=0.8"
                },
                {
                id: 3,
                name: "Snoop Dogg",
                cover_image: "https://e-cdns-images.dzcdn.net/images/artist/a423dd42b7394eeacc882be8ac633eee/500x500.jpg"
                },
                {
                id: 4,
                name: "G-Easy",
                cover_image: "https://www.biography.com/.image/t_share/MTQ3Mzg3MzA1OTU3NTMzMzY3/g_eazy_photo_by_larry_marano_getty_images_entertainment_getty_457429866.jpg"
                },
                {
                id: 5,
                name: "Logic",
                cover_image: "https://upload.wikimedia.org/wikipedia/commons/6/6d/Logic_at_2018_VMAs.png"
                },

                        {
                id: 7,
                name: "Tech N9ne",
                cover_image: "https://imagesvc.meredithcorp.io/v3/mm/image?q=85&c=sc&poi=face&w=2000&h=1047&url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F20%2F2019%2F03%2Ftech-n9ne-2000.jpg"
                },
                        {
                id: 8,
                name: "Hopsin",
                cover_image: "https://images.complex.com/complex/images/c_fill,dpr_auto,f_auto,q_90,w_1400/fl_lossy,pg_1/uqztcuubujccuphj8v4i/hopsin"
                },
                                {
                id: 6,
                name: "Joyner Lucas",
                cover_image: "https://partyflock.nl/images/artist/110268_404x404_487553/Joyner-Lucas.jpg"
                },
            ]
        }
    },
    mounted() {
        this.fetchData();
    },
    watch: {
        '$route' () {
            this.fetchData();
        }
    },
    computed: {
        ...mapGetters(['favouriteSongs', 'userFavouriteAlbums', 'userFavouriteArtists']),
    },
    methods: {
        async removeAlbumFromFavouriteAlbums(id) {
            this.loading = true;
            await this.$store.dispatch(ADD_REMOVE_USER_FAVOURITE_ALBUM, id);
            this.loading = false;
        },
        async removeTrackFromFavouriteTracks(id) {
            this.loading = true;
            await this.$store.dispatch(ADD_REMOVE_USER_FAVOURITE_SONG, id);
            this.loading = false;
        },
        async removeArtistFromFavouriteArtists(id) {
            this.loading = true;
            await this.$store.dispatch(ADD_REMOVE_USER_FAVOURITE_ARTIST, id);
            this.loading = false;
        },
        async fetchData() {
            this.loading = true;
            await this.$store.dispatch(FETCH_USER_FAVOURITE_ALBUMS);
            await this.$store.dispatch(FETCH_USER_FAVOURITE_ARTISTS);
            await this.$store.dispatch(FETCH_USER_FAVOURITE_SONGS);
            this.loading = false;
        }
    },

    components: {
        AlbumBox,
        TrackBoxAlt,
        ArtistBox,
        Loading,
    },
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.favourites-loading {
    position: absolute;
    top: 40%;
    left: 50%;
}

.main-heading {
  font-size: 2.5rem;
  color: darken($color: $color-secondary, $amount: 10);
  margin-bottom: 2rem;
  display: inline-flex;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0rem;
    left: 0;
    width: 100%;
    border: 0; 
    height: 1px; 
    background: linear-gradient(to left, transparent , $color-secondary, transparent);
  }
}
.section-favourite-tracks {

    margin: 2rem 0;

    &__wrapper > *{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(70rem, 2fr));
        column-gap: 5rem;

        & > h1 {
            font-size: 1.6rem;
            color: #dddddd;
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

.section-favourite-albums {
    margin: 5rem 0;

    &__wrapper {
        display: grid;
        grid-template-columns: repeat( auto-fit, 35rem );
        grid-template-rows: auto;
        gap: 2rem;

        & > h1 {
            font-size: 1.6rem;
            color: #dddddd;
        }
    }

    &__album {

        &__remove-btn {
            cursor: pointer;
            width: 3.5rem;
            height: 3.5rem;
            position: absolute;
            top: 1rem;
            right: 1rem;
            z-index: 1;
            border-radius: 50%;
            border: none;
            outline: none;
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
}

.section-favourite-artists {
    margin: 5rem 0;

    &__wrapper {
        display: grid;
        grid-template-columns: repeat( auto-fit, 35rem);
        grid-template-rows: auto;
        gap: 2rem;

        & > h1 {
            font-size: 1.6rem;
            color: #dddddd;
        }
    }

        &__remove-btn {
            cursor: pointer;
            width: 3.5rem;
            height: 3.5rem;
            position: absolute;
            top: 2rem;
            right: 3rem;
            z-index: 1;
            border-radius: 50%;
            border: none;
            outline: none;
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
</style>