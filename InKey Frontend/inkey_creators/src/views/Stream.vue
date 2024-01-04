<template>
  <div id="Stream">

    <div v-if="!streamingInProgress" style="display:flex; justify-content: center">
      <button class="btn-secondary" style="padding:1rem 2rem; font-size:1.9rem;"
        @click="createStream"
        >Start Stream</button>
    </div>
    <template v-else>
      <button class="btn-secondary" style="padding:1rem 2rem; font-size:1.9rem;"
        @click="destroyStream"
        >Stop Stream</button>
      <div class="stream-selector">
        <div v-bind:class="{ active: this.isMicrophone }" class="stream-selector__mic" @click="this.setMicrophoneView">Microphone</div>
        <div v-bind:class="{ active: !this.isMicrophone }" class="stream-selector__song" @click="this.setSongView">Audio File</div>
      </div>

      <div v-if="isMicrophone" class="microphone">
        <h1 class="microphone__heading">Stream your talent straight from your microphone to your fans' ears!</h1>
        <div class="btn-record" v-bind:class="{ 'btn-stop': this.microphoneTimerInterval !== undefined }" @click="startStopRecording()">
          {{ this.usesMic ? 'Stop' : 'Record' }}
        </div>
        <div v-if="microphoneTimerInterval !== undefined" div id="outerContainer">
          <!-- https://www.kirupa.com/animations/creating_pulsing_circle_animation.htm -->
          <div id="container">
            <div class="item">
              <h2 class="microphone__timer">{{ this.seconds2time(this.microphoneTimer) }}</h2>
            </div>
            <template>
              <div class="circle" style="animation-delay: 0s"></div>
              <div class="circle" style="animation-delay: 1s"></div>
              <div class="circle" style="animation-delay: 2s"></div>
              <div class="circle" style="animation-delay: 3s"></div>
            </template>
          </div>
        </div>
      </div>

      <div v-else class="song">
        <h1 class="song-heading">Stream your favorite songs to your fans!</h1>
        <div class="song-heding-upload">
          <label class="btn-record" for="song-heding-upload__btn">Set Audio File</label>
          <input type="file" id="song-heding-upload__btn" @change="getStreamAudioData" />
        </div>
      </div>

      <audio
        crossOrigin="anonymous"
        style="margin-top:100px"
        v-bind:class="{ hidden: this.isMicrophone || (!this.isMicrophone && !audioIsSetup) }"
        id="hidden_player"
        controls
      ></audio>
      
    </template>
  </div>
</template>
<script>
import io from 'socket.io-client';
import { SOCKET_URL } from '../common/config';
import { CREATE_STREAM, DELETE_STREAM } from '../store/actions.type';
import { mapGetters } from 'vuex';

