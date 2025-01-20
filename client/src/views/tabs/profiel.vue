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
          <h2 class="section_title">Personeel profiel</h2>
          <div class="profile_wrapper">
            <ul style="width: fit-content;">
              <a style="cursor:pointer;" @click="profileRegistrationToggler()"><li>Registreren</li></a>
              <a style="cursor:pointer;" @click="profileManagerToggler()"><li>Verwijderen</li></a>
            </ul>
          </div>
        </div>
        <div class="section_block" style="padding: 15px 15px;">
          <div class="logout_wrapper">
            <ion-button id="logout_btn" class="logout_btn" @click="user_logout">Log out</ion-button>
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
      
      <div v-if="toggleProfileRegistration" id="personeel_profiel_modal_registreren" class="modal container personeel_profiel_modal_registreren">
        <div class="personeel_profiel_modal_registreren_header" style="width: 95%;">
          <ion-grid>
            <ion-row>
              <ion-col size="2">
                <ion-icon @click="profileRegistrationToggler()" :icon="arrowBackSharp" style="font-size: 28px;color: #CD7130;cursor:pointer;"></ion-icon>
              </ion-col>
              <ion-col size="8">
                <h2 style="text-align:center;">Personeel profiel aanmaken</h2>
              </ion-col>
              <ion-col size="2">
              </ion-col>
            </ion-row>
          </ion-grid>
        </div>

        <div class="personeel_profiel_modal_registreren_form">
            <ion-grid>
              <ion-row>
                <ion-col>
                  <ion-item>
                    <ion-input v-model="profileData['firstname']" label="Voornaam" label-placement="stacked" ref="input" type="text" placeholder="voornaam"></ion-input>
                  </ion-item>
                </ion-col>
                <ion-col>
                  <ion-item>
                    <ion-input v-model="profileData['lastname']" label="Achternaam" label-placement="stacked" ref="input" type="text" placeholder="achternaam"></ion-input>
                  </ion-item>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-item>
                    <ion-input v-model="profileData['phone']" label="Telefoonnummer" label-placement="stacked" ref="input" type="text" placeholder="telefoonnummer"></ion-input>
                  </ion-item>
                </ion-col>
                <ion-col>
                  <ion-item>
                    <ion-input v-model="profileData['email']" label="Emailadres" label-placement="stacked" ref="input" type="text" placeholder="emailadres"></ion-input>
                  </ion-item>
                </ion-col>
              </ion-row>

              <ion-row>
                <ion-col>
                  <ion-item>
                    <ion-input v-model="profileData['address']" label="Adres" label-placement="stacked" ref="input" type="text" placeholder="adres"></ion-input>
                  </ion-item>
                </ion-col>
              </ion-row>
              
            </ion-grid>
        </div>

        <div class="personeel_profiel_modal_registreren_footer">
          <button class="profiel_aanmaken_btn" @click="postProfile()">Profiel aanmaken</button>
        </div>
 
      </div>

      <div v-if="toggleProfileManager" id="personeel_profiel_modal_blokkeren" class="modal container personeel_profiel_modal_blokkeren">
        
        <div class="personeel_profiel_modal_registreren_header" style="width: 95%;">
          <ion-grid>
            <ion-row>
              <ion-col size="2">
                <ion-icon @click="profileManagerToggler()" :icon="arrowBackSharp" style="font-size: 28px;color: #CD7130;cursor:pointer;"></ion-icon>
              </ion-col>
              <ion-col size="8">
                <h2 style="text-align:center;">Personeel profiel verwijderen</h2>
              </ion-col>
              <ion-col size="2">
              </ion-col>
            </ion-row>
          </ion-grid>
        </div>

        <div class="personeel_profiel_modal_registreren_form" style="width:90%;">
          <ul style="list-style-type: none;margin:0;padding: 25px 50px;">
            <li style="text-align:center;" v-for="profile in profiles">
              {{ profile?.id }} - {{ profile?.firstname }} - {{ profile?.lastname }} - {{ profile?.phone }} - {{ profile?.email }}
              <span @click="deleteProfile(profile)" style="cursor:pointer;margin-left: 25px;color:#CD7130;">X</span>
            </li>
          </ul>
        </div>

      </div>

    </ion-content>
  </ion-page>
