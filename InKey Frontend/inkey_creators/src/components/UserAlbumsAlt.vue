<template>
  <div class="albums-container">
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
    <button
      v-if="currentCreator.id && currentUser.id && currentCreator.id === currentUser.id"
      type="button"
      class="albums-container__create-btn"
      @click="showCreateAlbumModal"
    >
      Create Album
      <img src="../assets/images/add.png" alt="" />
    </button>

    <h1 v-if="!allAlbums || allAlbums.length < 1">No public albums to show</h1>

    <template v-for="album in allAlbums">
      <Album
        :key="album.id"
        :album="album"
        :id="album.id"
        :name="album.name"
        :description="album.description"
        :is_private="album.is_private"
        :cover_image="album.cover_image"
        @showEditAlbumModal="showEditAlbumModal"
        @showDeleteAlbumModal="showDeleteAlbumModal"
        @showEditSongModal="showEditSongModal"
        @showDeleteSongModal="showDeleteSongModal"
        @showMoveSongModal="showMoveSongModal"
      />
    </template>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { FETCH_ALL_ALBUMS } from '../store/actions.type';

import Album from './Album';
import CreateEditAlbumModal from './CreateEditAlbumModal';
import CreateEditSongModal from './CreateEditSongModal';
import DeleteItemModal from './DeleteItemModal';
import MoveSongModal from './MoveSongModal';

export default {
  name: 'UserAlbumsAlt',

  components: {
    Album,
    CreateEditAlbumModal,
    CreateEditSongModal,
    DeleteItemModal,
    MoveSongModal,
  },

  props: {
    creatorId: String,
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

  created() {
    this.fetchAllAlbums(0, 10);
  },

  watch: {
    creatorId(newId, oldId) {
      if (newId !== oldId) this.fetchAllAlbums(0, 10);
    },
  },

  computed: {
    ...mapGetters(['allAlbums', 'selectedAlbum', 'currentCreator', 'currentUser']),
  },

  methods: {
    showEditAlbumModal(album) {
      this.createEditAlbumModal.mode = 'Edit';
      this.createEditAlbumModal.album = album;
      this.createEditAlbumModal.visible = true;
    },
    showCreateAlbumModal() {
      this.createEditAlbumModal.mode = 'Create';
      this.createEditAlbumModal.album = {};
      this.createEditAlbumModal.visible = true;
    },
    hideAlbumModal() {
      this.createEditAlbumModal.album = {};
      this.createEditAlbumModal.visible = false;
    },
    showDeleteAlbumModal(album) {
      this.deleteItemModal.type = 'album';
      this.deleteItemModal.item = album;
      this.deleteItemModal.visible = true;
    },
    hideDeleteItemModal() {
      this.deleteItemModal.item = {};
      this.deleteItemModal.visible = false;
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
    showMoveSongModal(song) {
      this.moveSongModal.song = song;
      this.moveSongModal.visible = true;
    },
    hideMoveSongModal() {
      this.moveSongModal.song = null;
      this.moveSongModal.visible = false;
    },
    fetchAllAlbums(attemptNo, maxAttempts) {
      console.log(`Fetching albums -> ${attemptNo}`);
      const creatorId = this.$props.creatorId;

      if (attemptNo >= maxAttempts) throw 'Could not fetch creator songs on time';
      if (creatorId === null || creatorId === undefined)
        return setTimeout(() => {
          this.fetchAllAlbums(attemptNo + 1, maxAttempts);
        }, 500);

      this.$store.dispatch(FETCH_ALL_ALBUMS, creatorId);
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

.albums-container {
  width: 100%;
  height: 50vh;
  overflow-y: auto;

  @include respond(laptop) {
    height: 53vh;
  }

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
}
</style>
