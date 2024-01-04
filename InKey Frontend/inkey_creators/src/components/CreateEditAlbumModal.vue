<template>
  <div id="CreateEditAlbumModal">
    <div class="modal">
      <div class="modal-header">
        <h1 class="modal-header__title">{{ this.$props.mode }} Album</h1>
      </div>
      <form v-on:submit.prevent="submitChanges" class="modal-content">
        <div class="album-image">
          <img
            class="album-image__img"
            v-bind:style="{ backgroundImage: 'url(' + (updatedAlbum.cover_image_local_url || updatedAlbum.cover_image || defaultAlbumCover) + ')' }"
          />
          <div class="album-image__edit-img">
            <label for="cover-image-upload">Change</label>
            <input id="cover-image-upload" value="Change" type="file" @change="getUserSelectedImage" />
          </div>
          <div v-if="errors">
            <div class="error" v-if="!$v.updatedAlbum.cover_image.required">Cover image is required.</div>
          </div>
        </div>

        <div class="album-info">
          <div class="album-info__panel album-info__name">
            <label class="album-info__panel__label">Album Name</label>
            <input
              :class="'album-info__panel__input ' + { 'input-error': $v.updatedAlbum.name.$error }"
              name="name"
              v-model.trim="updatedAlbum.name"
              @input="setAlbumName($event.target.value)"
            />
            <div v-if="errors">
              <div class="error" v-if="!$v.updatedAlbum.name.required">Album name is required.</div>
              <div class="error" v-if="!$v.updatedAlbum.name.minLength">
                Album name must have at least {{ $v.updatedAlbum.name.$params.minLength.min }} letters.
              </div>
              <div class="error" v-if="!$v.updatedAlbum.name.maxLength">
                Album name must have at most {{ $v.updatedAlbum.name.$params.maxLength.max }} letters.
              </div>
            </div>
          </div>
          <div class="album-info__panel album-info__description">
            <label class="album-info__panel__label">Description</label>
            <input
              :class="'album-info__panel__input ' + { 'input-error': $v.updatedAlbum.description.$error }"
              name="description"
              v-model.trim="updatedAlbum.description"
              @input="setDescription($event.target.value)"
            />
            <div v-if="errors">
              <div class="error" v-if="!$v.updatedAlbum.description.required">Description is required.</div>
              <div class="error" v-if="!$v.updatedAlbum.description.minLength">
                Description must have at least {{ $v.updatedAlbum.description.$params.minLength.min }} letters.
              </div>
              <div class="error" v-if="!$v.updatedAlbum.description.maxLength">
                Description must have at most {{ $v.updatedAlbum.description.$params.maxLength.max }} letters.
              </div>
            </div>
          </div>
          <div class="album-info__panel album-info__isPrivate">
            <label class="album-info__panel__label">Private Album</label>
            <label
              id="album-is-private__label"
              for="album-is-private"
              v-bind:style="[!updatedAlbum.is_private ? { 'background-color': 'white' } : { color: 'white' }]"
            >
              {{ updatedAlbum.is_private ? '✔' : '✖' }}
            </label>
            <input
              type="checkbox"
              id="album-is-private"
              :class="'album-info__panel__input ' + { 'input-error': $v.updatedAlbum.is_private.$error }"
              name="is_private"
              v-model.trim="updatedAlbum.is_private"
              @input="setIsPrivate($event.target.value)"
            />
            <div v-if="errors">
              <div class="error" v-if="!$v.updatedAlbum.is_private.required">Private status is required.</div>
            </div>
          </div>
          <div class="album-info__panel album-info__controls">
            <input class="album-info__controls__save btn-secondary" type="submit" value="Save changes" />
            <button type="button" class="album-info__controls__cancel btn-secondary" @click="emitHideModal">Cancel</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { minLength, maxLength, required } from 'vuelidate/lib/validators';
import defaultAlbumCover from '../assets/images/album-cover.jpg';
import { UPDATE_ALBUM, CREATE_ALBUM } from '../store/actions.type';

