import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { IonicVue } from '@ionic/vue';
import { createAuth0 } from '@auth0/auth0-vue';
import { useAuth0 } from '@auth0/auth0-vue';

/* Core and Ionic CSS files */
import '@ionic/vue/css/core.css';
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';
import '@ionic/vue/css/palettes/dark.always.css';
import './theme/variables.css';

const app = createApp(App)
  .use(IonicVue)
  .use(router);

app.use(
  createAuth0({
    domain: 'dev-icv5ncp4ozs145pe.eu.auth0.com',
    clientId: '3iW54zkwBpaEl3eDECbnyjLIPLVRUH2p',
    authorizationParams: {
      redirect_uri: window.location.origin + '/login',
    },
  })
);

app.mount('#app');
