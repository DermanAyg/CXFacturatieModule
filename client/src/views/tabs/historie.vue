<template>
    <ion-page>
      <ion-content :fullscreen="true">
        
        <div id="modal_invoice" name="modal_invoice" class="md modal-default modal_invoice" style="display: none;">
          <div class="modal_invoice_wrapper">
            <div style="width: 95%;">
              <ion-grid>
                <ion-row>
                  <ion-col class="modal_invoice_wrapper_header_col_left">
                    <ion-icon @click="InvoiceToggler(null)" :icon="arrowBackOutline" style="font-size: 28px;color: #CD7130;cursor:pointer;"></ion-icon>
                  </ion-col>
                  <ion-col class="modal_invoice_wrapper_header_col_centered">
                    <ion-icon v-if="selectedInvoice?.status === 'open'" :icon="alertCircleSharp" style="font-size: 28px;color: #CD7130;"></ion-icon>
                    <ion-icon v-else :icon="checkmarkCircleSharp" style="font-size: 28px;color: #0AA34F;"></ion-icon>
                  </ion-col>
                  <ion-col class="modal_invoice_wrapper_header_col_right">
                    <ion-icon @click="InvoiceOptionsToggler()" :icon="ellipsisHorizontalOutline" style="font-size: 28px;color: #CD7130;cursor:pointer;"></ion-icon>
                  </ion-col>
                </ion-row>
              </ion-grid>
            </div>

            <!-- INVOICE OPTIONS MODAL BEGIN -->
            <div id="modal_invoice_options" name="modal_invoice_options" class="md modal-default modal_invoice_options" 
              style="display: none;">
              <div class="modal_invoice_options_wrapper">
                <div class="options_wrapper">
                  <ul class="options_wrapper_ul">
                    <li>Delen <span>@</span></li>
                    <li>Wijzigen <span>@</span></li>
                    <li>Verwijderen <span>@</span></li>
                  </ul>
                </div>
              </div>
            </div>
            <!-- INVOICE OPTIONS MODAL END -->

            <div style="width: 90%;margin-top: 25px;">
              <div id="invoice_wrapper" class="invoice_wrapper">
                <div class="invoice_status_wrapper">
                  <div>
                    <p class="invoice_wrapper_title">Factuur-{{ selectedInvoice?.number }}</p>
                    <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.lastname }}, {{ selectedInvoice?.uploaded_at }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div style="display:flex;width: 90%;margin-top: 25px;">
              <div style="background-color:white;height:500px;width:75%;">

                <iframe v-if="selectedInvoice?.fileUrl !== ''" id="invoiceIframe" width="100%" height="100%" frameborder="0"></iframe>
                <p style="color: black;font-size: 13px;padding: 0px 10px;" v-else>An error occured while trying to get the invoice, please contact the support team.</p>
                
              </div>
              <div style="display: flex;align-items: flex-end;">
                <ion-icon :icon="chatbubbleEllipsesSharp" @click="InvoiceRemarksToggler()" style="color: #CD7130;font-size:52px;margin-left: 25px;cursor: pointer;"></ion-icon>
              </div>

                <!-- MODAL REMARKS VIEWER BEGIN -->
                <div id="modal_invoice_remarks" name="modal_invoice_remarks" class="md modal-default modal_invoice_remarks" 
                  style="display: none;">
                  <div class="modal_invoice_remarks_wrapper">

                    <div style="margin-top: 15px;">
                      <ion-icon :icon="closeSharp" @click="InvoiceRemarksToggler()" style="color: #CD7130;font-size:52px;margin-left: 25px;cursor: pointer;"></ion-icon>
                    </div>
                    <div class="remark_wrapper">
                      
                      <div v-for="remark in selectedInvoice?.remarks" class="remark">
                        <p class="remark_username">{{ remark?.created_by }}<span class="remark_datetime">{{ remark?.created_at }}</span></p>
                        <p class="remark_content">{{ remark?.description }}</p>

                      </div>

                    </div>
                    <div class="remark_input_wrapper">
                      <input class="remark_input" id="remark" v-model="RemarkData.description" v-on:keyup.enter="postRemark()" name="remark" type="textarea" />
                    </div>

                  </div>
                </div>
                <!-- MODAL REMARKS VIEWER END -->

            </div>
          </div>
        </div>
        <!-- MODAL INVOICE VIEWER END -->

        <div id="container" class="container">
          <div class="section_block">
            <h2 class="section_title">Historie</h2>
            <div class="invoices_wrapper">

              <div v-if="isUser">
                <div v-for="invoice in loggedinuser.invoices">
                  <div v-if="invoice.status == 'closed'" id="invoice_wrapper" class="invoice_wrapper" @click="InvoiceToggler(invoice)">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.firstname }}, {{ invoice.last_activity }}</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-green" :icon="checkmarkCircleSharp"></ion-icon>
                    </div>
                  </div>
                  </div>
                </div>
              </div>
              <div v-if="isAdmin">
                <div v-for="invoice in initialInvoices">
                  <div v-if="invoice.status == 'closed'" id="invoice_wrapper" class="invoice_wrapper" @click="InvoiceToggler(invoice)">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">{{ userProfile?.firstname }} {{ userProfile?.firstname }}, {{ invoice.last_activity }}</p>
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

