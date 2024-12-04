<template>
    <ion-page>
      <ion-content :fullscreen="true">
        <div id="container" class="container">

          <!-- MODAL INVOICE GENERATION BEGIN -->
          <ion-modal ref="modal" trigger="factuur_aanmaak_modal" @willDismiss="onWillDismiss">
            <ion-header>
              <ion-toolbar>
                <ion-title style="text-align: center;">Factuur aanmaken</ion-title>
              </ion-toolbar>
            </ion-header>
            <ion-content class="ion-padding">
              <ion-list>
                <ion-item>
                  <ion-input v-model="FormData['bedrijfsnaam']" label="Bedrijfsnaam" label-placement="stacked" ref="input" type="text" placeholder="bedrijfsnaam"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['voornaam']" label="Voornaam" label-placement="stacked" ref="input" type="text" placeholder="voornaam"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['achternaam']" label="Achternaam" label-placement="stacked" ref="input" type="text" placeholder="achternaam"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['straat']" label="Straat" label-placement="stacked" ref="input" type="text" placeholder="straat"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['huisnummer']" label="Huisnummer" label-placement="stacked" ref="input" type="text" placeholder="huisnummer"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['postcode']" label="Postcode" label-placement="stacked" ref="input" type="text" placeholder="postcode"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['plaats']" label="Plaats" label-placement="stacked" ref="input" type="text" placeholder="plaats"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['klant-naam']" label="Klant naam" label-placement="stacked" ref="input" type="text" placeholder="naam"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['klant-straat']" label="klant straat" label-placement="stacked" ref="input" type="text" placeholder="straat"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['klant-huisnummer']" label="Klant huisnummer" label-placement="stacked" ref="input" type="text" placeholder="huisnummer"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['klant-postcode']" label="Klant postcode" label-placement="stacked" ref="input" type="text" placeholder="postcode"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['klant-plaats']" label="Klant plaats" label-placement="stacked" ref="input" type="text" placeholder="plaats"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['klant-kvk']" label="Klant KVK" label-placement="stacked" ref="input" type="text" placeholder="kvk nummer"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['factuurnummer']" label="Factuurnummer" label-placement="stacked" ref="input" type="text" placeholder="factuurnummer"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['factuurdatum']" label="Factuurdatum" label-placement="stacked" ref="input" type="text" placeholder="factuurdatum"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['vervaldatum']" label="Vervaldatum" label-placement="stacked" ref="input" type="text" placeholder="vervaldatum"></ion-input>
                </ion-item>

                <ion-item>
                  <ion-input v-model="FormData['btw-nummer']" label="BTW nummer" label-placement="stacked" ref="input" type="text" placeholder="btw nummer"></ion-input>
                </ion-item>

                <div style="padding-bottom: 50px;">
                  <p style="font-size: 13px;padding-left: 15px;">Werkzaamheden</p>
                  <ion-item class="table_werkzaamheden_wrapper">
                    <table class="table_werkzaamheden">
                      <tr class="table_werkzaamheden_headers">
                        <th class="vw15">Hoeveelheid</th>
                        <th class="vw40">Omschrijving</th>
                        <th class="vw10">Btw</th>
                        <th class="vw20">Prijs</th>
                      </tr>
                      <tr
                        v-for="(product, index) in FormData['producten']"
                        :key="index"
                        class="table_werkzaamheden_columns"
                      >
                        <td class="vw15">
                          <input
                            class="vw15"
                            type="number"
                            v-model="product.hoeveelheid"
                          />
                        </td>
                        <td class="vw40">
                          <input
                            class="vw40"
                            type="text"
                            v-model="product.omschrijving"
                          />
                        </td>
                        <td class="vw10">
                          <input
                            class="vw10"
                            type="text"
                            v-model="product.btw"
                          />
                        </td>
                        <td class="vw20">
                          <input
                            class="vw20"
                            type="number"
                            v-model="product.prijs"
                          />
                        </td>
                      </tr>
                    </table>

                  </ion-item>
                  <ion-fab class="werkzaamheden_btn_wrapper">
                    <ion-fab-button
                      class="werkzaamheden_btn"
                      style="--background: #E4833F;"
                      @click="addRow"
                    >
                      <ion-icon :icon="add" style="color: #FFF;"></ion-icon>
                    </ion-fab-button>
                  </ion-fab>
                </div>
                <button class="factuur_submit" @click="postGenerateInvoice()">Aanmaken</button>
              </ion-list>
            </ion-content>
          </ion-modal>
          <!-- MODAL INVOICE GENERATION END -->

          <!-- MODAL INVOICE VIEWER BEGIN -->
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
                      <ion-icon :icon="ellipsisHorizontalOutline" style="font-size: 28px;color: #CD7130;cursor:pointer;"></ion-icon>
                    </ion-col>
                  </ion-row>
                </ion-grid>
              </div>
              <div style="width: 90%;margin-top: 25px;">
                <div class="invoice_wrapper">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ selectedInvoice?.number }}</p>
                      <p class="invoice_wrapper_subtitle">Derman Aygun, 29-11-2024, vrijdag 11:36</p>
                    </div>
                  </div>
                </div>
              </div>
              <div style="display:flex;width: 90%;margin-top: 25px;">
                <div style="background-color:white;height:500px;width:75%;">

                  <iframe src="/test_invoice.pdf#zoom=67" width="100%" height="100%" frameborder="0"></iframe>

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

                        <div class="remark">
                          <p class="remark_username">Derman Aygun<span class="remark_datetime">18:57 - 30/10/24</span></p>
                          <p class="remark_content">Dit is een voorbeeld opmerking die door mij is gemaakt. Graag het volgende wijzigen aan uw factuur, naam, achternaam en adres.</p>
                        </div>
                        <div class="remark">
                          <p class="remark_username">Derman Aygun<span class="remark_datetime">18:57 - 30/10/24</span></p>
                          <p class="remark_content">Dit is een voorbeeld opmerking die door mij is gemaakt. Graag het volgende wijzigen aan uw factuur, naam, achternaam en adres.</p>
                        </div>
                        <div class="remark">
                          <p class="remark_username">Derman Aygun<span class="remark_datetime">18:57 - 30/10/24</span></p>
                          <p class="remark_content">Dit is een voorbeeld opmerking die door mij is gemaakt. Graag het volgende wijzigen aan uw factuur, naam, achternaam en adres.</p>
                        </div>
                        <div class="remark">
                          <p class="remark_username">Derman Aygun<span class="remark_datetime">18:57 - 30/10/24</span></p>
                          <p class="remark_content">Dit is een voorbeeld opmerking die door mij is gemaakt. Graag het volgende wijzigen aan uw factuur, naam, achternaam en adres.</p>
                        </div>
                        <div class="remark">
                          <p class="remark_username">Derman Aygun<span class="remark_datetime">18:57 - 30/10/24</span></p>
                          <p class="remark_content">Dit is een voorbeeld opmerking die door mij is gemaakt. Graag het volgende wijzigen aan uw factuur, naam, achternaam en adres.</p>
                        </div>
                        <div class="remark">
                          <p class="remark_username">Derman Aygun<span class="remark_datetime">18:57 - 30/10/24</span></p>
                          <p class="remark_content">Dit is een voorbeeld opmerking die door mij is gemaakt. Graag het volgende wijzigen aan uw factuur, naam, achternaam en adres.</p>
                        </div>

                      </div>
                      <div class="remark_input_wrapper">
                        <input class="remark_input" type="textarea" />
                      </div>

                    </div>
                  </div>
                  <!-- MODAL REMARKS VIEWER END -->

              </div>
            </div>
          </div>
          <!-- MODAL INVOICE VIEWER END -->

          <!-- PAGE CONTENT BEGIN -->
          <div class="cus_section_block_options">
            <div style="display:flex; justify-content: end;">
              <ion-fab>
                <ion-fab-button id="factuur_aanmaak_modal" style="--background: #E4833F;">
                  <ion-icon :icon="add" style="color: #FFF;"></ion-icon>
                </ion-fab-button>
              </ion-fab>
            </div>
          </div>

          <div class="section_block">
            <h2 class="section_title">Factuur zoeken</h2>
            <div class="searchbar_wrapper" style="display: flex;">
              <input v-model="searchInvoice" class="searchbar_input" type="text" name="search_invoice" />
            </div>
          </div>

          <div class="section_block">
            <h2 class="section_title">Open facturen</h2>
            <div class="invoices_wrapper">

              <template v-if="searchInvoice">
                <div>
                    <div v-for="invoice in initialInvoices">
                      <div v-if="invoice['number'].includes(searchInvoice) && invoice.status == 'open'" class="invoice_wrapper" @click="InvoiceToggler(invoice)">

                        <div class="invoice_status_wrapper">
                          <div>
                            <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                            <p class="invoice_wrapper_subtitle">Derman Aygun, 29-11-2024, vrijdag 11:36</p>
                          </div>
                          <div>
                            <ion-icon class="invoice-icon-green" :icon="alertCircleSharp" style="font-size: 28px;color: #CD7130;padding-right: 25px;padding-top: 4px;"></ion-icon>
                          </div>
                        </div>

                      </div>
                    </div>
                  </div>
              </template>
              
              <template v-else v-for="invoice in initialInvoices">
                <div v-if="invoice.status == 'open'" class="invoice_wrapper" @click="InvoiceToggler(invoice)">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">Derman Aygun, 29-11-2024, vrijdag 11:36</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-green" :icon="alertCircleSharp" style="font-size: 28px;color: #CD7130;padding-right: 25px;padding-top: 4px;"></ion-icon>
                    </div>
                  </div>
                </div>
              </template>

            </div>
          </div>
          
          <div class="section_block">
            <h2 class="section_title">Gesloten facturen</h2>
            <div class="invoices_wrapper">

              <template v-if="searchInvoice">
                <div>
                    <div v-for="invoice in initialInvoices">
                      <div v-if="invoice['number'].includes(searchInvoice)" class="invoice_wrapper" @click="InvoiceToggler(invoice)">

                      <div class="invoice_status_wrapper">
                        <div>
                          <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                          <p class="invoice_wrapper_subtitle">Derman Aygun, 29-11-2024, vrijdag 11:36</p>
                        </div>
                        <div>
                          <ion-icon class="invoice-icon-green" :icon="checkmarkCircleSharp" style="font-size: 28px;color: #0AA34F;padding-right: 25px;padding-top: 4px;"></ion-icon>
                        </div>
                      </div>

                      </div>
                    </div>
                  </div>
              </template>
              
              <template v-else v-for="invoice in initialInvoices">
                <div v-if="invoice.status == 'closed'" class="invoice_wrapper" @click="InvoiceToggler(invoice)">
                  <div class="invoice_status_wrapper">
                    <div>
                      <p class="invoice_wrapper_title">Factuur-{{ invoice.number }}</p>
                      <p class="invoice_wrapper_subtitle">Derman Aygun, 29-11-2024, vrijdag 11:36</p>
                    </div>
                    <div>
                      <ion-icon class="invoice-icon-green" :icon="checkmarkCircleSharp" style="font-size: 28px;color: #0AA34F;padding-right: 25px;padding-top: 4px;"></ion-icon>
                    </div>
                  </div>
                </div>
              </template>

            </div>
          </div>
        </div>
      </ion-content>
    </ion-page>
  </template>
