<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <!-- TODO: add date for recent invoices, 5days<invoice_date = recent invoice -->
        <div v-if="isAdmin" id="container" class="container">
          <div class="section_block">
            <h2 class="section_title">Recente facturen</h2>
            <div class="invoices_wrapper">
              <div>
                <div v-for="invoice in initialInvoices">
                  <div v-if="invoice.status == 'open'" class="invoice_wrapper">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.lastname }}, {{ parseDateToString(invoice.last_activity) }}</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-orange" :icon="alertCircleSharp"></ion-icon>
                    </div>
                  </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="section_block">
            <h2 class="section_title">Open facturen</h2>
            <div class="invoices_wrapper">
              <div>
                <div v-for="invoice in initialInvoices">
                  <div v-if="invoice.status == 'open'" class="invoice_wrapper">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.lastname }}, {{ parseDateToString(invoice.last_activity) }}</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-orange" :icon="alertCircleSharp"></ion-icon>
                    </div>
                  </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="isUser" id="container" class="container">
          <div class="section_block">
            <h2 class="section_title">Mijn facturen</h2>
            <div class="invoices_wrapper">
              <div>
                <div v-for="invoice in initialInvoices">
                  <div v-if="invoice.status == 'closed'" class="invoice_wrapper">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.lastname }}, {{ parseDateToString(invoice.last_activity) }}</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-green" :icon="checkmarkCircleSharp"></ion-icon>
                    </div>
                  </div>
                  </div>
                  <div v-else-if="invoice.status == 'open'" class="invoice_wrapper">
                    <div class="invoice_status_wrapper">
                      <div>
                        <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                        <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.lastname }}, {{ parseDateToString(invoice.last_activity) }}</p>
                      </div>
                      <div>
                        <ion-icon class="invoice-icon-orange" :icon="alertCircleSharp"></ion-icon>
                      </div>
                    </div>
                  </div>
                </div>
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
.invoices_wrapper {
  max-height: 470px!important;
}
</style>
<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonSpinner, onIonViewWillEnter } from '@ionic/vue';
import { ref, onMounted, watch, computed  } from 'vue';
import axios from 'axios'
import { alertCircleSharp, checkmarkCircleSharp } from 'ionicons/icons';
import { useAuth0 } from '@auth0/auth0-vue';

const initialInvoices = ref();
const loggedinuser = ref()
const userProfile = ref()

const isAdmin = computed(() => loggedinuser.value?.role === 'admin');
const isUser = computed(() => loggedinuser.value?.role === 'user');

const auth0 = useAuth0();
const { user, isAuthenticated } = useAuth0();

async function fetchInitialInvoices() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/invoice/')
  initialInvoices.value = response.data
}

async function fetchLoggedInUser() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/userbyemail/' + user.value?.email)
  return response.data
}

async function fetchUserProfile(profileId: any) {
    const response = await axios.get<[]>('http://127.0.0.1:8000/profile/{id}?profile_id=2')
    return response.data
}

function parseDate(dateString: string) {
  const [datePart, timePart] = dateString.split(' ');
  const [day, month, year] = datePart.split('-').map(Number);
  const [hours, minutes, seconds] = timePart.split(':').map(Number);

  return new Date(year, month - 1, day, hours, minutes, seconds);
}

function parseDateToString(dateString: string) {
  const [datePart, timePart] = dateString.split(' ');
  const [day, month, year] = datePart.split('-').map(Number);
  const [hours, minutes, seconds] = timePart.split(':').map(Number);

  return `${day}-${month}-${year}, ${hours}:${minutes}`;
}

onIonViewWillEnter(async () => {
  loggedinuser.value = null;
  userProfile.value = null;
  initialInvoices.value = null;

  if (isAuthenticated.value && user.value?.email) {
    loggedinuser.value = await fetchLoggedInUser();
    userProfile.value = await fetchUserProfile(loggedinuser.value.profile_id);
  }
  await fetchInitialInvoices();
  initialInvoices.value.sort((a: any, b: any) => {
    const dateA: any = parseDate(a.last_activity);
    const dateB: any = parseDate(b.last_activity);
    return dateB - dateA;
  });
});

watch([isAuthenticated, user], async ([authenticated, userInfo]) => {
  if (authenticated && userInfo?.email) {
    loggedinuser.value = await fetchLoggedInUser();
    userProfile.value = await fetchUserProfile(loggedinuser.value.profile_id);
  }
});

</script>