.vw10 {width: 10lvw}
.vw15 {width: 15vw}
.vw20 {width: 20vw}
.vw {width: 35vw}
.vw40 {width: 40vw}

.cus_section_block_options {
  min-width: 90%;
  min-height: 85px;
}
.section_block {
  min-width: 90%;
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
.invoices_wrapper {
  margin-top: 20px;
  overflow-y: scroll;
  max-height: 150px;
}
.invoice_wrapper {
  border-left: solid 7px orange;
  padding-left: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 7px;
  padding-top: 7px;
  cursor: pointer;
  margin-bottom: 15px;
}
.invoice_wrapper:hover {
  background-color: #232323;
}
.invoice_wrapper p {
  margin: 0;
}
.invoice_wrapper_title {
  margin-bottom: 7px!important;
  font-size: 18px;
}
.invoice_wrapper_subtitle {
  font-size: 13px;
  color: #A8AAAC;
}
.searchbar_wrapper {
  display: flex;
  padding-top: 15px;
  padding-bottom: 20px;
}
.searchbar_input {
  width: 100%;
  padding: 8px;
  background-color: #232222;
  border: solid 1px #ffffff15;
  border-radius: 0;
  color: #d5d5d5;
}
.searchbar_input:hover, .searchbar_input:active, .searchbar_input:focus {
  border: solid 1px #ffffff36!important;
  box-shadow: none!important;
}
.searchbar_icon_wrapper {
  width: 20%;
  display: flex;
  justify-content: center;
  padding: 8px;
  background-color: #E4833F;
}

.table_werkzaamheden {
  text-align: left !important;
}
.table_werkzaamheden_headers th {
  font-weight: normal!important;
  font-size: 13px;
  padding-bottom: 5px;
}
.table_werkzaamheden_columns input {
  background-color: transparent;
  border: solid 1px #ffffff42;
  color: #d5d5d5;
  font-size: 13px;
}
.table_werkzaamheden_columns .item-inner {
  border: none;
}
.werkzaamheden_btn_wrapper {
  position: relative;
  left: 81vw;
  top: 2vw;
}
.werkzaamheden_btn {
  height: 35px;
  width: 35px;
}
.factuur_submit {
  margin-right: 25px;
  margin-bottom: 25px;
  padding: 10px 40px;
  display: flex;
  justify-self: self-end;
  background-color: #E4833F;
  color: #FFF;
}
.invoice_status_wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
  flex-direction: row;
}
.modal_invoice {
  display: none;
  position: fixed;
  z-index: 20000;
  padding-top: 100px;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
  flex-direction: column;
  align-items: center;
}
.modal_invoice_wrapper {
  width: 70%;
  margin-top: 50px;
  min-height: 700px;
  display: flex;
  flex-flow: column;
  align-items: center;
  background-color: #292828;
  margin-bottom: 50px;
}
.modal_invoice_wrapper_header_col_centered {
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal_invoice_wrapper_header_col_left {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.modal_invoice_wrapper_header_col_right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.modal_invoice_remarks_wrapper {
  background-color: #1F1F1F;
  right: 17px;
  position: fixed;
  top: 55px;
  height: 90vh;
  width: 40%;
  display: flex;
  flex-flow: column;
  z-index: 1000000;
}
.remark_wrapper {
  display: flex;
  flex-flow: column;
  align-items: center;
  margin-top: 15px;
  overflow-y: scroll;
  max-height: 475px;
}
.remark {
  width: 90%;
  background-color: #292828;
  display: flex;
  flex-flow: column;
  padding-left: 10px;
  padding-right: 10px;
  margin-bottom: 15px;
}
.remark_username {
  font-size: 14px;
  display: flex;
  justify-content: space-between;
}
.remark_datetime {
  font-size: 12px;
  color: #FFFFFF80;
}
.remark_content {
  font-size: 13px;
}
.remark_input_wrapper {
  position: absolute;
  bottom: 35px;
  min-height: 50px;
  background-color: #292828;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.remark_input {
  background-color: #373737;
  border: solid 1px #0D1A331A;
  width: 95%;
  padding: 7px 10px;
  font-size: 13px;
}
.invoice_back_btn {
  position: absolute;
  font-size: 16px;
  top: 20px;
  left: 15px;
  z-index: 1000;
  cursor: pointer;
  color: #E4833F!important;
  font-size: 20px!important;
}
.modal_invoice_options {
  display: flex;
  position: absolute;
  margin-top: 50px;
  margin-left: 30vw;
  z-index: 100000;
  background-color: #1F1F1F;
}
.options_wrapper_ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}
.options_wrapper_ul li {
  display: flex;
  justify-content: space-between;
  width: 170px;
  padding: 7px 7px;
}
.options_wrapper_ul li:hover {
  cursor: pointer;
  background-color: #1c1c1c;
}
.cus_section_block_options {
  min-width: 90%;
  min-height: 85px;
}
.section_block {
  min-width: 90%;
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
.invoices_wrapper {
  margin-top: 20px;
  overflow-y: scroll;
  max-height: 150px;
}
.invoice_wrapper {
  border-left: solid 7px orange;
  padding-left: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 7px;
  padding-top: 7px;
  cursor: pointer;
  margin-bottom: 15px;
}
.invoice_wrapper:hover {
  background-color: #232323;
}
.invoice_wrapper p {
  margin: 0;
}
.invoice_wrapper_title {
  margin-bottom: 7px!important;
  font-size: 18px;
}
.invoice_wrapper_subtitle {
  font-size: 13px;
  color: #A8AAAC;
}
.searchbar_wrapper {
  display: flex;
  padding-top: 15px;
  padding-bottom: 20px;
}
.searchbar_input {
  width: 100%;
  padding: 8px;
  background-color: #232222;
  border: solid 1px #ffffff15;
  border-radius: 0;
  color: #d5d5d5;
}
.searchbar_input:hover, .searchbar_input:active, .searchbar_input:focus {
  border: solid 1px #ffffff36!important;
  box-shadow: none!important;
}
.searchbar_icon_wrapper {
  width: 20%;
  display: flex;
  justify-content: center;
  padding: 8px;
  background-color: #E4833F;
}

.table_werkzaamheden {
  text-align: left !important;
}
.table_werkzaamheden_headers th {
  font-weight: normal!important;
  font-size: 13px;
  padding-bottom: 5px;
}
.table_werkzaamheden_columns input {
  background-color: transparent;
  border: solid 1px #ffffff42;
  color: #d5d5d5;
  font-size: 13px;
}
.table_werkzaamheden_columns .item-inner {
  border: none;
}
.werkzaamheden_btn_wrapper {
  position: relative;
  left: 81vw;
  top: 2vw;
}
.werkzaamheden_btn {
  height: 35px;
  width: 35px;
}
.factuur_submit {
  margin-right: 25px;
  margin-bottom: 25px;
  padding: 10px 40px;
  display: flex;
  justify-self: self-end;
  background-color: #E4833F;
  color: #FFF;
}
.invoice_status_wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
  flex-direction: row;
}
.modal_invoice {
  display: none;
  position: fixed;
  z-index: 20000;
  padding-top: 100px;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
  flex-direction: column;
  align-items: center;
}
.modal_invoice_wrapper {
  width: 70%;
  margin-top: 50px;
  min-height: 700px;
  display: flex;
  flex-flow: column;
  align-items: center;
  background-color: #292828;
  margin-bottom: 50px;
}
.modal_invoice_wrapper_header_col_centered {
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal_invoice_wrapper_header_col_left {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.modal_invoice_wrapper_header_col_right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.modal_invoice_remarks_wrapper {
  background-color: #1F1F1F;
  right: 17px;
  position: fixed;
  top: 55px;
  height: 90vh;
  width: 40%;
  display: flex;
  flex-flow: column;
  z-index: 1000000;
}
.remark_wrapper {
  display: flex;
  flex-flow: column;
  align-items: center;
  margin-top: 15px;
  overflow-y: scroll;
  max-height: 475px;
}
.remark {
  width: 90%;
  background-color: #292828;
  display: flex;
  flex-flow: column;
  padding-left: 10px;
  padding-right: 10px;
  margin-bottom: 15px;
}
.remark_username {
  font-size: 14px;
  display: flex;
  justify-content: space-between;
}
.remark_datetime {
  font-size: 12px;
  color: #FFFFFF80;
}
.remark_content {
  font-size: 13px;
}
.remark_input_wrapper {
  position: absolute;
  bottom: 35px;
  min-height: 50px;
  background-color: #292828;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.remark_input {
  background-color: #373737;
  border: solid 1px #0D1A331A;
  width: 95%;
  padding: 7px 10px;
  font-size: 13px;
}
.invoice_back_btn {
  position: absolute;
  font-size: 16px;
  top: 20px;
  left: 15px;
  z-index: 1000;
  cursor: pointer;
  color: #E4833F!important;
  font-size: 20px!important;
}
.modal_invoice_options {
  display: flex;
  position: absolute;
  margin-top: 50px;
  margin-left: 30vw;
  z-index: 100000;
  background-color: #1F1F1F;
}
.options_wrapper_ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}
.options_wrapper_ul li {
  display: flex;
  justify-content: space-between;
  width: 170px;
  padding: 7px 7px;
}
.options_wrapper_ul li:hover {
  cursor: pointer;
  background-color: #1c1c1c;
}
</style>
<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, onIonViewWillEnter, onIonViewDidLeave, onIonViewWillLeave } from '@ionic/vue';
import { ref, onMounted, watch, computed  } from 'vue';
import axios from 'axios'
import { checkmarkCircleSharp, arrowBackOutline, chatbubbleEllipsesSharp, closeSharp, ellipsisHorizontalOutline, alertCircleSharp } from 'ionicons/icons';
import { useAuth0 } from '@auth0/auth0-vue';

const modal = ref();
const input = ref();
const searchInvoice = ref();
let selectedInvoice = ref();

const initialInvoices = ref();
const loggedinuser = ref()
const userProfile = ref()

const isAdmin = computed(() => loggedinuser.value?.role === 'admin');
const isUser = computed(() => loggedinuser.value?.role === 'user');

const auth0 = useAuth0();
const { user, isAuthenticated } = useAuth0();

const cancel = () => modal.value.$el.dismiss(null, 'cancel');

const date = new Date();
let day = date.getDate();
let month = date.getMonth() + 1;
let year = date.getFullYear();
let hour = date.getHours();
let minutes = date.getMinutes();

const RemarkData = ref({
    "description": "",
    "created_at": `${day}-${month}-${year} ${hour}:${minutes}`,
    "created_by": userProfile.value?.firstname + " " + userProfile.value?.lastname,
    "status": "pending",
    "invoice_id": selectedInvoice.value?.id
  })

function InvoiceToggler(invoice: any) {
  var modal = document.getElementById("modal_invoice");
  selectedInvoice.value = invoice;

  if (invoice?.fileUrl) {
    // Set the iframe source to the file URL
    document.getElementById('invoiceIframe').src = invoice.fileUrl;
  }

  if (modal?.style.display === "none") {
    modal.style.display = "flex";
  } else if (modal?.style.display === "flex") {
    modal.style.display = "none";
  }
}

function convertBase64ToPdfUrl(base64String: any) {
  const binary = atob(base64String); // Decode the base64 string
  const array = [];
  const emptyFileSignature = "c3RyaW5n"; // Base64 for "string"
  
  if (base64String.includes(emptyFileSignature)) {
    return '';
  }

  for (let i = 0; i < binary.length; i++) {
    array.push(binary.charCodeAt(i));
  }
  const blob = new Blob([new Uint8Array(array)], { type: 'application/pdf' });
  const url = URL.createObjectURL(blob); // Return the URL for the blob

  return `${url}#zoom=50`;
}

function InvoiceOptionsToggler() {
  var options_modal = document.getElementById("modal_invoice_options");

  if (options_modal?.style.display == "none") {
    options_modal.style.display = "flex";
  } else if (options_modal?.style.display == "flex") {
    options_modal.style.display = "none";
  }
}

function InvoiceRemarksToggler() {
  var remarks_modal = document.getElementById("modal_invoice_remarks");

  if (remarks_modal?.style.display === "none") {
    remarks_modal.style.display = "flex";
  } else if (remarks_modal?.style.display === "flex") {
    remarks_modal.style.display = "none";
  }
}

async function fetchInitialInvoices() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/invoice/')
  initialInvoices.value = response.data
}

