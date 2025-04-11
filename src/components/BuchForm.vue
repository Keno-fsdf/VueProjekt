<template>
    <div>
      <h2>{{ isEdit ? 'Buch Bearbeiten' : 'Buch Hinzufügen' }}</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="title">Titel</label>
          <input type="text" v-model="buch.title" id="title" required />
        </div>
        <div>
          <label for="verlag">Verlag</label>
          <input type="text" v-model="buch.verlag" id="verlag" required />
        </div>
        <button type="submit">{{ isEdit ? 'Ändern' : 'Hinzufügen' }}</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        buch: { title: '', verlag: '' },  // Buchdaten (Titel und Verlag)
        isEdit: false,  // Flag, ob es sich um die Bearbeitung eines Buches handelt
      };
    },
    created() {
      if (this.$route.params.id) {
        this.isEdit = true;
        this.fetchBuch(this.$route.params.id);  // Ruft das Buch bei der Bearbeitung ab
      }
    },
    methods: {
      async fetchBuch(id) {
        try {
          const response = await axios.get(`/buch/${id}`);  // Holt das Buch von der API
          this.buch = response.data;
        } catch (error) {
          console.error('Fehler beim Abrufen des Buchs:', error);
        }
      },
      async submitForm() {
        if (this.isEdit) {
          await this.updateBuch();  // PUT-Anfrage für das Bearbeiten eines Buches
        } else {
          await this.createBuch();  // POST-Anfrage für das Erstellen eines neuen Buches
        }
      },
      async createBuch() {
        try {
          await axios.post('/buch', this.buch);  // POST-Anfrage für das Hinzufügen eines Buchs
          this.$router.push('/');  // Weiterleitung nach dem Hinzufügen
        } catch (error) {
          console.error('Fehler beim Hinzufügen des Buches:', error);
        }
      },
      async updateBuch() {
        try {
          await axios.put(`/buch/${this.buch.id}`, this.buch);  // PUT-Anfrage für das Bearbeiten eines Buchs
          this.$router.push('/');  // Weiterleitung nach dem Bearbeiten
        } catch (error) {
          console.error('Fehler beim Bearbeiten des Buches:', error);
        }
      }
    }
  };
  </script>
  