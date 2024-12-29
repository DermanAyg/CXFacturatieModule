<template>
  <ion-page>
    <ion-content :fullscreen="true">

      <div id="container" class="container">
        <div class="section_block section_block_contactkaart">
          <h2 class="section_title">Contactkaart</h2>
          <div class="settings_wrapper">
            <a href="tel:phonenumber" class="section_block_contactkaart_btn">Contact opnemen</a>
            <p>Werkt bovenstaand knop niet? Bel dan: {{ initialCompany?.emergency_phone }}.</p>
            
          </div>
        </div>
        <div class="section_block">
          <h2 class="section_title">Bedrijfsgegevens</h2>
          <div v-if="loggedinuser.role === 'admin'" class="settings_wrapper">
            <ul>
              <li>{{ initialCompany?.name }}</li>
              <li>{{ initialCompany?.postcode }}, {{ initialCompany?.plaats }}</li>
              <li>{{ initialCompany?.straat }} {{ initialCompany?.huisnr }}</li>
            </ul>

            <ul>
              <li>KVK<span>{{ initialCompany?.kvk_nr }}</span></li>
              <li>BTW<span>{{ initialCompany?.btw_nr }}</span></li>
              <li>CODE<span>{{ initialCompany?.id }}</span></li>
            </ul>

            <ul>
              <li>Mail<span>{{ initialCompany?.email }}</span></li>
              <li>Telefoon<span>{{ initialCompany?.mobile }}</span></li>
            </ul>
            <div class="edit_settings_btn_wrapper">
              <div @click="updateCompanyToggler()" class="edit_settings_background">
                <ion-icon :icon="settingsSharp" style="color: #FFF;"></ion-icon>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div id="company_modal" class="modal company_modal container">
        <div class="section_block">
          <h2 class="section_title">Bedrijfsgegevens</h2>
          <div class="settings_wrapper">
            <ul>
              <li><input type="text" v-model="updatedCompany.name" /></li>
              <li><input type="text" v-model="updatedCompany.postcode" />  <input type="text" v-model="updatedCompany.plaats" /></li>
              <li><input type="text" v-model="updatedCompany.straat" />  <input type="text" v-model="updatedCompany.huisnr" /></li>
            </ul>

            <ul>
              <li><input type="text" v-model="updatedCompany.kvk_nr" /></li>
              <li><input type="text" v-model="updatedCompany.btw_nr" /></li>
            </ul>

            <ul>
              <li><input type="text" v-model="updatedCompany.email" /></li>
              <li><input type="text" v-model="updatedCompany.mobile" /></li>
            </ul>
            <div class="settings_btn_wrapper">
              <button @click="updateCompanyToggler()" class="settings_back_btn">Terug</button>
              <button @click="updateCompany()" class="settings_save_btn">Opslaan</button>
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
.settings_wrapper {
  max-height: 470px!important;
}
.settings_wrapper ul {
  list-style-type: none;
  padding: 0;
  margin-left:15px;
  padding-bottom: 10px;
}
.settings_wrapper li {
  padding-bottom: 5px;
}
.settings_wrapper li span {
  padding-left: 25px;
}
.section_block_contactkaart .settings_wrapper {
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
.edit_settings_btn_wrapper {
  display: flex;
  justify-content: flex-end;
  padding-bottom: 15px;
}
.edit_settings_background {
  display:flex;
  justify-content: center;
  align-items: center;
  width:25px;
  height:25px;
  background-color: #CD7130!important;
  cursor: pointer;
}
.company_modal {
  display: none;
  position: absolute;
  top: 200px;
}
.company_modal .section_block {
  height: 400px;
}
.company_modal input {
  color: black;
  border: none;
  padding: 5px;
  font-size: 13px;
}
.company_modal button {
  padding: 7px 20px;
  font-size: 13px;
}
.settings_btn_wrapper {
  display: flex;
  justify-content: flex-end;
}
.settings_back_btn {
  margin-left: 10px;
  background-color: #CD7130!important;
  color: #FFF;
}
.settings_save_btn {
  margin-left: 10px;
  background-color: #CD7130!important;
  color: #FFF;
}
</style>
<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
import { ref, onMounted, watch } from 'vue';
import axios from 'axios'
import { alertCircleSharp, checkmarkCircleSharp, settingsSharp } from 'ionicons/icons';

const initialCompany = ref();
const updatedCompany = ref({
  "name": "",
  "postcode": "",
  "plaats": "",
  "straat": "",
  "huisnr": "",
  "email": "",
  "mobile": "",
  "emergency_phone": "",
  "kvk_nr": "",
  "btw_nr": "",
  "users": []
});

const loggedinuser = ref({
  "email": "johnvisser_123@hotmail.com",
  "firstname": "John",
  "lastname": "Visser",
  "role": "admin",
})

function updateCompanyToggler() {
  var company_modal = document.getElementById("company_modal");
  if (!company_modal) return;

  const computedStyle = window.getComputedStyle(company_modal);
  const displayValue = computedStyle.display;

  if (displayValue === "none") {
    company_modal.style.display = "flex";
  } else if (displayValue === "flex") {
    company_modal.style.display = "none";
  }
}

async function updateCompany() {
  try {
    const response = await axios.put('http://127.0.0.1:8000/company/?company_id=1', updatedCompany.value,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  } catch (error) {
    console.error('Error updating the company:', error);
  }
  location.reload();
}

async function fetchInitialCompany() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/company/{id}?company_id=1')
  initialCompany.value = response.data
}

watch(initialCompany, (newCompany) => {
  if (newCompany) {
    updatedCompany.value = { ...newCompany };
  }
});

onMounted(async () => {
  await fetchInitialCompany();
});
</script>