<style>
.vw10 {width: 10vw !important;}
.vw15 {width: 15vw !important;}
.vw20 {width: 20vw !important;}
.vw40 {width: 40vw !important;}

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
}
.remark_wrapper {
  display: flex;
  flex-flow: column;
  align-items: center;
  margin-top: 15px;
  overflow-y: scroll;
  max-height: 675px;
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
  bottom: 15px;
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
    IonInput,
    IonList } from '@ionic/vue';
  import { OverlayEventDetail } from '@ionic/core/components';
  import { add, alertCircleSharp, arrowBackOutline, arrowForwardOutline, chatbubbleEllipsesOutline, chatbubbleEllipsesSharp, checkmarkCircleSharp, closeSharp, ellipsisHorizontalOutline } from 'ionicons/icons';
  import { ref, onMounted  } from 'vue';
  import axios from 'axios'

  const modal = ref();
  const input = ref();
  const searchInvoice = ref();
  const initialInvoices = ref();
  let selectedInvoice = ref();
  const FormData = ref({
    "bedrijfsnaam": "",
    "voornaam": "",
    "achternaam": "",
    "straat": "",
    "huisnummer": "",
    "postcode": "",
    "plaats": "",
    "klant-naam": "",
    "klant-straat": "",
    "klant-huisnummer": "",
    "klant-postcode": "",
    "klant-plaats": "",
    "klant-kvk": "",
    "factuurnummer": "",
    "factuurdatum": "",
    "vervaldatum": "",
    "btw-nummer": "",
    "producten": [{}],
  })

  function InvoiceToggler(invoice: any) {
    var modal = document.getElementById("modal_invoice");
    selectedInvoice.value = invoice;

    if (modal?.style.display === "none") {
      modal.style.display = "flex";
    } else if (modal?.style.display === "flex") {
      modal.style.display = "none";
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

  function addRow() {
    FormData.value["producten"].push({
      hoeveelheid: "",
      omschrijving: "",
      btw: "",
      prijs: "",
    })
  };

  async function postGenerateInvoice() {
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/generate-invoice/', FormData.value,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    } catch (error) {
      console.error("Error:", error);
    }
  }

  onMounted(async () => {
        await fetchInitialInvoices()
    })

</script>
