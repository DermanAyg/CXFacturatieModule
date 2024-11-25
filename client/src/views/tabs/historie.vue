<template>
    <ion-page>

      <ion-content :fullscreen="true">
  
        <ExploreContainer name="historie" />
        
      </ion-content>
    </ion-page>
  </template>

<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
import ExploreContainer from '@/components/ExploreContainer.vue';
</script>
