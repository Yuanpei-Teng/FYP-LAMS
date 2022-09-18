import { createApp } from 'vue'
import App from './App.vue'
import installElementPlus from './plugins/element'
import router from './router'
import axios from 'axios'
import tracking from './js/tracking-min'
import face from './js/face-min'
import jquery from './js/jquery.min'
import cookies from './js/cookies-utils'
import { Expand, ChatRound } from '@element-plus/icons'
import '@/router/permission'
const app = createApp(App).use(router).use(tracking).use(face).use(jquery)
//bind axios in Vue http attribute，after that we can use this.$http.get()/this.$http.post()to use GET/POST requests just like Ajax
app.config.globalProperties.$http = axios
app.config.globalProperties.$cookies = cookies
installElementPlus(app)
app.component('expand', Expand)
    .component('chat-round', ChatRound)
app.mount('#app')