export default {
  name: 'CreateEditAlbumModal',
  data() {
    return {
      defaultAlbumCover: defaultAlbumCover,
      //Vuelidate album data
      updatedAlbum: {
        cover_image: (this.album.cover_image || '') + '',
        cover_image_local_url: '',
        name: (this.album.name || '') + '',
        description: (this.album.description || '') + '',
        is_private: this.album.is_private !== undefined ? this.album.is_private : true,
      },
      //For preventing errors from popping up before submitting
      uiState: 'submit not clicked',
      errors: false,
      empty: true,
    };
  },
  props: {
    hideModal: Function,
    album: Object,
    mode: String,
  },
  //Vuelidate validations for album data
  validations: {
    updatedAlbum: {
      cover_image: { required },
      name: { required, minLength: minLength(4), maxLength: maxLength(70) },
      description: { required, minLength: minLength(4), maxLength: maxLength(200) },
      is_private: { required },
    },
  },
  methods: {
    emitHideModal() {
      this.$emit('hideModal');
    },
    getUserSelectedImage(e) {
      //Todo: Check type of image?
      this.updatedAlbum.cover_image = e.target.files[0];
      this.updatedAlbum.cover_image_local_url = URL.createObjectURL(e.target.files[0]);
      this.$v.updatedAlbum.cover_image.$touch();
    },
    setAlbumName(value) {
      this.updatedAlbum.name = value;
      this.$v.updatedAlbum.name.$touch();
    },
    setDescription(value) {
      this.updatedAlbum.description = value;
      this.$v.updatedAlbum.description.$touch();
    },
    setIsPrivate(value) {
      this.updatedAlbum.is_private = value === 'on' ? true : false;
      this.$v.updatedAlbum.is_private.$touch();
    },
    submitChanges() {
      this.formTouched = !this.$v.updatedAlbum.$anyDirty;
      this.errors = this.$v.updatedAlbum.$anyError;
      this.uiState = 'submit clicked';
      if (this.errors === false && this.formTouched === false) {
        const albumData = {};

        ['id', 'name', 'description', 'is_private', 'cover_image'].forEach((key) => {
          console.log(key, this.updatedAlbum[key], this.$props.album[key]);
          if (key === 'id') return (albumData[key] = this.$props.album[key]);
          if (this.updatedAlbum[key] !== this.$props.album[key]) albumData[key] = this.updatedAlbum[key];
        });

        if (this.$props.mode === 'Edit') this.$store.dispatch(UPDATE_ALBUM, albumData);
        else if (this.$props.mode === 'Create') this.$store.dispatch(CREATE_ALBUM, albumData);

        this.emitHideModal();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

#CreateEditAlbumModal {
  z-index: 1000;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(128, 128, 128, 0.5);

  .modal {
    min-width: 70%;
    max-width: 100%;
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    background-color: white;
    border-radius: 0.5rem;
    overflow: hidden;

    @include respond(small-laptop) {
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

      @include respond(tablet-port) {
        display: block;
      }

      .album-info {
        width: 40%;
        font-size: 2rem;

        @include respond(tablet-port) {
          margin: 0 auto;
          width: 80%;
        }

        &__isPrivate {
          @include respond(tablet-port) {
            display: flex !important;
            justify-content: center !important;
          }

          label {
            @include respond(tablet-port) {
              width: auto;
            }
          }
        }

        &__panel {
          display: inline-block;
          width: 100%;
          margin-bottom: 2rem;

          &__ &-group {
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

      .album-image {
        position: relative;

        @include respond(tablet-port) {
          width: 30rem;
          height: 30rem;
          margin: 0 auto;
        }

        &__img {
          width: 30rem;
          height: 30rem;
          background-size: cover;
          background-clip: padding-box;
          background-position: center center;
          // border-radius: 50%;
        }

        &__edit-img {
          z-index: 1000;
          background-color: $color-tertiary;
        }

        &__edit-img {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          display: none;
          cursor: pointer;
          // border-radius: 50%;

          label {
            top: 50%;
            left: 50%;
            position: absolute;
            transform: translate(-50%, -50%);
            font-size: 5rem;
            user-select: none;
            color: #fff;
            cursor: pointer;
          }

          input[type='file'] {
            display: none;
          }
        }
      }

      .album-image:hover .album-image__edit-img {
        display: block;
        background: rgba(44, 0, 70, 0.9);
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

  #album-is-private__label {
    background-color: $color-tertiary;
    border: 1px solid $color-tertiary;
    color: $color-tertiary;

    display: inline-block;
    border-radius: 0.5rem;
    height: 3.1rem;
    width: 3.1rem;

    text-align: center;
    vertical-align: center;
    margin-left: 1rem;

    user-select: none;
    cursor: pointer;
  }
  #album-is-private {
    display: none;
  }
}
</style>
