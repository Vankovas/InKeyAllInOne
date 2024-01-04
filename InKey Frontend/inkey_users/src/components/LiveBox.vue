<template>
    <div class="container">
        <h3 class="name"><router-link :to="{name: 'live-detail', params: { id: uuid }}">{{artist.firstname}}</router-link></h3>
        <h3 class="timestamp">{{timeSinceStart()}}</h3>
    </div>
</template>

<script>
export default {
    name: 'live-box',
    props: ['artist', 'uuid', 'start'],
    data(){
        return{
            
        }
    },
    methods:{
        timeSinceStart(){
            let now = this.getNowInCorrectFormat();
            let timeElapsed = now - this.start;
            let seconds = (((timeElapsed/1000)|0 )%60)
            let minutes = (((((timeElapsed/1000)|0 )/60)|0)%60)
            let hours = (((timeElapsed/1000)|0 )/3600)|0

            return this.addExtraZeroIfNeeded(hours)+":"+this.addExtraZeroIfNeeded(minutes)+":"+this.addExtraZeroIfNeeded(seconds);
        },
        addExtraZeroIfNeeded(number){
            return (number+"").length>1?number+"":"0"+number
        },
        getNowInCorrectFormat(){
            let now = new Date(Date.now());
            // need to fix backend
            // cause it gives incorrect date time 
            // this is a temporary fix
            // let mins = this.start.getTimezoneOffset();
            // console.log(mins)
            // if(mins == 0){
            //     return now; 
            // }
            return new Date(now);
        }
    }
}
</script>
<style lang="scss" scoped>
    .container{
        width: 100%;
        height: 50px;
        font-size: 2em;
        border-bottom: 2px solid #330d28;
        h3{
            display: inline-block;
        }
        text-align: center;
    }
    .name{
        width: 70%;
    }
    .timestamp{
        width: 30%;
    }
    a{
        color: white!important;
        text-decoration: none!important;
        transition: color 500ms;
    }
    a:hover{
        color: #fffa!important;
    }
</style>