<template>
  <div id="CreateEditSongModal">
    <div class="modal">
      <div class="modal-header">
        <h1 class="modal-header__title">{{ this.$props.mode }} Song</h1>
      </div>
      <form v-on:submit.prevent="submitChanges" class="modal-content">
        <div class="song-info">
          <div class="song-info__panel song-info__data">
            <label class="song-info__panel__label__audio">Audio File</label>
            <div id="song-data-song-wrapper">
              <label id="song-data__label__upload" for="song-data">
                {{ dataLabel === 'Remove' ? 'Change' : 'Upload' }}
              </label>
              <input
                type="file"
                id="song-data"
                :class="'song-info__panel__input ' + { 'input-error': $v.updatedSong.data.$error }"
                name="data"
                @input="setSongData"
              />

              <template v-if="dataLabel === 'Remove'">
                <div id="song-data__label__remove" @click="removeSongData">
                  {{ dataLabel }}
                </div>
              </template>
            </div>
            <div style="display:block" v-if="errors">
              <div class="error" v-if="!$v.updatedSong.data.required">Album File is required.</div>
            </div>
          </div>

          <div class="song-info__panel song-info__name">
            <label class="song-info__panel__label">Song Name</label>
            <input
              :class="'song-info__panel__input ' + { 'input-error': $v.updatedSong.name.$error }"
              name="name"
              v-model.trim="updatedSong.name"
              @input="setSongName($event.target.value)"
            />
            <div v-if="errors">
              <div class="error" v-if="!$v.updatedSong.name.required">Song name is required.</div>
              <div class="error" v-if="!$v.updatedSong.name.minLength">
                Song name must have at least {{ $v.updatedSong.name.$params.minLength.min }} letters.
              </div>
              <div class="error" v-if="!$v.updatedSong.name.maxLength">
                Song name must have at most {{ $v.updatedSong.name.$params.maxLength.max }} letters.
              </div>
            </div>
          </div>

          <div class="song-info__panel song-info__description">
            <label class="song-info__panel__label">Description</label>
            <input
              :class="'song-info__panel__input ' + { 'input-error': $v.updatedSong.description.$error }"
              name="description"
              v-model.trim="updatedSong.description"
              @input="setDescription($event.target.value)"
            />
            <div v-if="errors">
              <div class="error" v-if="!$v.updatedSong.description.required">Description is required.</div>
              <div class="error" v-if="!$v.updatedSong.description.minLength">
                Description must have at least {{ $v.updatedSong.description.$params.minLength.min }} letters.
              </div>
              <div class="error" v-if="!$v.updatedSong.description.maxLength">
                Description must have at most {{ $v.updatedSong.description.$params.maxLength.max }} letters.
              </div>
            </div>
          </div>

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
import { minLength, maxLength, required } from 'vuelidate/lib/validators';
import { UPDATE_SONG, CREATE_SONG, FETCH_ALL_ALBUMS } from '../store/actions.type';

export default {
  name: 'CreateEditSongModal',
  mounted() {
    this.$store.dispatch(FETCH_ALL_ALBUMS, this.currentCreator.id);
  },
  data() {
    return {
      //Vuelidate song data
      updatedSong: {
        data: (this.song.data || '') + '',
        name: (this.song.name || '') + '',
        description: (this.song.description || '') + '',
        album: this.song.album || true,
      },
      //For preventing errors from popping up before submitting
      uiState: 'submit not clicked',
      errors: false,
      empty: true,
      //For song data elements
      dataLabel: this.song.data ? 'Remove' : 'Upload',
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
      data: { required },
      name: { required, minLength: minLength(4), maxLength: maxLength(70) },
      description: { required, minLength: minLength(4), maxLength: maxLength(200) },
      album: { required },
    },
  },
  methods: {
    emitHideModal() {
      this.$emit('hideModal');
    },
    setSongData(e) {
      this.updatedSong.data = e.target.files[0];
      this.$v.updatedSong.data.$touch();
      this.dataLabel = this.updatedSong.data ? 'Remove' : 'Upload';
    },
    removeSongData() {
      this.updatedSong.data = null;
      this.$v.updatedSong.data.$touch();
      this.dataLabel = this.updatedSong.data ? 'Remove' : 'Upload';
    },
    setSongName(value) {
      this.updatedSong.name = value;
      this.$v.updatedSong.name.$touch();
    },
    setDescription(value) {
      this.updatedSong.description = value;
      this.$v.updatedSong.description.$touch();
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
        const songData = {};

        ['id', 'name', 'description', 'album', 'data'].forEach((key) => {
          console.log(key, this.updatedSong[key], this.$props.song[key]);
          if (key === 'id') return (songData[key] = this.$props.song[key]);
          if (this.updatedSong[key] !== this.$props.song[key]) songData[key] = this.updatedSong[key];
        });

        if (this.$props.mode === 'Edit') this.$store.dispatch(UPDATE_SONG, songData);
        else if (this.$props.mode === 'Create') this.$store.dispatch(CREATE_SONG, songData);

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

#CreateEditSongModal {
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

    @include respond(small-laptop) {
      width: 70%;
    }

    @include respond(tablet-port) {
      width: 80%;
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

        @include respond(tablet-port) {
          width: 80%;
        }

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

            &__audio {
              display: block;
              font-size: 1.8rem;
              font-weight: 500;
            }
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

  #song-data__label__remove,
  #song-data__label__upload {
    background-color: $color-tertiary;
    color: $color-white;
    border: 1px solid $color-tertiary;
    padding: 1rem 2rem;

    display: inline;
    border-radius: 0.5rem;

    text-align: center;
    vertical-align: center;
    margin-left: 1rem;

    user-select: none;
    cursor: pointer;
  }

  #song-data__label__upload:hover {
    background-color: $color-white;
    color: $color-tertiary;
  }

  #song-data__label__remove {
    background-color: $color-white;
    color: $color-tertiary;

    &:hover {
      background-color: $color-tertiary;
      color: $color-white;
    }
  }

  #song-data {
    display: none;
  }

  #song-data-song-wrapper {
    display: flex;
    justify-content: space-evenly;
    padding-top: 0.5rem;
  }
}
</style>
