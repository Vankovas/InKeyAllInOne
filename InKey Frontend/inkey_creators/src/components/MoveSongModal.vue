<template>
  <div id="MoveSongModal">
    <div class="modal">
      <div class="modal-header">
        <h1 class="modal-header__title">Move Song</h1>
      </div>
      <form v-on:submit.prevent="submitChanges" class="modal-content">
        <div class="song-info">
          <div class="song-info__panel song-info__album">
            <label class="song-info__panel__label">Album</label>
            <select
              :class="'song-info__panel__input ' + { 'input-error': $v.updatedSong.album.$error }"
              name="album"
              v-model.trim="updatedSong.album"
              @input="setAlbum($event.target.value)"
            >
              <option v-for="album in allAlbums" :value="album.id" :key="`album${album.id}`">
                {{ album.name }}
              </option>
            </select>
            <div v-if="errors">
              <div class="error" v-if="!$v.updatedSong.album.required">Album is required.</div>
            </div>

            <div v-if="errors">
              <div class="error" v-if="!$v.updatedSong.album.required">Album is required.</div>
            </div>
          </div>

          <div class="song-info__panel song-info__controls">
            <input class="song-info__controls__save btn-secondary" type="submit" value="Save changes" />
            <button type="button" class="song-info__controls__cancel btn-secondary" @click="emitHideModal">Cancel</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import { UPDATE_SONG, FETCH_ALL_ALBUMS } from '../store/actions.type';

export default {
  name: 'MoveSongModal',
  mounted() {
    this.$store.dispatch(FETCH_ALL_ALBUMS, this.currentCreator.id);
  },
  data() {
    return {
      //Vuelidate song data
      updatedSong: {
        album: this.song.album || true,
      },
      //For preventing errors from popping up before submitting
      uiState: 'submit not clicked',
      errors: false,
      empty: true,
    };
  },
  props: {
    hideModal: Function,
    song: Object,
    mode: String,
  },
  //Vuelidate validations for song data
  validations: {
    updatedSong: {
      album: { required },
    },
  },
  methods: {
    emitHideModal() {
      this.$emit('hideModal');
    },
    setAlbum(value) {
      this.updatedSong.album = value;
      this.$v.updatedSong.album.$touch();
    },
    submitChanges() {
      this.formTouched = !this.$v.updatedSong.$anyDirty;
      this.errors = this.$v.updatedSong.$anyError;
      this.uiState = 'submit clicked';
      if (this.errors === false && this.formTouched === false) {
        if (this.updatedSong.album !== this.song.album) {
          const songData = { id: this.song.id, album: this.updatedSong.album };
          this.$store.dispatch(UPDATE_SONG, songData);
        }

        this.emitHideModal();
      }
    },
  },
  computed: {
    ...mapGetters(['allAlbums', 'currentCreator']),
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

#MoveSongModal {
  z-index: 1000;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(128, 128, 128, 0.5);

  .modal {
    width: 55%;
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    background-color: white;
    border-radius: 0.5rem;
    overflow: hidden;

    @include respond(tablet-land) {
      width: 70%;
    }
    @include respond(phone) {
      width: 90%;
    }

    &-header {
      background-color: $color-tertiary;
      color: $color-white;
      padding: 3rem;

      &__title {
        font-size: 2.5rem;
      }
    }

    &-content {
      display: flex;
      justify-content: space-around;
      align-items: center;

      width: 100%;
      margin: 0 auto;
      padding: 2rem 0;

      .song-info {
        width: 60%;
        font-size: 2rem;

        &__panel {
          display: inline-block;
          width: 100%;
          margin-bottom: 2rem;

          &-group {
            display: flex;
            justify-content: space-between;
          }

          &__label {
            font-size: 1.8rem;
            font-weight: 500;
          }

          &__input {
            font-size: 1.7rem;
            padding: 1rem 2rem;
            background-color: rgba(238, 238, 238, 0.2);
            border: 1px solid #393e46;
            border-radius: 0.3rem;
            width: 100%;
          }
        }

        &__panel > * {
          width: 100%;
        }

        &__controls {
          width: 100%;
          display: flex;
          justify-content: space-evenly;
          margin: 2rem 0;

          &__cancel,
          &__save {
            width: 30%;
            border-radius: 0.5rem;

            font-size: 2rem;
            line-height: 4rem;
          }

          &__save {
            width: 100%;
            margin-right: 2rem;
            border-color: $color-tertiary;
            background-color: $color-tertiary;
            color: $color-white;

            &:hover {
              background-color: $color-white;
              color: $color-tertiary;
            }
          }

          &__cancel {
            border-color: $color-tertiary;
            background-color: $color-white;
            color: $color-tertiary;

            &:hover {
              background-color: $color-tertiary;
              color: $color-white;
            }
          }
        }
      }
    }
  }

  .input-error {
    border-color: salmon;
  }

  .error {
    width: 100% !important;
    color: salmon;
    font-size: 1.5rem;
  }
}
</style>
