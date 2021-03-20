<template>
  <aside class="aside">

    <el-skeleton style="width: 100%" :loading="loading" animated>
      <template #template>
        <el-skeleton-item
            variant="image"
            style="width: 120px; height: 120px;"
        />
        <div style="margin: 1.7rem 0">
          <el-skeleton-item variant="h2" style="width: 50%;" />
          <el-skeleton-item variant="text" />
          <el-skeleton-item variant="text" />
          <el-skeleton-item variant="text" />
          <el-skeleton-item variant="text" />
          <el-skeleton-item variant="text" />
        </div>
      </template>
      <template #default>
        <el-avatar shape="square" size="120"
                   src="http://ddragon.leagueoflegends.com/cdn/11.6.1/img/champion/Aatrox.png"></el-avatar>
        <h2>{{ title }}</h2>
        <p>{{ info }}</p>
      </template>
    </el-skeleton>


  </aside>
</template>

<script>
import {ElCol, ElAvatar, ElSkeleton, ElSkeletonItem} from 'element-plus';

export default {
  name: "Aside",
  components: {
    ElCol, ElAvatar, ElSkeleton, ElSkeletonItem
  },
  data() {
    return {
      title: '',
      info: '',
      loading: true
    }
  },
  mounted() {
    this.axios.get('http://ddragon.leagueoflegends.com/cdn/11.6.1/data/zh_CN/champion/Aatrox.json')
        .then(resp => {
          const data = resp.data.data
          this.title = data.Aatrox.title + "·" + data.Aatrox.id
          this.info = data.Aatrox.blurb
          this.loading = false
        })
  }
}
</script>

<style scoped>
aside {
  margin: 1.5rem;
  padding: 2rem;
  width: 30%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}

.el-avatar--120 {
  width: 120px;
  height: 120px;
  line-height: 120px
}
</style>