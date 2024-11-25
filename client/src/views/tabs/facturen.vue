<template>
    <ion-page>

      <ion-content :fullscreen="true">
  
        <div class="container">
          <div class="section_block">
            <h2>Factuur zoeken</h2>
          </div>
        </div>
        
      </ion-content>
    </ion-page>
  </template>
<style>
.section_block {
  min-width: 90%;
  min-height: 150px;
  background-color: #292828;
  border: solid 1px RGB(13,26,51,0.1);
  border-radius: 5px;
}
</style>
<script setup lang="ts">
  import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
</script>
