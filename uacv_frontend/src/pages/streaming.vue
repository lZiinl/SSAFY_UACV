<template>
  <v-container>
    <h1>Live Stream</h1>
    <stream-player :stream-url="streamUrl" />
    <!-- 추가: 스트림 시작 버튼 -->
    <v-btn @click="startStream">Start Stream</v-btn>
  </v-container>
</template>

<script>
import StreamPlayer from '@/components/StreamPlayer.vue'
import { mapState, mapActions } from 'vue'

export default {
  name: 'StreamView',
  components: {
    StreamPlayer
  },
  computed: {
    ...mapState('stream', ['streamUrl'])
  },
  methods: {
    // 추가: startStream 액션 매핑
    ...mapActions('stream', ['startStream'])
  }
  // 제거: created 훅에서 자동으로 스트림을 시작하는 부분 제거
}
</script>