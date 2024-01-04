<template>
  <div>
    <section class="section-popular-albums">
      <h2 class="main-heading">Popular Albums</h2>
      <Carousel :perPageCustom="[[2500, 6],[2100, 5],[1600, 4],[1300, 3],[700, 2], [500, 1], [300, 1]]" :paginationEnabled="false">
        <Slide v-for="album in mostViewedAlbums" :key="album.id">
          <AlbumBox :id="album.id" :name="album.name" :artist_name="album.artist_name" :artist_id="album.artist" :coverImage="album.cover_image" :rating="album.rating"/>
        </Slide>
      </Carousel>
    </section>
    <section class="section-trending-albums">
      <h2 class="main-heading">Trending Now</h2>
      <Carousel :perPageCustom="[[2500, 6],[2100, 5],[1600, 4],[1300, 3],[700, 2], [500, 1], [300, 1]]" :paginationEnabled="false">
        <Slide v-for="album in trendingAlbums" :key="album.id">
          <AlbumBox :id="album.id" :name="album.name" :artist_name="album.artist_name" :artist_id="album.artist" :coverImage="album.cover_image" :rating="album.rating"/>
        </Slide>
      </Carousel>
    </section>
    <section class="section-top-rated-albums">
      <h2 class="main-heading">Top Rated</h2>
      <Carousel :perPageCustom="[[2500, 6],[2100, 5],[1600, 4],[1300, 3],[700, 2], [500, 1], [300, 1]]" :paginationEnabled="false">
        <Slide v-for="album in topAlbums" :key="album.id">
          <AlbumBox :id="album.id" :name="album.name" :artist_name="album.artist_name" :artist_id="album.artist" :coverImage="album.cover_image" :rating="album.rating"/>
        </Slide>
      </Carousel>
    </section>
  </div>
</template>

<script>
import { Carousel, Slide } from 'vue-carousel'
import AlbumBox from '../components/AlbumBox'
import { mapGetters } from 'vuex'

export default {
    data() {
        return {
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
        }
    },
    computed: {
      ...mapGetters(['topAlbums', 'mostViewedAlbums', 'trendingAlbums']),
    },

    components: {
        AlbumBox,
        Carousel,
        Slide
    },
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

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

.section-popular-albums, .section-trending-albums, .section-top-rated-albums {
    margin: 2rem 0 4rem 0;
}

</style>