<template>
  <div id="dialogue">
    <el-row :gutter="20" type="flex" justify="space-around" style="margin-left: 0px; margin-right: 0px;">
      <el-col :xs="17" :sm="12" :lg="10">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" router="router"
                 active-text-color="#FFA500">
          <el-menu-item index="search">Search</el-menu-item>
          <el-menu-item index="help">Help</el-menu-item>
          <el-menu-item index="about">About</el-menu-item>
        </el-menu>
      </el-col>
      <el-col :xs="4" :sm="3" :lg="2" style="padding-top: 20px; padding-right: 5px">
        <github-button href="https://github.com/windrises/dialogue.moe" data-icon="octicon-star" data-size="large">
          Star
        </github-button>
      </el-col>
    </el-row>
    <router-view/>
  </div>
</template>

<script>
import GithubButton from 'vue-github-button'
export default {
  name: 'Dialogue',
  data () {
    return {
      router: true
    }
  },
  computed: {
    activeIndex: function () {
      let path = this.$route.path.substr(1)
      if (path === '') {
        path = 'search'
      }
      return path
    }
  },
  components: {
    GithubButton
  }
}
</script>

<style>
#dialogue {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 25px;
}
</style>
