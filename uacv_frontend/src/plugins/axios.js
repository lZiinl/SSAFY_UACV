import axios from 'axios'

const axiosInstance = axios.create({
  baseURL: 'http://i11c102.p.ssafy.io:8080'  // 여기에 백엔드 서버 주소를 넣으세요
})

export default axiosInstance