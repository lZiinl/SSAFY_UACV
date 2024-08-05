import axios from 'axios'

export const stream = {
  namespaced: true,
  state: {
    streamUrl: ''
  },
  mutations: {
    SET_STREAM_URL(state, url) {
      state.streamUrl = url
    }
  },
  actions: {
    async startStream({ commit }) {
      try {
        // 수정: API 엔드포인트와 요청 본문 업데이트
        const response = await axios.post('http://localhost:8080/api/feed/start', {
          inputUrl: 'input',
          outputName: 'test'
        })
        // 수정: 응답에서 streamUrl을 가져와 저장
        commit('SET_STREAM_URL', response.data.streamUrl)
      } catch (error) {
        console.error('Failed to start stream:', error)
      }
    }
  }
}