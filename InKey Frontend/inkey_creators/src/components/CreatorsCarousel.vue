<template>
  <div class="carousel">
    <swiper class="swiper" :options="swiperOption">
      <swiper-slide v-for="(creator, index) in this.featuredCreators" :key="index">
        <!-- albumName="AlbumName" -->
        <FeaturedCreatorCard
          :creatorId="creator.id"
          :creatorName="creator.firstname + ' ' + creator.lastname"
          :likes="Math.random() * 100000"
          :follows="Math.random() * 100000"
          :imageUrl="creator.profile_picture"
        />
      </swiper-slide>
    </swiper>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { FETCH_FEATURED_CREATORS } from '../store/actions.type';

import { Swiper, SwiperSlide } from 'vue-awesome-swiper';
import FeaturedCreatorCard from './FeaturedCreatorCard.vue';

export default {
  created() {
    this.$store.dispatch(FETCH_FEATURED_CREATORS);
  },
  computed: {
    ...mapGetters(['featuredCreators']),
  },
  data() {
    return {
      swiperOption: {
        effect: 'coverflow',
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: '3',
        coverflowEffect: {
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: false,
        },
      },

      mockCreators: [
        {
          creatorId: 1,
          creatorName: 'Future',
          albumName: 'Beast Mode 2',
          likes: 2386,
          follows: 13165,
          imageUrl: 'https://media.nu.nl/m/utfx1mpa5ljy_wd640.jpeg',
        },
        {
          creatorId: 2,
          creatorName: 'Drake',
          albumName: 'So Far Gone',
          likes: 622586,
          follows: 13165,
          imageUrl: 'https://i2.wp.com/www.dailycal.org/assets/uploads/2018/10/Drake_Kevin-Mazur-Getty-Images_File-copy.jpg?ssl=1',
        },
        {
          creatorId: 3,
          creatorName: 'Eminem',
          albumName: 'Music to Be Murdered By',
          likes: 7652386,
          follows: 3413165,
          imageUrl:
            'https://www.biography.com/.image/t_share/MTQ3NjM5MTEzMTc5MjEwODI2/eminem_photo_by_dave_j_hogan_getty_images_entertainment_getty_187596325.jpg',
        },
        {
          creatorId: 4,
          creatorName: 'J. Cole',
          albumName: '4 Your Eyez Only',
          likes: 1352386,
          follows: 1513165,
          imageUrl:
            'https://www.grammy.com/sites/com/files/styles/image_landscape_hero/public/muzooka/J.%2BCole/J.%2520Cole_16_9_1581558280.jpg?itok=OH3_rUF-',
        },
        {
          creatorId: 5,
          creatorName: 'Joyner Lucas',
          albumName: 'ADHD',
          likes: 232386,
          follows: 135165,
          imageUrl: 'https://hiphop-n-more.com/wp-content/uploads/2020/02/joyner-lucas-2_0.jpg',
        },
      ],
    };
  },

  components: {
    Swiper,
    SwiperSlide,
    FeaturedCreatorCard,
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';

.carousel {
  width: 104rem;
  height: 60rem;
  display: flex;
  justify-content: center;
}
.swiper-wrapper {
  height: 90%;
}
.swiper {
  height: 100%;
  width: 100%;

  .swiper-slide {
    height: 46rem;
    box-shadow: 0 6px 10px -5px gray;
    padding-top: 1rem;
  }
}
</style>
