<!-- src/pages/streaming.vue -->
<template>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>Camera 1</v-card-title>
            <v-card-text>
              <VideoPlayer :options="playerOptions1" />
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>Camera 2</v-card-title>
            <v-card-text>
              <VideoPlayer :options="playerOptions2" />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row class="mt-4">
        <v-col cols="12" sm="6" md="3">
          <v-btn block color="primary" @click="startStreams">Start Streams</v-btn>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-btn block color="error" @click="stopStreams">Stop Streams</v-btn>
        </v-col>
      </v-row>
      <v-snackbar v-model="snackbar" :color="snackbarColor" top>
        {{ snackbarText }}
      </v-snackbar>
    </v-container>
  </template>
  
  <script>
  import VideoPlayer from '@/components/VideoPlayer.vue'
  import axios from 'axios'
  
  export default {
    name: 'Streaming',
    components: {
      VideoPlayer
    },
    data() {
      return {
        playerOptions1: {
          autoplay: true,
          controls: true,
          sources: [{ 
            src: '/api/streams/camera1/playlist.m3u8', 
            type: 'application/x-mpegURL' 
          }]
        },
        playerOptions2: {
          autoplay: true,
          controls: true,
          sources: [{ 
            src: '/api/streams/camera2/playlist.m3u8', 
            type: 'application/x-mpegURL' 
          }]
        },
        snackbar: false,
        snackbarText: '',
        snackbarColor: 'info'
      }
    },
    methods: {
      async startStreams() {
        try {
          await axios.post('/api/streams/start', {
            camera1: 'rtsp://192.168.100.251:5000/cam1',
            camera2: 'rtsp://192.168.100.251:5001/cam2'
          })
          this.showSnackbar('Streams started successfully', 'success')
        } catch (error) {
          this.showSnackbar('Failed to start streams', 'error')
        }
      },
      async stopStreams() {
        try {
          await axios.post('/api/streams/stop')
          this.showSnackbar('Streams stopped successfully', 'success')
        } catch (error) {
          this.showSnackbar('Failed to stop streams', 'error')
        }
      },
      showSnackbar(text, color) {
        this.snackbarText = text
        this.snackbarColor = color
        this.snackbar = true
      }
    }
  }
  </script>