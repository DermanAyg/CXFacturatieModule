<template>
  <ion-page>
    <ion-content :fullscreen="true">

      <div id="container" class="container">
        <div class="section_block">
          <div class="profiel_wrapper">

            <ion-grid>
              <ion-row style="display: flex;align-items: center;">
                <ion-col size="2">
                  <div>
                    <ion-icon :icon="personCircleSharp" style="color: #A8AAAC;font-size:74px;"></ion-icon>
                  </div>
                </ion-col>
                <ion-col size="10" style="padding-left: 25px;">
                  <h2 style="margin-bottom: 5px;margin-top:0px;">{{ userProfile?.firstname}} {{ userProfile?.lastname}}</h2>
                  <p style="margin: 0px;">{{ loggedinuser?.role }}</p>
                </ion-col>
              </ion-row>
            </ion-grid>

          </div>
        </div>
        <div class="section_block">
          <h2 class="section_title">Gegevens</h2>
          <div class="profile_wrapper">
            <ul>
              <li>{{ userProfile?.phone }}</li>
              <li>{{ userProfile?.email }}</li>
              <li>{{ userProfile?.date_of_birth }}</li>
              <li>{{ userProfile?.address }}</li>
              <li>{{ userProfile?.gender }}</li>
            </ul>
            <div class="edit_profile_btn_wrapper">
              <div class="edit_profile_background" @click="updateProfileToggler()">
                <ion-icon :icon="settingsSharp" style="color: #FFF;"></ion-icon>
              </div>
            </div>
          </div>
        </div>
        <div v-if="isAdmin" class="section_block">
          <h2 class="section_title">Personeel</h2>
          <div class="profile_wrapper">
            <ul>
              <a href="#"><li>Registreren</li></a>
              <a href="#"><li>Wachtwoord vergeten</li></a>
              <a href="#"><li>Blokkeren</li></a>
              <a href="#"><li>Onderhouden</li></a>
            </ul>
          </div>
        </div>
        <div v-if="isAdmin" class="section_block">
          <h2 class="section_title">Facturen</h2>
          <div class="profile_wrapper">
            <ul>
              <a href="#"><li>Registreren</li></a>
              <a href="#"><li>Wachtwoord vergeten</li></a>
              <a href="#"><li>Blokkeren</li></a>
              <a href="#"><li>Onderhouden</li></a>
            </ul>
          </div>
        </div>
        <div class="section_block">
          <div class="logout_wrapper">
            <ion-button @click="user_logout">Log out</ion-button>
          </div>
        </div>
      </div>

      <div id="profile_modal" class="modal profile_modal container">
        <div class="section_block">
          <h2 class="section_title">Gegevens</h2>
          <div class="profile_wrapper">
            <ul>
              <li><input type="text" v-model="updatedProfile.phone" /></li>
              <li><input type="text" v-model="updatedProfile.email" /></li>
              <li><input type="text" v-model="updatedProfile.date_of_birth" /></li>
              <li><input type="text" v-model="updatedProfile.address" /></li>
              <li><input type="text" v-model="updatedProfile.gender" /></li>
            </ul>
            <div class="profile_btn_wrapper">
              <button @click="updateProfileToggler()" class="profile_back_btn">Terug</button>
              <button @click="updateProfile()" class="profile_save_btn">Opslaan</button>
            </div>
          </div>
        </div>
      </div>

    </ion-content>
  </ion-page>
