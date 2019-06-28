<template>
    <div>
      <el-row :gutter="20" type="flex" justify="center" style="margin-left: 0px; margin-right: 0px;">
        <el-col :xs="24" :sm="20" :lg="18">
          <el-card class="box-card">
            <ul>
              <li>
                <div class="text item">
                  <p>Dialogue.moe is a open source project which aims to help us search dialogues in animes</p>
                </div>
              </li>
              <li>
                <div class="text item">
                  <p>The dialogues come from a large number of Chinese subtitle files which are crawled from the Internet</p>
                  <p>The dialogues are stored and analyzed by Elasticsearch for full-text search</p>
                </div>
              </li>
              <li>
                <div class="text item">
                  <p>Due to the high cost, the server has only 2 vCPU and 4 GiB memory. Please don't try to crawl this website with high concurrency</p>
                </div>
              </li>
              <li>
                <div class="text item">
                  <p>You can find the data and source code in <a href="https://github.com/windrises/dialogue.moe" target="_blank">
                    https://github.com/windrises/dialogue.moe
                  </a></p>
                </div>
              </li>
              <li>
                <div class="text item">
                  <p>Please Email <a href="mailto:dialogue.moe@gamil.com">dialogue.moe@gamil.com</a> if you</p>
                  <ul>
                    <li>
                      <p>don't want your work to appear in search results</p>
                    </li>
                    <li>
                      <p>have any advise</p>
                    </li>
                  </ul>
                </div>
              </li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.text {
  font-size: 16px;
  text-align: left;
}

.item {
  padding: 18px 0;
}
</style>
