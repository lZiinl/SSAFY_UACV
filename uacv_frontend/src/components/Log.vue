<template>
  <h5 class="text-h5 font-weight-bold">LOG</h5>
  <div>
    <ul>
      <li v-for="log in displayedLogs" :key="log.id">
        {{ formatToKST(log.time) }} - {{ log.message }}
      </li>
    </ul>
  </div>
</template>


<script>

import { ref, onMounted, computed } from 'vue';

export default {
  name: "Log",
  setup() {
    const logs = ref([]);
    const socket = ref(null);

    const displayedLogs = computed(() => {
      return logs.value.slice(-2);
    });

    const addLog = (newLog) => {
      logs.value.push(newLog);
    };

    const fetchInitialLogs = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/sound-logs`);
        const data = await response.json();

        logs.value = data.map(log => ({
          id: log.id,
          time: new Date(log.receivedAt).toLocaleString('ko-KR'),
          message: `총 소리 인식 (${log.soundType}로 추정)`,
        }));

      } catch (error) {
        console.error('Error fetching initial logs:', error);
      }
    };

    const formatToKST = (date) => {
      return date.toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
    };

    onMounted(() => {
      fetchInitialLogs();
      socket.value = new WebSocket(`${import.meta.env.VITE_WEBSOCKET_URL}/sound`);
      socket.value.onmessage = (event) => {
        const newLog = JSON.parse(event.data);
        addLog({
          id: newLog.id,
          time: new Date(newLog.receivedAt), // .toLocaleString('ko-KR'),
          message: `총 소리 인식 (${newLog.soundType}로 추정)`,
        });
      };
    });

    return {
      displayedLogs,
      formatToKST,
    };
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 5px;
}
</style>