async function fetchLoggedInUser() {
  const response = await axios.get<[]>('http://127.0.0.1:8000/userbyemail/' + user.value?.email)
  return response.data
}

async function fetchUserProfile(profileId: any) {
    const response = await axios.get<[]>('http://127.0.0.1:8000/profile/{id}?profile_id=' + profileId)
    return response.data
}

function parseDate(dateString: string) {
  const [datePart, timePart] = dateString.split(' ');
  const [day, month, year] = datePart.split('-').map(Number);
  const [hours, minutes, seconds] = timePart.split(':').map(Number);

  return new Date(year, month - 1, day, hours, minutes, seconds);
}

async function postRemark() {
  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/remark/', RemarkData.value,
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

watch([isAuthenticated, user], async ([authenticated, userInfo]) => {
  if (authenticated && userInfo?.email) {
    loggedinuser.value = await fetchLoggedInUser();
    userProfile.value = await fetchUserProfile(loggedinuser.value.profile_id);

    loggedinuser.value.invoices.forEach((invoice: { file: any; fileUrl: string; }) => {
      if (invoice.file) {
        invoice.fileUrl = convertBase64ToPdfUrl(invoice.file);
      }
    });

  }
});

const loading = ref(true);
watch(loggedinuser, (newVal) => {
  if (newVal) loading.value = false;
});

watch(
() => selectedInvoice.value?.id,
(newId) => {
  if (newId) {
    RemarkData.value['invoice_id'] = newId;
  }
});

watch(
() => userProfile.value,
(newProfile) => {
  if (newProfile) {
    const firstname = newProfile.firstname;
    const lastname = newProfile.lastname;
    RemarkData.value['created_by'] = `${firstname} ${lastname}`.trim();
  }
});

onIonViewWillLeave(async () => {
  location.reload();
})

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
