<template>
  <div>
    <el-container>
      <el-header height="260px">
        <el-row :gutter="20" type="flex" justify="center">
          <el-col :xs="24" :sm="20" :lg="18">
            <el-card class="box-card">
              <el-row :gutter="20">
                <el-col :span="5" :offset="1">
                  <a href="/search">
                    <img src="../assets/logo.png" alt="logo" style="height: 40px">
                  </a>
                </el-col>
              </el-row>
              <el-row :gutter="20" type="flex" justify="center">
                <el-col :xs="24" :sm="20" :lg="18">
                  <div class="grid-content bg-purple">
                  <el-input
                    placeholder="Please input"
                    v-model="text"
                    clearable @keyup.enter.native="search">
                    <el-button slot="append" icon="el-icon-search" :loading="loading" @click="search"></el-button>
                  </el-input>
                  </div>
                </el-col>
              </el-row>

              <div class="hidden-sm-and-up">
                <el-row :gutter="20" type="flex" justify="start">
                  <el-col :xs="24">
                    <el-input
                      size="small"
                      placeholder="Optional"
                      v-model="bangumi_id"
                      clearable @keyup.enter.native="search">
                      <template slot="prepend">Bangumi ID:</template>
                    </el-input>
                  </el-col>
                </el-row>
                <el-row :gutter="20" type="flex" justify="start">
                  <el-col :xs="7">
                    <el-checkbox v-model="duplicate">Remove duplication</el-checkbox>
                  </el-col>
                </el-row>
              </div>
              <div class="hidden-xs-only">
                <el-row :gutter="20" type="flex" justify="space-around">
                  <el-col :sm="4" :lg="4">
                    <el-checkbox v-model="duplicate">Remove duplication</el-checkbox>
                  </el-col>
                  <el-col :sm="12" :lg="8">
                    <el-input
                      size="small"
                      placeholder="Optional"
                      v-model="bangumi_id"
                      clearable @keyup.enter.native="search">
                      <template slot="prepend">Bangumi ID:</template>
                    </el-input>
                  </el-col>
                </el-row>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-header>
      <el-row :gutter="20" type="flex" justify="center" v-if="progress_vis">
        <el-col :xs="24" :sm="20" :lg="18">
          <el-progress :percentage="percentage" :color="progress_color" :show-text=false style="top: 15px"></el-progress>
        </el-col>
      </el-row>
      <el-container v-if="result_show">
        <el-main>
          <el-row :gutter="20" type="flex" justify="center">
            <el-col :xs="24" :sm="20" :lg="18">
              <el-card class="box-card">
                <el-row :gutter="20">
                  <el-col :span="5" :offset="1">
                    <div class="text" style="float: left">
                      About {{total}} results
                    </div>
                  </el-col>
                  <el-col :span="4" :offset="0">
                    <div class="text" style="float: left">
                      {{time_cost}} ms
                    </div>
                  </el-col>
                </el-row>
                <div><el-divider></el-divider></div>

                <el-table
                  :show-header="false"
                  :data="dialogues"
                  stripe
                  style="width: 100%">
                  <el-table-column>
                    <template slot-scope="scope">
                      <el-row :gutter="20">
                        <div class="hidden-sm-and-up">
                          <el-row :gutter="20" type="flex" justify="start">
                            <el-col :xs="24">
                              <el-button size="medium" round>
                                <a :href="'https://bgm.tv/subject/' + scope.row.subject_id" target="_blank" style="color: orange;">
                                  <strong>{{scope.row.subject_name}}</strong>
                                </a>
                              </el-button>
                              <el-tag type="warning" effect="plain" v-if="scope.row.ep.length">ep.{{scope.row.ep}}</el-tag>
                            </el-col>
                          </el-row>
                          <el-row :gutter="20" type="flex" justify="start" style="top: 5px">
                            <el-col :xs="4">
                              <div>
                                <el-tag type="info">Score: {{scope.row.score}}</el-tag>
                              </div>
                            </el-col>
                          </el-row>
                        </div>
                        <el-row :gutter="20" type="flex" justify="space-around" class="hidden-xs-only">
                          <el-col :sm="20" :lg="16">
                            <el-button size="medium" round>
                              <a :href="'https://bgm.tv/subject/' + scope.row.subject_id" target="_blank" style="color: orange;">
                                <strong>{{scope.row.subject_name}}</strong>
                              </a>
                            </el-button>
                            <el-tag type="warning" effect="plain" v-if="scope.row.ep.length">ep.{{scope.row.ep}}</el-tag>
                          </el-col>
                          <el-col :sm="4" :lg="4">
                            <div>
                              <el-tag type="info">Score: {{scope.row.score}}</el-tag>
                            </div>
                          </el-col>
                        </el-row>

                        <el-row :gutter="20" style="top: 10px">
                          <el-col :span="3" class="hidden-xs-only" :xs="{offset: 0}" :sm="{offset: 2}">
                            <div class="text" style="float: left">
                              Subtitle:
                            </div>
                          </el-col>
                          <el-col :span="18">
                            <div class="text" style="float: left">
                              {{scope.row.sub_title}}
                            </div>
                          </el-col>
                        </el-row>
                        <el-row :gutter="20" style="top: 5px">
                          <el-col :span="3" class="hidden-xs-only" :xs="{offset: 0}" :sm="{offset: 2}">
                            <div class="text" style="float: left">
                              ep:
                            </div>
                          </el-col>
                          <el-col :span="18">
                            <div class="text" style="float: left">
                              {{scope.row.file_name}}
                            </div>
                          </el-col>
                        </el-row>

                        <el-row :gutter="20" style="top: 10px">
                          <el-col :span="16" :xs="{offset: 6}" :sm="{offset: 5}">
                            <div class="text" style="text-align: center">
                              {{scope.row.text_before}}
                            </div>
                          </el-col>
                        </el-row>
                        <el-row :gutter="20" style="top: 5px">
                          <el-col :xs="{span: 6, offset: 0}" :sm="{span: 3, offset: 2}">
                            <div class="text" style="float: left">
                              <strong>{{scope.row.time_current}}</strong>
                            </div>
                          </el-col>
                          <el-col :span="16">
                            <div class="text" style="text-align: center; font-weight:bold" v-html="scope.row.text_current_highlight"></div>
                          </el-col>
                        </el-row>
                        <el-row :gutter="20" style="top: 0px">
                          <el-col :span="16" :xs="{offset: 6}" :sm="{offset: 5}">
                            <div class="text" style="text-align: center">
                              {{scope.row.text_after}}
                            </div>
                          </el-col>
                        </el-row>
                      </el-row>
                    </template>
                  </el-table-column>
                </el-table>

                <div><el-divider></el-divider></div>
                <el-row :gutter="20">
                  <el-col :span="24" :offset="0">
                    <el-button plain :loading="next_loading" @click="next_page">
                      Next page<i class="el-icon-arrow-right" ></i>
                    </el-button>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
    <el-backtop style="color: orange"></el-backtop>
  </div>
