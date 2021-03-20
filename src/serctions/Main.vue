<template>
  <el-container>
    <Aside/>
    <el-main>
      <el-skeleton :loading="loading" :rows="10" animated>
        <el-collapse v-model="activeName" accordion>
          <el-collapse-item :title="name" :name="index" v-for="(event, name, index) in events" :key="index">
            <div class="audio-item" v-for="id in event" :key="id.id">
              <audio-player :url="'https://cdn.jsdelivr.net/gh/Gitvoice/Aatrox@audio/skin0/'+id+'.mp3'"/>
              <span>{{ id }}</span>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-skeleton>
    </el-main>
  </el-container>
</template>

<script>
import {ElContainer, ElMain, ElCollapse, ElCollapseItem, ElSkeleton} from 'element-plus';
import Aside from "@/serctions/Aside";
import AudioPlayer from "@/components/AudioPlayer";

function sortObjByKey(obj) {
  const keys = Object.keys(obj).sort();
  const newObj = {}
  for (let i = 0; i < keys.length; i++) {
    const index = keys[i];
    newObj[index] = obj[index];
  }
  return newObj;
}

export default {
  name: "Main",
  components: {
    ElContainer, ElMain, ElCollapse, ElCollapseItem, ElSkeleton, Aside, AudioPlayer
  },
  data() {
    return {
      events: null,
      activeName: 0,
      loading: true
    }
  },
  mounted() {
    let url = 'https://cdn.jsdelivr.net/gh/Virace/lol-audio-events-hashtable/VO/characters/aatrox/skin0.json'
    this.axios.get(url + '?' + new Date().getTime())
        .then(resp => {
          const data = resp.data.data
          for (let audio in data) {
            if (Object.prototype.hasOwnProperty.call(data, audio)) {
              this.events = sortObjByKey(data[audio])
              this.loading = false
            }
          }

        })
  }
}
</script>

<style scoped>
.el-main {
  margin: 1.5rem;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-space__item {
  width: 100%;
}
.el-collapse{
  width: 100%;
}

ul {
  padding: 1rem 1.5rem;

}

.audio-item {
  position: relative;
  display: block;
  padding: .5rem 1rem;
  text-decoration: none;
}
</style>