<template>
    <ion-page>
      <ion-content :fullscreen="true">
        <div id="container" class="container">
          <div class="section_block">
            <h2 class="section_title">Historie</h2>
            <div class="invoices_wrapper">
              <div>
                <div v-for="invoice in initialInvoices">
                  <div v-if="invoice.status == 'closed'" class="invoice_wrapper">
                    <!-- <pre>{{ invoice }}</pre> -->

                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">{{ loggedinuser.firstname }} {{ loggedinuser.lastname }}, {{ parseDateToString(invoice.last_activity) }}</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-green" :icon="checkmarkCircleSharp"></ion-icon>
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
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
import { ref, onMounted  } from 'vue';
import axios from 'axios'
import { checkmarkCircleSharp } from 'ionicons/icons';

const initialInvoices = ref();
const loggedinuser = ref({
  "email": "johnvisser_123@hotmail.com",
  "firstname": "John",
  "lastname": "Visser",
  "role": "user",
})

async function fetchInitialInvoices() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/invoice/')
  initialInvoices.value = response.data
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

onMounted(async () => {
  await fetchInitialInvoices();
  initialInvoices.value.sort((a: any, b: any) => {
    const dateA: any = parseDate(a.last_activity);
    const dateB: any = parseDate(b.last_activity);
    return dateB - dateA;
  });
});

</script>
