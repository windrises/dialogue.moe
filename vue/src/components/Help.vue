<template>
    <div>
      <el-row :gutter="20" type="flex" justify="center" style="margin-left: 0px; margin-right: 0px;">
        <el-col :xs="24" :sm="20" :lg="18">
          <el-card class="box-card">
            <ul>
              <li>
                <div class="text item">
                  <p>Please input Simplified Chinese</p>
                </div>
              </li>
              <li>
                <div class="text item">
                  <p>The "Bangumi ID" means the anime's ID in
                  <a href="https://bgm.tv" target="_blank"> https://bgm.tv</a></p>
                </div>
              </li>
                <li>
                  <div class="text item">
                    <p>Two dialogues will be considered as the "duplication" when the following conditions are met:</p>
                    <ul>
                      <li><p>Come from the same anime</p></li>
                      <li><p>The timestamps are close</p></li>
                      <li><p>The <a href="https://en.wikipedia.org/wiki/Levenshtein_distance">
                        Levenshtein distance</a> is small</p></li>
                    </ul>
                  </div>
                </li>
              <li>
                <div class="text item">
                  <p>The anime name and episode number in search results are for reference only</p>
                </div>
              </li>
              <li>
                <div class="text item">
                  <p>To understand how the "Score" has been calculated, please read
                  <a href="https://www.elastic.co/guide/en/elasticsearch/guide/current/relevance-intro.html" target="_blank">
                    elastic docs
                  </a></p>
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
  name: 'Help'
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
