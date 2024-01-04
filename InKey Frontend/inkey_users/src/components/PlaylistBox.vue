<template>
  <div class="playlist-box">
      <div class="playlist-box__cover">
        <img class="playlist-box__cover__image" src="../assets/images/music.png"/>
      </div>
      <div class="playlist-box__info">
          <h2 @click="routeToPlaylistDetails">{{name}}</h2>
          <h4>By {{creator}}</h4>
      </div>
      <button v-if="songs.length>0" class="playlist-box__play-btn" type="button" @click="playPlaylist"><font-awesome-icon icon="play"/></button>
      <slot></slot>
  </div>
</template>

<script>
import { EventBus } from '../common/event-bus'
import { FETCH_PLAYLIST } from '../store/actions.type'
import { mapGetters } from 'vuex'

export default {
    props: ['id', 'name', 'creator',],

    data() {
        return {
            songs: [] 
        }
    },

    methods: {
        async playPlaylist() {
            if(this.songs.length>0){
                EventBus.$emit("set-songs", this.songs, true);
            }
        },
        routeToPlaylistDetails() {
            const playlistId = this.$props.id;
            this.$router.push({ name: 'playlist', params: { id: playlistId } })
        },
        async loadSongs(){
            await this.$store.dispatch(FETCH_PLAYLIST, this.$props.id);
            if(this.selectedPlaylist !== undefined){
                this.songs = this.selectedPlaylist.songs;
            }
        }
    },
    mounted(){
        this.loadSongs();
    },
    computed:{
        ...mapGetters(['selectedPlaylist'])
    }
} 
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.playlist-box {
    background-color:  $color-primary-3;
    display: inline-block;
    padding: 2.5rem;
    border-radius: .8rem;
    position: relative;

    &:hover &__play-btn {
        z-index: 1;
    }

    &__cover {

        background-color: darken($color: $color-primary-3, $amount: 10); 
        padding: 2.5rem;
        border-radius: .2rem;
        box-shadow: 0 0 4rem .5rem rgba($color: $color-primary-1, $alpha: 0.3);

        &__image {
            width: 10rem;
        }
    }

    &__info {
        margin-top: 2rem;
        display: inline-block;

        & > h2 {
            cursor: pointer;
            font-size: 2.2rem;
        }

        & > h4 {
            font-size: 1.6rem;
            color: darken($color: $color-white, $amount: 25);
        }

    }

    &__play-btn {
        cursor: pointer;
        position: absolute;
        bottom: 1.5rem;
        right: 1.5rem;
        background-color: $color-secondary;
        padding: 1rem;
        width: 4rem;
        height: 4rem;
        border-radius: 50%;
        border: none;
        outline: none;
        transition: all .1s ease-in;
        z-index: -1;

        &:hover, &:active {
            box-shadow: 0 0 2rem 1rem rgba($color: $color-primary-1, $alpha: 0.2);
            transform: scale(1.1);
        }

        & > * {
            font-size: 1.8rem;
            margin-left: .3rem;
            display: block;
            color: $color-primary-1;
        }
    }
}

</style>