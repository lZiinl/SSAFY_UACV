<!-- src/components/VideoPlayer.vue -->
<template>
    <div class="video-player">
      <video ref="videoPlayer" class="video-js vjs-default-skin"></video>
    </div>
  </template>
  
  <script>
  import videojs from 'video.js'
  import 'video.js/dist/video-js.css'
  import '@videojs/http-streaming'
  
  export default {
    name: 'VideoPlayer',
    props: {
      options: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        player: null
      }
    },
    mounted() {
      this.player = videojs(this.$refs.videoPlayer, this.options, () => {
        this.player.log('Player is ready')
      })
    },
    beforeDestroy() {
      if (this.player) {
        this.player.dispose()
      }
    }
  }
  </script>
  
  <style scoped>
  .video-player {
    width: 100%;
    aspect-ratio: 16 / 9;
  }
  </style>