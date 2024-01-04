<template>
    <div class="container">
        <div class="description">
            <h3 class="name">Artist Name</h3><h3 class="timestamp">Time</h3>
        </div>
        <live-box v-for="(stream, index) in streams" :key="index" 
        :artist="stream.artist" :uuid="stream.uuid" :start="new Date(stream.created_at)"></live-box>
    </div>
</template>
<script>
    import {FETCH_ALL_STREAMS} from '../store/actions.type';
    import LiveBox from '../components/LiveBox.vue';
    export default {
        name: 'live',
        components:{
            LiveBox,
        },
        data(){
            return{
                streams: [],
            }
        },
        beforeRouteEnter(to, from, next) {
            next(vm => vm.$store.dispatch(FETCH_ALL_STREAMS).then(() => {
                vm.streams = vm.$store.getters.allStreams;
            }));
        },
    }
</script>
<style lang="scss" scoped>
    .container{
        overflow-y: auto;
        height: 100%;
    }
    .description{
        width: 100%;
        height: 50px;
        font-size: 2em;
        border-bottom: 2px solid #330d28;
        color: #fffa;
        text-align: center;
        h3{
            display: inline-block;
        }
    }
    .name{
        width: 70%;
    }
    .timestamp{
        width: 30%;
    }
</style>