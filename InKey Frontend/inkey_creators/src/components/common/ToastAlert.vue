//context.dispatch(CREATE_ALERT, { status: 'success || error || warning || info', message: 'YOUR MESSAGE HERE' });

<template>
  <div id="ToastAlert" :class="'toast-alert-' + this.$props.alert.status + ' toast-alert-' + this.$props.alert.uuid">
    <div class="toast-alert-content">
      <p class="toast-alert-content-status">{{ this.getFormattedStatus() }}</p>
      <p class="toast-alert-content-message">{{ this.$props.alert.message }}</p>
      <span class="toast-alert-content-closebtn" @click="this.removeToastAlert">&times;</span>
    </div>
  </div>
</template>

<script>
import { REMOVE_ALERT } from '../../store/actions.type';
export default {
  name: 'ToastAlert',
  mounted() {
    this.startClosingTimeout();
  },
  beforeDestroy() {
    clearTimeout(this.closeTimeout);
    clearTimeout(this.animationTimeout);
  },
  props: {
    alert: Object,
  },
  data() {
    return {
      closeTimeout: null,
      animationTimeout: null,
    };
  },
  methods: {
    getFormattedStatus() {
      return this.makeOnlyFirstCharCapital(this.$props.alert.status);
    },

    startClosingTimeout() {
      const timer = setTimeout(() => {
        this.removeToastAlert();
      }, 10 * 1000);
      this.closeTimeout = timer;
    },

    removeToastAlert() {
      //Clear auto close timer to prevent it trying to fire when the user has closed the alert before the auto-closing function.
      clearTimeout(this.closeTimeout);

      //Remove after the animation has finished. (600 ms)
      document.querySelector(`.toast-alert-${this.$props.alert.uuid}`).classList.toggle('zero-opacity');

      const timer = setTimeout(() => {
        this.$store.dispatch(REMOVE_ALERT, this.$props.alert.uuid);
      }, 0.6 * 1000);
      this.animationTimeout = timer;
    },

    makeOnlyFirstCharCapital(str) {
      return str[0].toUpperCase() + str.slice(1).toLowerCase();
    },
  },
};
</script>

<style lang="scss" scoped>
@import '../../scss/_variables.scss';
@import '../../scss/_utilities.scss';

#ToastAlert {
  padding: 1rem;
  opacity: 1;
  transition: opacity 0.6s;

  .toast-alert-content {
    width: 80%;

    & * {
      display: inline;
      font-size: 1.5rem;
      color: white;
      line-height: 1.5rem;
    }

    &-status {
      margin: 0 2rem 0 23rem;
      font-weight: bold;
    }

    &-closebtn {
      font-weight: bold;
      float: right;
      font-size: 2rem;
      cursor: pointer;
      transition: 0.3s;

      &:hover {
        color: black;
      }
    }
  }
}

.toast-alert-success {
  background-color: $color-success;
}

.toast-alert-error {
  background-color: $color-error;
}

.toast-alert-warning {
  background-color: $color-warning;
}

.toast-alert-info {
  background-color: $color-info;
}

.zero-opacity {
  opacity: 0 !important;
}
</style>
