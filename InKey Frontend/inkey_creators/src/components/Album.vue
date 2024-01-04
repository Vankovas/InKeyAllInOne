<template>
  <div>
    <div class="album" @click="expand" :class="[{ empty_album: !mappedSongs[id] || mappedSongs[id].length < 1 }, { active: expandAlbum }]">
      <div class="album__cover-img"><img :src="cover_image" alt="Cover" /></div>
      <div class="album__name">{{ name }}</div>
      <div class="album__description">{{ description ? description : 'No description' }}</div>
      <div class="album__is-private">{{ is_private ? 'Private' : 'Public' }}</div>
      <div v-if="currentCreator.id && currentUser.id && currentCreator.id === currentUser.id" class="album__settings">
        <button type="button" class="album__settings__btn" v-click-outside="hide" @click="handleAlbumsSettingsDropdown">
          <img src="../assets/images/settings-albums.png" alt="" />
        </button>
        <div class="album__settings__dropdown" v-if="openDropdown">
          <a class="album__settings__dropdown__edit" @click="editAlbum()">Edit</a>
          <a class="album__settings__dropdown__change" @click="changeVisibilityAlbum()">{{ is_private ? 'Make Public' : 'Make Private' }}</a>
          <a class="album__settings__dropdown__delete" @click="deleteAlbum()">Remove</a>
        </div>
      </div>
      <div class="album__expand">
        <div type="button" class="album__expand__btn">
          <img
            :class="{ stop_rotation: !mappedSongs[id] || mappedSongs[id].length < 1 }"
            :style="{ transform: 'rotate(' + (this.expandAlbum ? '180' : '0') + 'deg)' }"
            src="../assets/images/expand-albums.png"
          />
        </div>
      </div>
    </div>
    <div class="content" v-if="expandAlbum">
      <div v-for="(track, index) in mappedSongs[id]" :key="track.id">
        <Track
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
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { FETCH_ALL_ALBUM_SONGS, UPDATE_ALBUM } from '../store/actions.type';
import Track from './Track';

export default {
  props: ['id', 'name', 'description', 'is_private', 'cover_image', 'album'],

  data() {
    return {
      openDropdown: false,
      expandAlbum: false,
    };
  },

  created() {
    this.$store.dispatch(FETCH_ALL_ALBUM_SONGS, this.$props.id);
  },

  methods: {
    handleAlbumsSettingsDropdown() {
      this.openDropdown = true;
    },
    editAlbum() {
      this.$emit('showEditAlbumModal', this.$props.album);
    },
    changeVisibilityAlbum() {
      this.$store.dispatch(UPDATE_ALBUM, { id: this.$props.album.id, is_private: !this.$props.album.is_private });
    },
    deleteAlbum() {
      this.$emit('showDeleteAlbumModal', this.$props.album);
    },
    hide() {
      this.openDropdown = false;
    },
    expand(e) {
      if (
        e.target.tagName != 'IMG' &&
        e.target.className != 'album__settings__btn' &&
        event.target.className != 'album__settings__dropdown__edit' &&
        event.target.className != 'album__settings__dropdown__change' &&
        event.target.className != 'album__settings__dropdown__delete'
      ) {
        this.expandAlbum = !this.expandAlbum;
      }
    },
    showEditSongModal(song) {
      this.$emit('showEditSongModal', song);
    },
    showDeleteSongModal(song) {
      this.$emit('showDeleteSongModal', song);
    },
    showMoveSongModal(song) {
      this.$emit('showMoveSongModal', song);
    },
  },

  directives: {
    clickOutside: {
      bind: function(el, binding, vnode) {
        el.clickOutsideEvent = function(event) {
          // here I check that click was outside the el and his childrens
          if (!(el == event.target || el.contains(event.target)) && event.target.text != 'Albums') {
            // and if it did, call method provided in attribute value
            vnode.context[binding.expression](event);
          }
        };
        document.body.addEventListener('click', el.clickOutsideEvent);
      },
      unbind: function(el) {
        document.body.removeEventListener('click', el.clickOutsideEvent);
      },
    },
  },

  computed: {
    ...mapGetters(['mappedSongs', 'currentUser', 'currentCreator']),
  },

  components: {
    Track,
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

.content {
  font-size: 1.7rem;
  transition: max-height 0.2s ease-out;
  padding: 0 10rem;

  @include respond(small-laptop) {
    padding: 0 1rem;
  }

  & > * {
    &:not(:last-child) {
      border-bottom: 1px solid #ddd;
    }
  }
}
.album {
  padding-right: 2rem;
  display: flex;
  align-items: center;
  font-family: inherit;
  font-size: 1.5rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  background-color: #fff6f7;
  border-radius: 0.2rem;
  cursor: pointer;

  &:hover {
    background-color: darken($color: #fff6f7, $amount: 2);
  }

  &__cover-img {
    margin-right: 2rem;
    display: flex;
    align-items: center;

    & > * {
      width: 10rem;
      height: 10rem;
      border-radius: 0.2rem;
    }
  }

  &__name {
    flex: 1;
    margin-right: 2rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    font-weight: 600;

    @include respond(laptop) {
      flex: 2;
    }
  }

  &__description {
    flex: 3;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    display: inline-block;

    @include respond(laptop) {
      flex: 2;
    }
    @include respond(tablet-land) {
      display: none;
    }
  }

  &__is-private {
    margin: 0 3rem 0 5rem;
    font-weight: 600;
    text-align: left;
  }

  &__settings {
    display: flex;
    align-items: center;
    position: relative;

    &__btn {
      cursor: pointer;
      background-color: transparent;
      border: none;
      outline: none;
      padding: 2rem;

      & > * {
        width: 2.5rem;
      }
    }

    &__dropdown {
      position: absolute;
      top: 3rem;
      left: -5rem;
      width: 15rem;
      background-color: #fff6f7;
      overflow: auto;
      box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
      border-radius: 0.3rem;
      z-index: 1;

      & > *:not(:last-child) {
        border-bottom: 1px solid #f1f1f1;
      }

      & a {
        cursor: pointer;
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        font-family: inherit;
        font-size: 1.5rem;
        font-weight: 500;

        &:hover {
          background-color: rgba($color: $color-primary, $alpha: 0.3);
        }
      }
    }
  }

  &__expand {
    display: flex;
    align-items: center;
    margin-left: 2rem;

    &__btn {
      background-color: transparent;
      border: none;
      outline: none;
      & > * {
        width: 2rem;
      }
    }
  }
}

.empty_album {
  background-color: #fdfdfd !important;
  cursor: default;
}

.stop_rotation {
  transform: none !important;
}

.active {
  background-color: darken($color: #fff6f7, $amount: 3);
}
</style>