</template>

<script>
export default {
  name: 'Search',
  data () {
    return {
      text: '',
      bangumi_id: '',
      duplicate: false,
      last_text: '',
      last_bangumi_id: '',
      last_duplicate: false,
      total: 0,
      time_cost: 0,
      sort_values: '',
      result_show: false,
      loading: false,
      next_loading: false,
      last_scrollTop: 0,
      percentage: 0,
      timer: '',
      progress_vis: false,
      progress_color: '#f7cbab',
      dialogues: []
    }
  },
  methods: {
    post () {
      let config = {
        headers: {
          'Content-Type': 'application/json'
        }
      }
      this.axios.post('***', {
        text: this.last_text,
        bangumi_id: this.last_bangumi_id,
        duplicate: this.last_duplicate,
        sort_values: this.sort_values,
        history: this.dialogues
      }, config)
        .then((response) => {
          if (response.data.hasOwnProperty('error')) {
            this.error(response.data.error)
          } else {
            this.total = response.data.total
            this.time_cost = response.data.time_cost
            this.dialogues = this.dialogues.concat(response.data.dialogues)
            if (this.dialogues.length > 0) {
              this.sort_values = this.dialogues[this.dialogues.length - 1].sort_values
            }
            this.result_show = true

            this.$nextTick(function () {
              let scrollTop = document.documentElement.scrollTop
              let windowHeight = document.documentElement.clientHeight
              let scrollHeight = document.documentElement.scrollHeight
              if (scrollHeight - (scrollTop + windowHeight) <= 0.1 * windowHeight) {
                document.documentElement.scrollTop = this.last_scrollTop
              }
            })
          }
          this.loading = false
          this.next_loading = false
          this.progress_done()
        })
        .catch((error) => {
          this.error('Unknown Error!')
          this.loading = false
          this.next_loading = false
          this.progress_done()
        })
    },
    strip (str) {
      return str.replace(/(^\s*)|(\s*$)/g, '')
    },
    search () {
      this.text = this.strip(this.text)
      this.bangumi_id = this.strip(this.bangumi_id)
      if (this.text === '') {
        return
      }
      this.last_text = this.text
      this.last_bangumi_id = this.bangumi_id
      this.last_duplicate = this.duplicate
      this.result_show = false
      this.loading = true
      this.dialogues = []
      this.sort_values = ''
      this.progress()
      this.post()
    },
    next_page () {
      this.next_loading = true
      this.last_scrollTop = document.documentElement.scrollTop
      this.post()
    },
    error (message) {
      this.$message({
        showClose: true,
        message: message,
        type: 'error'
      })
    },
    add_percentage () {
      if (this.percentage < 95) {
        this.percentage += Math.floor(Math.random() * 5)
      }
    },
    progress () {
      this.percentage = 0
      this.progress_vis = true
      this.timer = setInterval(this.add_percentage, 250)
    },
    progress_done () {
      this.percentage = 100
      clearInterval(this.timer)
      this.progress_vis = false
    }
  }
}
</script>

<style scoped>
.el-header, .el-footer {
  background-color: #FFFFFF;
  color: #333;
  text-align: center;
  line-height: 55px;
}

.el-aside {
  background-color: #FFFFFF;
  color: #333;
  text-align: center;
  line-height: 200px;
  padding: 20px;
}

.el-main {
  background-color: #FFFFFF;
  color: #333;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-select .el-input {
  width: 130px;
}

.text {
  font-size: 14px;
}

>>> em {
  color: orange;
}
</style>
