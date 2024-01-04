<template>
  <div id="LiveDetails">
    <Chat ref="chat" :socket="this.socket"></Chat>
  </div>
</template>

<script>
import io from 'socket.io-client';
import { EventBus } from '../common/event-bus';
import { SOCKET_URL } from '../common/config';
import Chat from '../components/Chat';

export default {
  name: 'LiveDetails',

  components: {
    Chat,
  },
  watch: {
    $route(){
       this.id = this.$route.params.id;
       this.setUp();
    }
  },
  data() {
    return {
      socket: undefined,
      id: this.$route.params.id,
      isListening: false,
      queue: [],
      sourceBuffer: null,
      mediaSource: null,
      player: null,
      interval: undefined,
    };
  },
  mounted(){
    this.setUp();
  },
  methods: {
    setUp(){
      this.socket = io(SOCKET_URL);
      // here instead of "1" should be the uuid of the stream
      this.socket.emit('enter', this.id);
      this.socket.on('stream', (arrayBuffer) => {
        let blob = new Uint8Array(arrayBuffer);
        this.queue.push(blob);
        this.appendToSourceBuffer();
        console.log(blob);
      });
      this.$refs['chat'].connectSocket(this.socket);
      EventBus.$on('player-received', (player) => {
        this.mediaSource = new MediaSource();
        this.mediaSource.addEventListener('sourceopen', () => {
          this.sourceBuffer = this.mediaSource.addSourceBuffer('audio/webm;codecs=opus');
          this.sourceBuffer.mode = 'sequence';
          this.mediaSource.duration = 0;
          this.sourceBuffer.addEventListener('updateend', () => {
            EventBus.$emit('set-duration', this.player.duration);
            console.log(this.mediaSource.readyState);
            this.appendToSourceBuffer();
          });
        });
        if (!this.interval) {
          this.interval = setInterval(() => {
            this.appendToSourceBuffer();
          }, 1000);
        }
        this.player = player;
        this.player.src = URL.createObjectURL(this.mediaSource);
      });
      EventBus.$emit('stream-start');
    },
    concat(arrays) {
      // sum of individual array lengths
      let totalLength = arrays.reduce((acc, value) => acc + value.length, 0);
      if (!arrays.length) return null;
      let result = new Uint8Array(totalLength);
      // for each array - copy it over result
      // next array is copied right after the previous one
      let length = 0;
      for (let array of arrays) {
        result.set(array, length);
        length += array.length;
      }

      return result;
    },

    appendToSourceBuffer() {
      if (this.mediaSource.readyState === 'open' && this.sourceBuffer && this.sourceBuffer.updating === false) {
        if (this.queue.length != 0) {
          let full = this.concat(this.queue);
          this.sourceBuffer.appendBuffer(full);
          console.log(this.queue);
          this.queue = [];
        }
      }

      // Limit the total buffer size to 20 minutes
      // This way we don't run out of RAM
      if (this.player.buffered.length && this.player.buffered.end(0) - this.player.buffered.start(0) > 1200) {
        this.sourceBuffer.remove(0, this.player.buffered.end(0) - 1200);
      }
    },

    destroySocket() {
      EventBus.$emit('stream-end');
      clearInterval(this.interval);
      this.socket.emit('disconnect');
      this.socket.disconnect();
      this.$refs.chat.messages = [];
    },
  },

  beforeRouteLeave(to, from, next) {
    this.destroySocket();

    next();
  },

  beforeDestroy() {
    this.destroySocket();
  },
};
</script>

<style lang="scss" scoped></style>