</template>
<style>
.container {
  min-height: 500px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: unset;
  margin-top: 100px;
  flex-direction: column;
  margin-bottom: 25px;
}
.profile_wrapper {
  max-height: 470px!important;
}
.profile_wrapper ul {
  list-style-type: none;
  padding: 0;
  margin-left:15px;
  padding-bottom: 10px;
}
.profile_wrapper li {
  padding-bottom: 5px;
}
.profile_wrapper li span {
  padding-left: 25px;
}
.section_block_contactkaart .profile_wrapper {
  display: flex;
  flex-flow: column;
  align-items: center;
  padding-top: 25px;
}
.section_block_contactkaart {
  background-color: #CD7130!important;
}
.section_block_contactkaart_btn {
  background-color: #292828;
  width: 80%;
  display: block;
  text-align: center;
  padding: 20px 0px;
  text-decoration: none;
  font-weight: 500;
  color: #FFF!important;
}
.section_block_contactkaart p {
  font-size: 13px;
}
.edit_profile_btn_wrapper {
  display: flex;
  justify-content: flex-end;
  padding-bottom: 15px;
}
.edit_profile_background {
  display:flex;
  justify-content: center;
  align-items: center;
  width:25px;
  height:25px;
  background-color: #CD7130!important;
  cursor: pointer;
}
.profile_modal {
  display: none;
  position: absolute;
  top: 120px;
}
.profile_modal .section_block {
  height: 285px;
}
.profile_modal input {
  color: black;
  border: none;
  padding: 5px;
  font-size: 13px;
}
.profile_modal button {
  padding: 7px 20px;
  font-size: 13px;
}
.profile_btn_wrapper {
  display: flex;
  justify-content: flex-end;
}
.profile_back_btn {
  margin-left: 10px;
  background-color: #CD7130!important;
  color: #FFF;
}
.profile_save_btn {
  margin-left: 10px;
  background-color: #CD7130!important;
  color: #FFF;
}
</style>
<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, onIonViewWillEnter } from '@ionic/vue';
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios'
import { alertCircleSharp, checkmarkCircleSharp, personCircleSharp, settingsSharp } from 'ionicons/icons';
import { useAuth0 } from '@auth0/auth0-vue';
import router from '@/router';

const updatedProfile = ref({
  "firstname": "",
  "lastname": "",
  "phone": "",
  "email": "",
  "date_of_birth": "",
  "gender": "",
  "address": ""
});

const loggedinuser = ref()
const userProfile = ref()

const isAdmin = computed(() => loggedinuser.value?.role === 'admin');
const isUser = computed(() => loggedinuser.value?.role === 'user');

const auth0 = useAuth0();
const { logout, user, isAuthenticated } = useAuth0();
const logoutParams = { returnTo: window.location.origin + '/login' };

function user_logout() {
  logout({ logoutParams });
}

function updateProfileToggler() {
  var profile_modal = document.getElementById("profile_modal");
  if (!profile_modal) return;

  const computedStyle = window.getComputedStyle(profile_modal);
  const displayValue = computedStyle.display;

  if (displayValue === "none") {
    profile_modal.style.display = "flex";
  } else if (displayValue === "flex") {
    profile_modal.style.display = "none";
  }
}

async function updateProfile() {
  try {
    const response = await axios.put('http://127.0.0.1:8000/profile/?profile_id=' + loggedinuser.value.profile_id, updatedProfile.value,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  } catch (error) {
    console.error('Error updating the profile:', error);
  }
  location.reload();
}

async function fetchLoggedInUser() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/userbyemail/' + user.value?.email)
  return response.data
}

async function fetchUserProfile(profileId: any) {
    const response = await axios.get<[]>('http://127.0.0.1:8000/profile/{id}?profile_id=' + loggedinuser.value.profile_id)
    return response.data
}

onIonViewWillEnter(async () => {
  loggedinuser.value = null;
  userProfile.value = null;

  if (isAuthenticated.value && user.value?.email) {
    loggedinuser.value = await fetchLoggedInUser();
    userProfile.value = await fetchUserProfile(loggedinuser.value.profile_id);
  }
});

watch([isAuthenticated, user], async ([authenticated, userInfo]) => {
  if (authenticated && userInfo?.email) {
    loggedinuser.value = await fetchLoggedInUser();
    userProfile.value = await fetchUserProfile(loggedinuser.value.profile_id);
  }
});
</script>
