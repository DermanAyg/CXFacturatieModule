<template>
  <ion-app>
    <ion-router-outlet />
    <ion-header>
      
        <ion-toolbar >
          <div class="cus_toolbar">
            <ion-title>Codelogix</ion-title>
            <ion-icon class="notification_icon" :icon="notificationsSharp"></ion-icon>
          </div>
        </ion-toolbar>
      
    </ion-header>
  </ion-app>
</template>
<script setup lang="ts">
import { IonApp, IonRouterOutlet, IonHeader, IonToolbar, IonIcon } from '@ionic/vue';
import { notificationsSharp } from 'ionicons/icons';
</script>
<style>
.cus_toolbar {
  display: flex;
  align-items: center;
}
.notification_icon {
  margin-right: 20px;
  font-size: 18px;
  cursor: pointer;
}
.notification_icon:hover {
  color: #E4833F!important;
}
a {
 color: #E4833F!important;
}
</style>