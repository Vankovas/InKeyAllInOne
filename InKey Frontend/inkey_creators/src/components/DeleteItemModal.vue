<template>
  <div id="DeleteItemModal">
    <div class="modal">
      <div class="modal-header">
        <h1 class="modal-header__title">Confirm {{ this.$props.type }} deletion</h1>
      </div>
      <div v-if="!confirmed" class="modal-content">
        <div class="modal-content-info">Are you sure you want to delete the {{ this.$props.type }}?</div>
        <div class="modal-content-controls">
          <input class="modal-content-controls__cancel btn-secondary" type="submit" @click="deleteItem" value="Yes" />
          <button style="margin: 0 0 0 2rem" type="button" class="modal-content-controls__save btn-secondary" @click="emitHideModal">No</button>
        </div>
      </div>

      <div v-else class="modal-content">
        <div class="modal-content-info">
          {{ `The ${this.$props.type} was successfully deleted!` }}
        </div>
        <div class="modal-content-controls">
          <button type="button" class="modal-content-controls__cancel btn-secondary" @click="emitHideModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { DELETE_ALBUM, DELETE_SONG } from '../store/actions.type';
export default {
  name: 'DeleteItemModal',
  data() {
    return {
      hideModal: Function,
      confirmed: false,
    };
  },
  props: {
    item: Object,
    type: String,
  },
  methods: {
    emitHideModal() {
      this.$emit('hideModal');
    },
    deleteItem() {
      console.log(this.$props.type);
      if (!['album', 'song'].includes(this.$props.type)) throw console.error('Unknown Type (SRC: DeleteItemModal: deleteItem())');

      let action = null;
      if (this.$props.type === 'album') action = DELETE_ALBUM;
      else if (this.$props.type === 'song') action = DELETE_SONG;

      console.log(action, this.$props.item.id);
      this.$store.dispatch(action, this.$props.item.id);
      this.confirmed = true;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

#DeleteItemModal {
  z-index: 1000;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(128, 128, 128, 0.5);

  .modal {
    width: 70rem;
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    @include respond(tablet-port) {
      width: 80%;
    }

    @include respond(phone) {
      width: 90%;
    }

    background-color: white;
    border-radius: 0.5rem;
    overflow: hidden;

    &-header {
      background-color: $color-tertiary;
      color: $color-white;
      padding: 3rem;

      &__title {
        font-size: 2.5rem;
      }
    }

    &-content {
      width: 100%;
      margin: 0 auto;
      padding: 2rem 0;

      * {
        display: block;
      }

      &-info {
        width: 100%;
        font-size: 2rem;

        text-align: center;
        font-size: 3rem;
      }

      &-controls {
        width: 50%;
        display: flex;
        justify-content: space-evenly;
        margin: 2rem auto;

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
</style>
