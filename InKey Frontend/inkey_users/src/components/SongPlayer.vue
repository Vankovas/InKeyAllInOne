<template>
    <div>
        <audio id="audio" @timeupdate="onTimeUpdateListener($event)" ref="player"></audio>
        <div class="player">
            <div class="play-container">
                <font-awesome-icon class="icon" @click="previousSong()" icon="step-backward"/>
                <font-awesome-icon class="icon" @click="toogle()" :icon="player && !player.paused ? 'pause-circle':'play-circle'"/>
                <font-awesome-icon class="icon" @click="nextSong()" icon="step-forward"/>
            </div>
            <div class="current-time-container">
                {{displayMinSecObj(currentTime)}}
            </div>
            <div class="time-container">
                <input
                    type="range" id="timestamp"
                    @mousedown="userIsClicking=true" 
                    @mouseup="userIsClicking=false"
                    v-model="currentTime" 
                    @change="skipToThisTime($event)"
                    step="1" min="0" :max="duration" class="slider">
            </div>
            <div class="duration-time-container">
                {{displayMinSecObj(duration)}}
            </div>
            <div class="shuffle-container">
                <font-awesome-icon class="icon" :class='shuffle?"enabled-icon":""' @click="toogleShuffle()" icon="random"/>
                <font-awesome-icon class="icon" :class='redo?"enabled-icon":""' @click="toogleRedo()" icon="redo"/>
            </div>
            <div class="volume-container">
                <font-awesome-icon class="icon" @click="mute()" :icon=" !muted ? 'volume-up': 'volume-mute'"/>
                <input 
                    type="range" id="change_vol" 
                    @change="changeVol()" 
                    @wheel="onWheelScrollVolume($event)"
                    step="0.05" min="0" max="1" value="1" class="slider"
                >
            </div>
        </div>
    </div>
</template>
<script>
import { EventBus } from '../common/event-bus.js';

export default {
    name: 'song-player',
    data(){
        return{
            currentTime: 0,
            duration: 0,
            player: undefined,
            isPlaying: false,
            userIsClicking: false, 
            muted: false,
            songs: [],
            songIndex: 0,
            shuffle: false,
            redo: false,
            streaming: false,
            playerPlayPromise: undefined,
        }
    },
    methods: {
        loadSong(id){
            this.songIndex = id;
            this.player.src = this.songs[this.songIndex].data;
        },
        setSongs(songs){
            this.songs = songs;
            this.loadSong(0);
        },
        toogleRedo(){
            this.redo = !this.redo;
        },
        toogleShuffle(){
            this.shuffle = !this.shuffle;
        },
        nextSong(){
            if(!this.streaming && this.songs.length>0){
                if(this.shuffle){
                     this.getRandomSong();
                }else{
                    this.loadSong(this.songIndex < this.songs.length-1 ? this.songIndex+1 : 0);
                }
                this.play();
            }
        },
        previousSong(){
            if(!this.streaming && this.songs.length>0){
                if(this.shuffle){
                    this.getRandomSong();
                }else{
                    this.loadSong(this.songIndex > 0 ? this.songIndex - 1 : this.songs.length-1);
                }
                this.play();
            }
        },
        getRandomSong(){
            let newIndex = this.songIndex
            while(newIndex == this.songIndex){
                newIndex = (Math.random()*this.songs.length | 0);
            }
            this.loadSong(newIndex);
        },
        mute(){
            this.muted = !this.muted;
            this.player.muted = this.muted;
        },
        onWheelScrollVolume(e){
            e.preventDefault();
            let orginalVal = this.player.volume;
            let change = e.deltaY<0 ? 0.05 : -0.05;
            let newVal = orginalVal + change;
            if(newVal > 1){
                newVal = 1;
            }else if(newVal < 0){
                newVal = 0;
            }
            this.player.volume = newVal;
            e.target.value = newVal;
            this.player.muted = false;
            this.muted = false;
        },
        changeVol(){
            this.player.volume=document.getElementById("change_vol").value;
            this.player.muted = false;
            this.muted = false;
        },
        secondsToMinutes(seconds){
            let sec = parseInt(seconds);
            let min = (sec / 60) |0;
            sec = sec % 60;
            return {min: min, sec: sec}
        },
        displayMinSecObj(seconds){
            let obj = this.secondsToMinutes(seconds);
            let min = (""+obj.min).length == 1 ? "0"+obj.min : ""+obj.min;
            let sec = (""+obj.sec).length == 1 ? "0"+obj.sec : ""+obj.sec;
            return min+":"+sec;
        },
        skipToThisTime(){
            let theTime = document.getElementById("timestamp").value;
            this.player.currentTime = theTime;
        },
        onTimeUpdateListener() {
            if(!this.userIsClicking){
                this.player = document.getElementById("audio");
                this.currentTime = this.player.currentTime;
            }
        },
        toogle(){
            if(this.isPlaying) this.pause();
            else this.play();
        },
        play(){
            if(this.streaming || this.songs.length>0){
                this.isPlaying = true;
                this.playerPlayPromise = this.player.play();
            }
        },
        pause(){
            if(this.streaming || this.songs.length>0){
                this.isPlaying = false;
                this.player.pause();
                if (this.playPromise !== undefined) {
                    this.playPromise.then(() => {this.player.pause();})
                }
            }
        }
    },
    mounted(){
        this.player = document.getElementById("audio");
        this.player.onloadedmetadata = () => {
            this.duration = this.player.duration;
            this.currentTime = this.player.currentTime;
        }
        this.player.onended = ()=>{
            if(this.redo){
                this.player.currentTime = 0;
                this.play()
            }else{
                this.nextSong();
            }
        };
        EventBus.$on('set-songs', (e, play=false) => {
            this.setSongs(e);
            if(play){
                this.play();
            }
        });
        EventBus.$on('add-song', (e, play=false) => {
            this.songs = this.songs.filter(element => !element.singleTime);
            this.songs.push(e);
            if(play){
                this.loadSong(this.songs.length-1);
                this.play();
            }
        });
        EventBus.$on('stream-start', () => {
            this.songs = [];
            this.songIndex = 0;
            this.streaming = true;
            EventBus.$emit('player-received', this.player);
        });
        EventBus.$on('stream-end', () => {
            this.streaming = false;
            this.duration = 0;
        });
        EventBus.$on('set-duration', (time) => {
            this.duration = time;
        });
        EventBus.$on('remove-song', ()=>{
            if(this.songs.length > 0){
                this.pause();
                this.songs.splice(this.songIndex, 1);
                this.songIndex = this.songIndex>0 ? this.songIndex-1 : 0;
                this.duration = 0;
                this.currentTime = 0;
                if(this.songs.length>0){
                    this.player.src = this.songs[this.songIndex];
                }else{
                    this.player.src = "";
                }
            }
        });
    },
}
</script>
<style lang="scss" scoped>
@import "../scss/_variables.scss";
@import "../scss/_utilities.scss";
@import "../scss/_mixins.scss";

