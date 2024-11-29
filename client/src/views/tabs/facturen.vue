<template>
    <ion-page>
      <ion-content :fullscreen="true">
        <div class="container">

          <!-- TODO: factuur aanmak modal -->
          <ion-modal ref="modal" trigger="open-modal" @willDismiss="onWillDismiss">
            <ion-header>
              <ion-toolbar>
                <ion-buttons slot="start">
                  <ion-button @click="cancel()">Cancel</ion-button>
                </ion-buttons>
                <ion-title style="text-align: center;">Factuur aanmaken</ion-title>
                <ion-buttons slot="end">
                  <ion-button :strong="true" @click="confirm()">Confirm</ion-button>
                </ion-buttons>
              </ion-toolbar>
            </ion-header>
            <ion-content class="ion-padding">
              <ion-item>
                <ion-input
                  label="Enter your name"
                  label-placement="stacked"
                  ref="input"
                  type="text"
                  placeholder="Your name"
                ></ion-input>
              </ion-item>
            </ion-content>
          </ion-modal>

          <div class="cus_section_block_options">
            <div style="display:flex; justify-content: end;">
              <ion-fab>
                <ion-fab-button id="open-modal" style="--background: #E4833F;">
                  <ion-icon :icon="add" style="color: #FFF;"></ion-icon>
                </ion-fab-button>
              </ion-fab>
            </div>
          </div>

          <div class="section_block">
            <h2 class="section_title">Factuur zoeken</h2>
          </div>

          <div class="section_block">
            <h2 class="section_title">Open facturen</h2>
          </div>

          <div class="section_block">
            <h2 class="section_title">Gesloten facturen</h2>
          </div>

        </div>
      </ion-content>
    </ion-page>
  </template>
<style>
.cus_section_block_options {
  min-width: 90%;
  min-height: 85px;
}
.section_block {
  min-width: 90%;
  min-height: 150px;
  background-color: #292828;
  border: solid 1px RGB(13,26,51,0.1);
  border-radius: 5px;
  margin-bottom: 20px;
  padding: 0px 15px;
}
.section_block_invis {
  min-width: 90%;
  min-height: 150px;
}

.section_title {
  font-size: 20px;
}
</style>
<script setup lang="ts">
  import { 
    IonPage, 
    IonHeader, 
    IonToolbar, 
    IonTitle, 
    IonContent, 
    IonFab, 
    IonFabButton, 
    IonIcon, 
    IonButtons,
    IonButton,
    IonModal,
    IonItem,
    IonInput, } from '@ionic/vue';
  import { OverlayEventDetail } from '@ionic/core/components';
  import { add } from 'ionicons/icons';
  import { ref } from 'vue';

  const message = ref('This modal example uses triggers to automatically open a modal when the button is clicked.');

  const modal = ref();
  const input = ref();

  const cancel = () => modal.value.$el.dismiss(null, 'cancel');

  const confirm = () => {
    const name = input.value.$el.value;
    modal.value.$el.dismiss(name, 'confirm');
  };

  const onWillDismiss = (ev: CustomEvent<OverlayEventDetail>) => {
    if (ev.detail.role === 'confirm') {
      message.value = `Hello, ${ev.detail.data}!`;
    }
  };
</script>
