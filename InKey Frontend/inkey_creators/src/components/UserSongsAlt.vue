<template>
  <div id="UserSongsAlt">
    <CreateEditAlbumModal
      v-if="createEditAlbumModal.visible"
      @hideModal="hideAlbumModal"
      :mode="createEditAlbumModal.mode"
      :album="createEditAlbumModal.album"
    ></CreateEditAlbumModal>
    <CreateEditSongModal
      v-if="createEditSongModal.visible"
      @hideModal="hideSongModal"
      :mode="createEditSongModal.mode"
      :song="createEditSongModal.song"
    ></CreateEditSongModal>
    <DeleteItemModal
      v-if="deleteItemModal.visible"
      @hideModal="hideDeleteItemModal"
      :type="deleteItemModal.type"
      :item="deleteItemModal.item"
    ></DeleteItemModal>
    <MoveSongModal v-if="moveSongModal.visible" :song="moveSongModal.song" @hideModal="hideMoveSongModal"></MoveSongModal>
    <div class="songs-container">
      <button
        v-if="currentCreator.id && currentUser.id && currentCreator.id === currentUser.id"
        type="button"
        class="songs-container__create-btn"
        @click="showCreateSongModal"
      >
        Upload Song
        <img src="../assets/images/add.png" alt="" />
      </button>
      <h1 v-if="!allSongs || allSongs.length < 1">No songs to show</h1>
      <div class="songs-container__content">
        <template v-for="(track, index) in allSongs">
          <Track
            :key="track.id"
            :id="track.id"
            :index="index + 1"
            :name="track.name"
            :description="track.description"
            :rating="track.rating"
            :views="track.views"
            :data="track.data"
            :song="track"
            @showEditSongModal="showEditSongModal"
            @showDeleteSongModal="showDeleteSongModal"
            @showMoveSongModal="showMoveSongModal"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { FETCH_ALL_SONGS } from '../store/actions.type';

import Track from './Track';
import CreateEditAlbumModal from './CreateEditAlbumModal';
import CreateEditSongModal from './CreateEditSongModal';
import DeleteItemModal from './DeleteItemModal';
import MoveSongModal from './MoveSongModal';

export default {
  name: 'UserSongsAlt',

  components: {
    Track,
    CreateEditAlbumModal,
    CreateEditSongModal,
    DeleteItemModal,
    MoveSongModal,
  },

  props: {
    creatorId: String,
  },

  created() {
    this.fetchAllSongs(0, 10);
  },

  watch: {
    creatorId(newId, oldId) {
      if (newId !== oldId) this.fetchAllSongs(0, 10);
    },
  },

  data() {
    return {
      createEditAlbumModal: {
        mode: '',
        album: null,
        visible: false,
      },
      createEditSongModal: {
        mode: '',
        song: null,
        visible: false,
      },
      deleteItemModal: {
        type: '',
        item: null,
        visible: false,
      },
      moveSongModal: {
        song: null,
        visible: false,
      },
    };
  },

  computed: { ...mapGetters(['currentCreator', 'allSongs', 'currentUser']) },

  methods: {
    showCreateAlbumModal() {
      this.createEditAlbumModal.mode = 'Create';
      this.createEditAlbumModal.album = {};
      this.createEditAlbumModal.visible = true;
    },
    hideAlbumModal() {
      this.createEditAlbumModal.album = {};
      this.createEditAlbumModal.visible = false;
    },
    showEditSongModal(song) {
      this.createEditSongModal.mode = 'Edit';
      this.createEditSongModal.song = song;
      this.createEditSongModal.visible = true;
    },
    showCreateSongModal() {
      this.createEditSongModal.mode = 'Create';
      this.createEditSongModal.song = {};
      this.createEditSongModal.visible = true;
    },
    showDeleteSongModal(song) {
      this.deleteItemModal.type = 'song';
      this.deleteItemModal.item = song;
      this.deleteItemModal.visible = true;
    },
    hideSongModal() {
      this.createEditSongModal.song = {};
      this.createEditSongModal.visible = false;
    },
    hideDeleteItemModal() {
      this.deleteItemModal.item = {};
      this.deleteItemModal.visible = false;
    },
    showMoveSongModal(song) {
      this.moveSongModal.song = song;
      this.moveSongModal.visible = true;
    },
    hideMoveSongModal() {
      this.moveSongModal.song = null;
      this.moveSongModal.visible = false;
    },
    fetchAllSongs(attemptNo, maxAttempts) {
      console.log(`Fetching songs -> ${attemptNo}`);
      const creatorId = this.$props.creatorId;

      if (attemptNo >= maxAttempts) throw 'Could not fetch creator songs on time';
      if (creatorId === null || creatorId === undefined)
        return setTimeout(() => {
          this.fetchAllSongs(attemptNo + 1, maxAttempts);
        }, 500);

      this.$store.dispatch(FETCH_ALL_SONGS, creatorId);
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

#UserSongsAlt {
  .songs-container {
    width: 100%;
    height: 48vh;
    overflow-y: auto;

    @include respond(tablet-land) {
      height: 55vh;
    }

    @include respond(tablet-port) {
      height: 58vh;
    }

    &::-webkit-scrollbar {
      width: 0.7rem;
      background-color: #fff6f7;
    }
    &::-webkit-scrollbar-thumb {
      border-radius: 10px;
      background-image: -webkit-gradient(
        linear,
        left bottom,
        left top,
        color-stop(0.44, $color-primary),
        color-stop(0.72, $color-secondary),
        color-stop(0.86, $color-tertiary)
      );
    }

    &__create-btn {
      cursor: pointer;
      font-size: 1.6rem;
      padding: 1rem 1.5rem;
      display: block;
      margin: auto;
      background: transparent;
      border: 1px solid black;
      border-radius: 0.3rem;
      display: flex;
      align-items: center;
      margin-bottom: 2rem;
      outline: none;

      & > * {
        width: 1.4rem;
        margin-left: 0.7rem;
      }

      &:hover {
        background-color: darken($color: #fff6f7, $amount: 5);
      }

      &:active {
        background-color: darken($color: #fff6f7, $amount: 2);
      }
    }

    &__content {
      font-size: 1.7rem;
      transition: max-height 0.2s ease-out;
      padding: 0 10rem;

      @include respond(tablet-land) {
        padding: 0 1rem;
      }

      & > * {
        &:not(:last-child) {
          border-bottom: 1px solid #ddd;
        }
      }

      .tabs-container {
        height: 100%;
      }
    }
  }
}
</style>
