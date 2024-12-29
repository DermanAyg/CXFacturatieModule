<template>
  <ion-page>
    
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Login</ion-title>
        </ion-toolbar>
      </ion-header>

      <div class="container">
        <ion-item>
          <ion-spinner name="crescent"></ion-spinner>
        </ion-item>
      </div>
      
    </ion-content>
  </ion-page>
</template>
<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButton } from '@ionic/vue';
import { computed, onMounted, watchEffect } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import router from '@/router';

const { loginWithRedirect, logout, user, isAuthenticated, isLoading } = useAuth0();
const logoutParams = { returnTo: window.location.origin };

const redirectToHome = () => {
  router.push('/tabs/home');
};

async function user_login() {
  await loginWithRedirect();
}

onMounted(async () => {
  while (isLoading.value) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  if (isAuthenticated.value) {
    redirectToHome();
  } else {
    user_login();
  }
});

watchEffect(() => {
  if (isAuthenticated.value) {
    redirectToHome();
  }
});
</script>