$icon_width: 30px;
$icon_margin: 10px;
$icon_color: white;

.player {
    user-select: none;
    padding-top: 1rem;
    position: fixed;
    bottom: 0;
    height: 8rem;
    font-size: 30px;
    width: 100%;
    background: $color-primary-3;
    z-index: 1000;
    color: $icon_color;
    display: flex;
    align-items: center;

    div {
        display: inline-table;
        text-align: center;
    }
}

.play-container {
    display: flex !important;
    align-items: center;
    margin-left: 2.5%;
    width: 10%;

    .icon {
        margin-right: calc(33% - #{$icon_width});
    }

    @include respond(tablet-port) {
        &>*:first-child,
        &>*:last-child {
            display: none;
        }
        font-size: 8rem;
    }
}

.current-time-container {
    display: flex !important;
    align-items: center;
    justify-content: center;
    width: 10%;

    @include respond(tablet-port) {
        font-size: 2.5rem;
    }
}

.time-container {
    display: flex !important;
    align-items: center;

    input {
        width: 100%;
    }

    width: 40%;

    @include respond(tablet-port) {
        font-size: 2.5rem;
    }
}

.duration-time-container {
    display: flex !important;
    align-items: center;
    justify-content: center;
    width: 10%;

    @include respond(tablet-port) {
        font-size: 2.5rem;
    }
}

.shuffle-container {
    display: flex !important;
    align-items: center;
    width: 10%;

    @include respond(tablet-port) {
        font-size: 2.5rem;
    }

    .icon {
        margin-right: calc(50% - #{$icon_width});
    }
}

.volume-container {
    display: flex !important;
    align-items: center;
    width: 15%;

    input {
        width: calc(100% - #{$icon_width} - (#{$icon_margin} * 2));
    }

    @include respond(tablet-port) {
        font-size: 2.5rem;
    }
}

.icon {
    width: $icon_width;
    margin-right: $icon_margin;
    cursor: pointer;
    color: $color-secondary;
}

.icon:hover {
    color: white;
}

.enabled-icon {
    color: $color-primary-1 !important;
}

.enabled-icon:hover {
    color: $color-primary-2 !important;
}

input[type=range] {
    -webkit-appearance: none;
    cursor: pointer;
}

input[type=range]::-webkit-slider-runnable-track {
    width: 300px;
    height: 5px;
    background: white;
    border: none;
}

input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    border: none;
    height: 16px;
    width: 16px;
    border-radius: 50%;
    background: $color-secondary;
    margin-top: -4px;
}

input[type=range]:focus {
    outline: none;
}

</style>