</template>
<style>
.personeel_profiel_modal_registreren_header {
  padding-top: 20px;
  padding-bottom: 20px;
  background-color: #0c0c0c;
}
.personeel_profiel_modal_registreren_header ion-col{
  display:flex;
  align-items: center;
}
.personeel_profiel_modal_registreren_header ion-col h2{
  margin:0;
  text-align:center;
  width: 100%;
}
.personeel_profiel_modal_registreren_form {
  margin-top: 50px;
  background-color: #0c0c0c;
}
.personeel_profiel_modal_registreren_footer {
  margin-top: 30px;
}
.profiel_aanmaken_btn {
  margin-right: 25px;
  margin-bottom: 25px;
  padding: 10px 40px;
  display: flex;
  justify-self: self-end;
  background-color: #E4833F;
  color: #FFF;
}
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
  padding-bottom: 0px;
  margin-bottom: 0px;
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
  height: 225px;
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
  margin-top: -30px;
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
.logout_btn {
  border-radius: 0;
  color: #FFF;
  font-size: 12px;
}
.personeel_profiel_modal_registreren, .personeel_profiel_modal_blokkeren {
  position: absolute;
  background-color: #121212;
  top: 0;
  left: 4vw;
  width: 91vw;
  height: 80vh;
}
</style>
<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, onIonViewWillEnter, onIonViewDidLeave, onIonViewWillLeave,IonModal,IonItem,IonInput,IonList } from '@ionic/vue';
import { ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios'
import { alertCircleSharp, arrowBackSharp, checkmarkCircleSharp, personCircleSharp, settingsSharp } from 'ionicons/icons';
import { useAuth0 } from '@auth0/auth0-vue';
import router from '@/router';

const loggedinuser = ref();
const userProfile = ref();
const profiles = ref();

const isAdmin = computed(() => loggedinuser.value?.role === 'admin');
const isUser = computed(() => loggedinuser.value?.role === 'user');

const auth0 = useAuth0();
const { logout, user, isAuthenticated } = useAuth0();
const logoutParams = { returnTo: window.location.origin + '/login' };

const profileData = ref({
  'firstname': '',
  'lastname': '',
  'phone': '',
  'email': '',
  'date_of_birth': 'anon',
  'gender': 'anon',
  'address': ''
})

const toggleProfileRegistration = ref();
const toggleProfileManager = ref();

const updatedProfile = ref({
  "firstname": "",
  "lastname": "",
  "phone": "",
  "email": "",
  "date_of_birth": "",
  "gender": "",
  "address": "",
});

async function deleteProfile(profile: any) {
  if(confirm("Weet je zeker dat je profiel: " + profile.email + " wilt verwijderen?")) {
    try {
      const response = await axios.delete('http://127.0.0.1:8000/profile/{id}?profile_id='+profile.id+'',
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    } catch (error) {
      console.error('Error deleting the profile:', error);
    }
    location.reload()
  }
}

function user_logout() {
  logout({ logoutParams });
}

function updateProfileToggler() {
  var profile_modal = document.getElementById("profile_modal");
  if (!profile_modal) return;

  const computedStyle = window.getComputedStyle(profile_modal);
  const displayValue = computedStyle.display;

  updatedProfile.value['firstname'] = userProfile.value?.firstname;
  updatedProfile.value['lastname'] = userProfile.value?.lastname;
  updatedProfile.value['phone'] = userProfile.value?.phone;
  updatedProfile.value['email'] = userProfile.value?.email;
  updatedProfile.value['date_of_birth'] = userProfile.value?.date_of_birth;
  updatedProfile.value['gender'] = userProfile.value?.gender;
  updatedProfile.value['address'] = userProfile.value?.address;

  if (displayValue === "none") {
    profile_modal.style.display = "flex";
  } else if (displayValue === "flex") {
    profile_modal.style.display = "none";
  }
}

function profileRegistrationToggler() {
  if (toggleProfileRegistration.value) {
    toggleProfileRegistration.value = false;
  } else {
    toggleProfileRegistration.value = true;
  }
}

function profileManagerToggler() {
  if (toggleProfileManager.value) {
    toggleProfileManager.value = false;
  } else {
    toggleProfileManager.value = true;
  }
}

async function postProfile() {
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/profile/', profileData.value,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    } catch (error) {
      console.error("Error:", error);
    }
    location.reload();
  }

async function updateProfile() {
  console.log(loggedinuser.value.profile_id);
  console.log(updatedProfile.value)
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

async function fetchUserProfiles() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/profile/')
  return response.data
}

async function fetchUserProfile(profileId: any) {
    const response = await axios.get<[]>('http://127.0.0.1:8000/profile/{id}?profile_id=' + loggedinuser.value.profile_id)
    return response.data
}

onIonViewWillLeave(async () => {
  location.reload();
})

onIonViewWillEnter(async () => {
  loggedinuser.value = null;
  userProfile.value = null;
  profiles.value = await fetchUserProfiles();

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