export default {
  name: 'Stream',
  data() {
    return {
      stream: undefined,
      isLoading: false,
      socket: undefined,
      audio: undefined,
      chunks: [],
      micStream: undefined,
      playerStream: undefined,
      usesMic: false,
      interval: undefined,
      sendingTime: 1000,

      //Views
      isMicrophone: true,
      microphoneTimer: 0,
      microphoneTimerInterval: undefined,

      //Stream Audio Data
      streamAudioData: null,
      audioIsSetup: false,

      streamingInProgress: false,
    };
  },

  methods: {
    async createStream(){
      await this.startStreaming();
      this.streamingInProgress = true;
    },
    async destroyStream(){
      this.socket.emit('disconnect');
      await this.$store.dispatch(DELETE_STREAM);
      if (this.interval) {
        clearInterval(this.interval);
      }
      this.streamingInProgress = false;
    },




    getStreamAudioData(e) {
      this.streamAudioData = URL.createObjectURL(e.target.files[0]);
      this.setupStreamSong(this.streamAudioData);
      this.audioIsSetup = true;
    },

    setMicrophoneView() {
      this.isMicrophone = true;
    },

    setSongView() {
      this.isMicrophone = false;
      if (this.usesMic) this.startStopRecording();
    },

    seconds2time(inputSecs) {
      const hours = Math.floor(inputSecs / 3600);
      let minutes = Math.floor((inputSecs - hours * 3600) / 60);
      const seconds = inputSecs - hours * 3600 - minutes * 60;
      let time = '';

      if (hours != 0) {
        time = hours + ':';
      }
      if (minutes != 0 || time !== '') {
        minutes = minutes < 10 && time !== '' ? '0' + minutes : String(minutes);
        time += minutes + ':';
      }
      if (time === '') {
        time = seconds + 's';
      } else {
        time += seconds < 10 ? '0' + seconds : String(seconds);
      }
      return time;
    },

    startMicrophoneCountdown() {
      this.microphoneTimerInterval = setInterval(() => this.microphoneTimer++, 1000);
    },

    stopMicrophoneCountdown() {
      if (this.microphoneTimerInterval === undefined) return;

      clearInterval(this.microphoneTimerInterval);
      this.microphoneTimerInterval = undefined;
      this.microphoneTimer = 0;
    },

    startStreaming() {
      this.isLoading = true;
      this.stream = this.getStream;
      return this.$store.dispatch(CREATE_STREAM).then(() => {
        this.stream = this.getStream;
        this.isLoading = false;
        this.setupStream();
      });
    },

    startStopRecording() {
      this.usesMic = !this.usesMic;
      if (this.usesMic) {
        if (this.micStream.state !== 'recording') {
          this.startMicrophoneCountdown();
          this.micStream.start();
        }
      } else {
        if (this.micStream.state !== 'inactive') {
          this.stopMicrophoneCountdown();
          this.micStream.stop();
        }
      }
    },

    streamToSocket() {
      if (this.usesMic && this.micStream.state == 'recording') {
        this.micStream.requestData();
      }

      if (!this.usesMic && this.playerStream && this.playerStream.state == 'recording') {
        this.playerStream.requestData();
      }

      if (this.chunks.length > 0) {
        let blob = new Blob(this.chunks, { type: 'audio/ogg; codecs=opus' });
        console.log(blob);
        this.socket.emit('stream', blob);
        this.chunks = [];
      }
    },

    setupStreamSong(URL) {
      this.audio = document.getElementById('hidden_player');
      this.audio.src = URL;
      const stream = this.audio.captureStream();
      this.playerStream = new MediaRecorder(stream);
      this.audio.onplay = () => {
        this.playerStream.ondataavailable = (e) => {
          this.chunks.push(e.data);
        };
        if (this.playerStream.state !== 'recording') {
          this.playerStream.start();
        }
      };
      this.audio.onend = () => {
        if (this.playerStream.state !== 'inactive') {
          this.playerStream.stop();
        }
      };
      this.audio.onseeking = () => {
        if (this.playerStream.state !== 'inactive') {
          this.playerStream.stop();
        }
      };
    },

    setupStream() {
      this.socket = io(SOCKET_URL);
      this.socket.emit('enter', this.stream.uuid);
      let constraints = { audio: true };
      navigator.mediaDevices.getUserMedia(constraints).then((mediaStream) => {
        this.micStream = new MediaRecorder(mediaStream);
        this.micStream.ondataavailable = (e) => {
          this.chunks.push(e.data);
          if(this.micStream.state==="recording"){
            this.micStream.stop();
          }
        };
        this.micStream.onstop = () => {
          if(this.usesMic){
            this.micStream.start();
          }
        }
      });
      this.interval = setInterval(() => {
        this.streamToSocket();
      }, this.sendingTime);
    },
  },

  beforeDestroy() {
    this.socket.emit('disconnect');
    this.$store.dispatch(DELETE_STREAM);
    if (this.interval) {
      clearInterval(this.interval);
    }
  },
  beforeRouteLeave(to, from, next){
    this.socket.emit('disconnect');
    this.$store.dispatch(DELETE_STREAM);
    if (this.interval) {
      clearInterval(this.interval);
    }
    next();
  },
  computed: {
    ...mapGetters(['getStream']),
  },
};
</script>
<style lang="scss" scoped>
@import '../scss/_variables.scss';
@import "../scss/_utilities.scss";

@keyframes scaleIn {
  from {
    transform: scale(0.5, 0.5);
    opacity: 0.5;
  }
  to {
    transform: scale(2.5, 2.5);
    opacity: 0;
  }
}

h1 {
  text-align: center;
}

#Stream {
  height: 48vh;
  overflow: hidden;

  audio {
    width: 100%;
  }
}

.stream-selector {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;

  & > * {
    display: block;
    cursor: pointer;
    outline: none;
    white-space: nowrap;
    background-color: transparent;

    transition: all 0.2s;

    padding: 0.5rem 2rem;
    font-size: 2rem;

    border-top: 1px solid $color-primary;
    border-bottom: 1px solid $color-primary;
    color: $color-primary;
  }

  &__mic {
    border-left: 1px solid $color-primary;
  }

  &__song {
    border-right: 1px solid $color-primary;
  }

  .active {
    color: $color-white;
    background-color: $color-primary;
  }
}

.btn-record {
  display: block;
  cursor: pointer;
  outline: none;
  white-space: nowrap;
  border-radius: 0.5rem;
  background-color: transparent;
  border: 1px solid $color-primary;
  color: $color-primary;
  transition: all 0.2s;

  padding: 0.5rem 2rem;
  font-size: 2rem;
  margin: 2rem auto 0 auto;
  width: max-content;

  &:hover {
    background-color: $color-primary;
    color: $color-white;
  }

  &:active {
    transform: translateY(2px);
  }
}

.btn-stop {
  border: 1px solid $color-primary;
  background-color: $color-primary;
  color: $color-white;

  &:hover {
    background-color: $color-white;
    color: $color-primary;
  }
}

#container {
  width: 30vh;
  height: 30vh;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  overflow: hidden;
  position: relative;

  .circle {
    border-radius: 50%;
    background-color: $color-primary;
    width: 10vh;
    height: 10vh;
    position: absolute;
    opacity: 0;
    animation: scaleIn 4s infinite cubic-bezier(0.36, 0.11, 0.89, 0.32);
  }

  .item {
    z-index: 10;
    font-size: 1.75rem;
    color: white;
  }

  .item img {
    width: 150px;
  }
}

.hidden {
  visibility: hidden;
}

#song-heding-upload__btn {
  display: none;
}
</style>
