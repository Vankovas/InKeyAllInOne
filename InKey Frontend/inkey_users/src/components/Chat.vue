<template>
  <div id="Chat">
    <div class="message-panel">
      <template v-for="(msgData, index) in this.messages">
        <ChatMessage :key="index" :data="msgData"></ChatMessage>
      </template>
    </div>
    <div class="input-panel">
      <textarea type="text" v-model="message" />
      <div @click="sendMessage"><span>Send</span></div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { uuid } from 'uuidv4';

import ChatMessage from './ChatMessage';

//TODO: Add functionality for anonnymous user
//Generate id with uuidv4 for anon users

export default {
  name: 'Chat',

  components: {
    ChatMessage,
  },

  data() {
    return {
      message: '',
      socket: undefined,
      messages: [],
      uuid: uuid(),
      color: this.getRandomColor(),
    };
  },

  methods: {
    getRandomColor() {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    },

    connectSocket(socket) {
      console.log(socket);
      this.socket = socket;
      this.socket.on('receiveMessage', (res) => {
        const { timestamp, user, message } = res;
        this.receiveMessage(timestamp, user, message);
      });
    },

    sendMessage() {
      const data = {
        timestamp: this.formatTimestamp(),
        user: {
          id: this.currentUser !== undefined && this.currentUser.id !== undefined ? this.currentUser.id : this.uuid,
          username: this.currentUser !== undefined && this.currentUser.username !== undefined ? this.currentUser.username : 'Anon',
          color: this.color,
        },
        message: this.message,
      };

      this.socket.emit('sendMessage', data);
      this.message = '';
    },

    receiveMessage(timestamp, user, message) {
      this.messages.push({ timestamp, user, message });
    },

    formatTimestamp() {
      return this.formatAMPM(new Date(Date.now()));
    },

    formatAMPM(date) {
      let hours = date.getHours();
      let minutes = date.getMinutes();
      let seconds = date.getSeconds();

      const extension = hours >= 12 ? 'PM' : 'AM';

      hours = hours % 12;
      hours = hours ? hours : 12; // the hour '0' should be '12'

      hours = this.format2Digits(hours);
      minutes = this.format2Digits(minutes);
      seconds = this.format2Digits(seconds);

      const formattedTime = `${hours}:${minutes}:${seconds}${extension}`;
      return formattedTime;
    },

    format2Digits(num) {
      if (num < 10) return `0${num}`;
      return num;
    },
  },
  computed: {
    ...mapGetters(['currentUser']),
  },
};
</script>

<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import '../scss/_utilities.scss';

#Chat {
  height: 80vh;
  width: 100%;
  background-color: $color-primary-2;

  .message-panel {
    height: 90%;
  }

  .input-panel {
    height: 10%;
    display: flex;
    border-top: 2px solid $color-primary-1;
    background: $color-primary-3;

    textarea {
      width: 100%;
      height: 100%;
      resize: none;

      border: none;
      background: $color-primary-3;
      padding: 1rem 0 1rem 1rem;
      color: $color-white;

      &:focus {
        outline: none;
      }

      &::-webkit-scrollbar {
        width: 0.7rem;
        background-color: #fff6f7;
      }
      &::-webkit-scrollbar-thumb {
        border-radius: 10px;
        background-color: $color-secondary;
      }
    }

    div {
      height: 50%;
      margin: 0 1rem;
      transform: translate(0, 50%);
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      outline: none;
      border: none;

      span {
        font-family: inherit;
        font-size: 1.7rem;
        padding: 0.5rem 2rem;
        background-color: $color-secondary;
        transition: box-shadow 0.2s;
        color: black;
        font-weight: 500;
        border-radius: 2rem;

        &:hover {
          box-shadow: 0 0 2rem 0 rgba($color-secondary, 0.6);
        }

        &:active {
          color: $color-white;
        }
      }
    }
  }
}
</style>
