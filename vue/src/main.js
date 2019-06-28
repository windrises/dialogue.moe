// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Dialogue from './Index'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'element-ui/lib/theme-chalk/display.css'
import {
  Backtop,
  Divider,
  Menu,
  MenuItem,
  Input,
  Checkbox,
  Button,
  Table,
  TableColumn,
  Tag,
  Icon,
  Row,
  Col,
  Card,
  Container,
  Header,
  Aside,
  Main,
  Progress,
  Message
} from 'element-ui'

Vue.use(Backtop)
Vue.use(Divider)
Vue.use(Menu)
Vue.use(Icon)
Vue.use(Input)
Vue.use(Checkbox)
Vue.use(Button)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Tag)
Vue.use(Row)
Vue.use(Col)
Vue.use(Card)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(MenuItem)
Vue.use(Progress)

Vue.use(VueAxios, axios)

Vue.prototype.$message = Message
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#dialogue',
  router,
  components: { Dialogue },
  template: '<Dialogue/>'
})
