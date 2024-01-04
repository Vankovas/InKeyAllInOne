<template>
  <div class="track">
    <div class="track__data">
      <a :href="data" target="_blank"><img src="../assets/images/play.png" alt=""/></a>
    </div>
    <div class="track__name">{{ index }}. {{ name }}</div>
    <div class="track__description">{{ description ? description : 'No description' }}</div>
    <div class="track__rating">
      <img src="../assets/images/rating-filled.png" alt="" />
      <pre> Rating: </pre>
      {{ rating }}
    </div>
    <div class="track__views">
      <img src="../assets/images/views-filled.png" alt="" />
      <pre> Plays: </pre>
      {{ views }}
    </div>
    <div v-if="currentCreator.id && currentUser.id && currentCreator.id === currentUser.id" class="track__settings">
      <button type="button" class="track__settings__edit" @click="handleEdit"><img src="../assets/images/edit.png" alt="" /></button>
      <button type="button" class="track__settings__move" @click="handleMove"><img src="../assets/images/move.png" alt="" /></button>
      <button type="button" class="track__settings__delete" @click="handleDelete"><img src="../assets/images/delete.png" alt="" /></button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  props: ['id', 'index', 'name', 'description', 'rating', 'views', 'data', 'song'],

  data() {
    return {};
  },

  computed: {
    ...mapGetters(['currentUser', 'currentCreator']),
  },

  methods: {
    handleEdit() {
      this.$emit('showEditSongModal', this.$props.song);
    },
    handleMove() {
      this.$emit('showMoveSongModal', this.$props.song);
    },
    handleDelete() {
      this.$emit('showDeleteSongModal', this.$props.song);
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';
@import '../scss/_mixins.scss';

.track {
  padding: 1.5rem 0;
  display: flex;
  align-items: center;
  font-family: inherit;
  font-size: 1.6rem;
  font-weight: 400;
  color: #505050;

  &__data {
    margin-right: 2rem;

    & a > * {
      display: flex;
      align-items: center;
      width: 3.5rem;
    }
  }

  &__name {
    font-weight: 500;
    width: 25rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    @include respond(small-laptop) {
      width: 40%;
    }
  }

  &__description {
    margin: 0 auto 0 5rem;

    @include respond(small-laptop) {
      display: none;
    }
  }

  &__rating {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-right: 2rem;

    @include respond(small-laptop) {
      margin-left: auto;
    }

    & > img {
      width: 2rem;
    }

    & > pre {
      font-family: inherit;
      @include respond(phone) {
        display: none;
      }
    }
  }

  &__views {
    display: flex;
    align-items: center;
    margin-right: 5rem;

    @include respond(tablet-port) {
      margin-right: 3rem;
    }

    & > img {
      width: 2rem;
    }

    & > pre {
      font-family: inherit;
      @include respond(phone) {
        display: none;
      }
    }
  }

  &__settings {
    & > * {
      cursor: pointer;
      background-color: transparent;
      border: none;
      outline: none;
      padding: 0.5rem;
      background-color: #f6edfa;
      border-radius: 0.5rem;
    }

    & > *:not(:last-child) {
      margin-right: 0.8rem;
    }
    &__edit {
      &:hover {
        background-color: darken(#f6edfa, 5);
      }
      & > * {
        width: 2.5rem;
      }
    }
    &__move {
      &:hover {
        background-color: darken(#f6edfa, 5);
      }
      & > * {
        width: 2.5rem;
      }
    }
    &__delete {
      background-color: #ffebee;

      &:hover {
        background-color: darken(#ffebee, 5);
      }
      & > * {
        width: 2.5rem;
      }
    }
  }
}
</style>
