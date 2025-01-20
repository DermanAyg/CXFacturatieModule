<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">

        <ion-tab-button tab="settings" href="/tabs/settings">
          <ion-icon aria-hidden="true" :icon="settingsSharp" />
          <ion-label>Settings</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="historie" href="/tabs/historie">
          <ion-icon aria-hidden="true" :icon="fileTrayFullSharp" />
          <ion-label>Historie</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="home" href="/tabs/home">
          <ion-icon aria-hidden="true" :icon="homeSharp" />
          <ion-label>Home</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="facturen" href="/tabs/facturen">
          <ion-icon aria-hidden="true" :icon="documentSharp" />
          <ion-label>Facturen</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="profiel" href="/tabs/profiel">
          <ion-icon aria-hidden="true" :icon="personCircleSharp" />
          <ion-label>Profiel</ion-label>
        </ion-tab-button>

      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { documentSharp, fileTrayFullSharp, homeSharp, personCircleSharp, settingsSharp } from 'ionicons/icons';
</script>
