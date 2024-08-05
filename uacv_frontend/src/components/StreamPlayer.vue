<template>
    <div>
      <video ref="videoPlayer" controls autoplay></video>
    </div>
  </template>
  
  <script>
  import Hls from 'hls.js'
  
  export default {
    name: 'StreamPlayer',
    props: {
      streamUrl: {
        type: String,
        required: true
      }
    },
    watch: {
      streamUrl: {
        immediate: true,
        handler: 'loadStream'
      }
    },
    methods: {
      loadStream() {
        if (Hls.isSupported() && this.streamUrl) {
          const video = this.$refs.videoPlayer
          const hls = new Hls()
          hls.loadSource(this.streamUrl)
          hls.attachMedia(video)
          // 추가: MANIFEST_PARSED 이벤트 리스너 추가
          hls.on(Hls.Events.MANIFEST_PARSED, () => {
            video.play()
          })
        }
      }
    }
  }
  </script>