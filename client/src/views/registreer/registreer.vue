<template>
    <ion-page>

      <ion-content :fullscreen="true">
        <ion-header collapse="condense">
          <ion-toolbar>
            <ion-title size="large">Registreer</ion-title>
          </ion-toolbar>
        </ion-header>
  
        <ExploreContainer name="registreer" />
      </ion-content>
    </ion-page>
  </template>

<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
</script>
