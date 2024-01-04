<template>
  <div>
    <div class="create-playlists-loading" v-if="loading">
      <Loading />
    </div>
    <div class="create-playlists" v-else>
      <h1>Your Playlists</h1>
      <section class="section-my-playlists">
        <div class="playlists-wrapper">
          <PlaylistBox v-for="playlist in userPlaylists" :key="playlist.id" :id="playlist.id" :name="playlist.name"
            :creator="playlist.user_name">
            <button type="button" class="remove-playlist" @click="removePlaylist(playlist.id)">
              <font-awesome-icon icon="times" /></button>
          </PlaylistBox>

          <div class="create-playlist">
            <div>
              <button class="create-playlist__create-btn" type="button" @click="createPlaylistModal">
                <font-awesome-icon icon="plus" /></button>
              <div class="create-playlist__info">
                <h1 @click="createPlaylistModal">Create New Playlist</h1>
              </div>
            </div>
          </div>
        </div>
      </section>
      <div v-if="showPlaylistModal" class="modal">
        <div class="modal__content">
          <div class="modal__form">
            <div class="modal__form__header">
              <h1>Create New Playlist</h1>
            </div>
            <form @submit.prevent="createPlaylist" class="form">
              <div class="form__form-group">
                <label for="playlistName">Playlist Name:</label>
                <input class="input-primary" name="playlistName" type="text" v-model="newPlaylist.name" />
              </div>
              <div class="form__form-group">
                <label for="playlistDescription">Description:</label>
                <input class="input-primary" name="playlistDescription" type="text" v-model="newPlaylist.description" />
              </div>
              <button class="form__btn btn-primary">
                Create
              </button>
              <button class="form__btn btn-secondary" type="button" @click="showPlaylistModal = false">
                Cancel
              </button>
            </form>
          </div>
          <div class="modal__close">
            <button type="btn" @click="showPlaylistModal = false">
              <font-awesome-icon icon="times" /></button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import PlaylistBox from '../components/PlaylistBox'
import {
  mapGetters
} from 'vuex'
import Loading from '../components/Loading'
import {
  FETCH_USER_PLAYLISTS,
  CREATE_PLAYLIST,
  DELETE_PLAYLIST
} from '../store/actions.type';

export default {
  data() {
    return {
      showPlaylistModal: false,
      newPlaylist: {
        name: null,
        description: null,
      },
      loading: false,
    }
  },
  computed: {
    ...mapGetters(['userPlaylists']),
  },
  mounted() {
    this.fetchPlaylists();
  },
  watch: {
    '$route'() {
      this.fetchPlaylists();
    }
  },
  methods: {
    createPlaylistModal() {
      this.showPlaylistModal = true;
      this.newPlaylist = {
        name: null,
        description: null,
      }
    },
    async createPlaylist() {
      if (this.newPlaylist.name && this.newPlaylist.description) {
        this.loading = true;
        await this.$store.dispatch(CREATE_PLAYLIST, { name: this.newPlaylist.name, description: this.newPlaylist.description });
        this.loading = false;
        this.showPlaylistModal = false;
      } else {
        alert("Please specify the name and the desciption");
      }
    },
    async removePlaylist(id) {
        this.loading = true;
        await this.$store.dispatch(DELETE_PLAYLIST, id);
        this.loading = false;
    },
    async fetchPlaylists() {
      this.loading = true;
      await this.$store.dispatch(FETCH_USER_PLAYLISTS);
      this.loading = false;
    }
  },
  components: {
    PlaylistBox,
    Loading
  }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";

.create-playlists-loading {
  position: absolute;
  top: 50%;
  left: 50%;
}

.create-playlists {
  &>h1 {
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
      background: linear-gradient(to left, transparent, $color-secondary, transparent);
    }
  }
}

.section-my-playlists {
  display: flex;
}

.playlists-wrapper {
  margin: 2rem 0 3.5rem 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, 20rem);
  grid-template-rows: auto;
  gap: 2rem;
  width: 100%;
}

.create-playlist {
  display: inline-block;
  background-color: $color-primary-3;
  padding: 2.5rem;
  border-radius: .8rem;
  height: 28.6rem;
  width: 20rem;

  &__create-btn {
    cursor: pointer;
    background-color: darken($color: $color-primary-3, $amount: 10);
    border: none;
    outline: none;
    padding: 3rem;
    margin-bottom: 2rem;
    border-radius: .2rem;
    box-shadow: 0 0 4rem .5rem rgba($color: $color-primary-1, $alpha: 0.3);
    transition: all .2s ease-in;

    &:hover,
    &:active {
      background-color: lighten($color: $color-primary-3, $amount: 20);
    }

    &:hover~*,
    &:active~* {
      transform: scale(1.1);
    }

    &>* {
      font-size: 10.3rem;
      color: $color-white;
    }
  }

  &__info {
    text-align: center;
    transition: all .1s ease-in;

    &>h1 {
      cursor: pointer;
      font-size: 2rem;
    }

    &:hover,
    &:active {
      transform: scale(1.1);
    }
  }
}

.remove-playlist {
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

  &:hover,
  &:active {
    background-color: $color-secondary;
  }

  &>* {
    color: $color-white;
    font-size: 1.8rem;
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
</style>