<template>
  <div class="audio-player">
    <audio :src="url" :preload="preload" ref="audio" @play="onPlay" @pause="onPause"
           @loadedmetadata="onLoadedmetadata" @timeupdate="onTimeUpdate"></audio>
    <div>
      <span><i @click="playOrPause" :class="iconClass"></i></span>
      <span>{{ remainingTime+"″" }}</span>
<!--      <el-tag></el-tag>-->
    </div>
  </div>
</template>

<script>
// import {ElTag} from 'element-plus';

export default {
  name: "AudioPlayer",
  components: {},
  props: {
    url: {
      type: String,
      default: 'https://files.catbox.moe/tv2j3t.mp3'
    },
    preload: {
      type: String,
      default: 'metadata'
    },
  },
  data() {
    return {
      playing: false,
      c: 0,
      duration: 0
    }
  },
  methods: {
    playOrPause() {
      if (this.playing) {
        this.$refs.audio.pause()
      } else {
        const audios = document.getElementsByTagName('audio');
        [...audios].forEach((item) => {
          if (item !== this.$refs.audio) {
            // 重置其他播放器状态
            item.pause()
            item.currentTime = 0
            // const temp = item.src
            // item.src = ''
            // item.src = temp
          }
        })
        this.$refs.audio.play()
      }


    },
    onPlay() {
      this.playing = true
    },
    onPause() {
      this.playing = false
    },
    onLoadedmetadata(data) {
      this.duration = data.target.duration
    },
    onTimeUpdate(data) {
      this.c = data.target.currentTime
    }
  },
  computed: {
    iconClass() {
      return this.playing ? 'el-icon-video-pause' : 'el-icon-video-play'
    },
    remainingTime() {
      const current = Math.round(this.duration - this.c)
      if (current === 0){
        return Math.round(this.duration)
      }
      return current
    }
  },
}
</script>

<style scoped>
.audio-player{
  margin: .3rem .6rem;
  display: inline-block;
  background-color: rgb(152,225,101);
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
  border-radius: 0.3rem;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}
audio {
  display: none;
}
span i {
  font-size: 26px;
  font-weight: 600;
  margin-right: 20px;
  vertical-align: -2px;
}
span i:hover {
  color: #409eff;
}
</style>