<template>
  <v-app>
    <Navbar />

    <Appbar />

    <v-main>
      <v-container>
        <div class="d-flex justify-center align-center my-4">
          <h3 class="text-h5 font-weight-bold mr-3">LOG</h3>
        </div>

        <v-data-table :items="filteredItems" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title style="color: #FFFFEF;">기록보기</v-toolbar-title>
              <v-divider inset vertical class="mx-4" />

              <v-menu v-model="menu" max-height="400" :close-on-content-click="false" transition="scale-transition"
                class="custom-menu">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn icon v-bind="attrs" v-on="on" @click="toggleMenu">
                    <v-icon style="color: #FFFFEF;">mdi-filter</v-icon>
                  </v-btn>
                </template>

                <v-list>
                  <v-list-item v-for="option in filterOptions" :key="option" @click="applyFilter(option)">
                    <v-list-item-content>{{ option }}</v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-toolbar>
          </template>
        </v-data-table>

      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Appbar from '@/components/appbar.vue';
import Navbar from '@/components/navbar.vue';

import { useUserStore } from '@/stores/user';

const store = useUserStore()

export default {
  data() {
    return {

      headers: [
        { text: "시간", value: "time" },
        { text: "구분", value: "type" },
        { text: "내용", value: "content" },
      ],
      filterOptions: ["소리인식", "발사기록", "센서인식"],
      items: [
      ],

    };
  },

  computed: {
    filteredItems() {
      if (this.filterOption) {
        return this.items.filter(item => item.type === this.filterOption);
      }
      return this.items;
    },
  },

  methods: {
    async fetchSoundLogs() {
      try {
        const headers = {
          Authorization: `Bearer ${sessionStorage.getItem("token")}`
        }

        const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/sound-logs`, { headers });
        const data = await response.json();

        this.items = data.map(log => ({
          time: new Date(log.receivedAt).toLocaleString('ko-KR'),
          type: "소리인식",
          content: `총 소리 인식 (${log.soundType}로 추정)`,
        }));

      } catch (error) {
        console.error('Error fetching sound logs:', error);
      }
    },
    expandDrawer() {
      this.mini = false;
      this.drawerWidth = 150;
    },
    collapseDrawer() {
      this.mini = true;
      this.drawerWidth = 56;
    },
    logout() {
      this.$router.push("/");
    },
    applyFilter(option) {
      this.filterOption = option;
      this.menu = false;
    },
    toggleMenu() {
      this.menu = !this.menu;
    },
    applyFilter(option) {
      this.filterOption = option;
      this.menu = false;
    },
  },
  mounted() {
    this.fetchSoundLogs();
  },

  components: {
    NavigationItem: {
      props: {
        icon: String,
        title: String,
        to: String,
        mini: Boolean,
      },
      template: `
        <v-list-item :to="to" @click="$emit('click')">
          <v-list-item-icon v-if="icon">
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content v-if="title && !mini">
            <v-list-item-title>{{ title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      `,
    },
  },
};
</script>

<style scoped>
.v-toolbar-title span {
  font-size: 24px;
  font-weight: bold;
  color: #FFFFEF;
}

.v-toolbar {
  background-color: #004d40;
  text-align: center;
}

.v-pagination {
  justify-content: center;
}

.v-menu {
  position: absolute;
  top: 30%;
  left: 85%;
}
</style>
