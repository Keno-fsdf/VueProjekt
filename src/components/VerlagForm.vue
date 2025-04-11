<template>
    <div>
      <h2>{{ isEdit ? 'Verlag bearbeiten' : 'Neuen Verlag hinzufügen' }}</h2>
      <form @submit.prevent="submitForm">
        <input v-model="verlag.name" placeholder="Verlag Name" required />
        <button type="submit">{{ isEdit ? 'Speichern' : 'Hinzufügen' }}</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: ['verlagId'],
    data() {
      return {
        verlag: {
          name: ''
        },
        isEdit: false
      };
    },
    created() {
      if (this.verlagId) {
        this.isEdit = true;
        this.fetchVerlag();
      }
    },
    methods: {
      async fetchVerlag() {
        try {
          const response = await axios.get(`/verlag/${this.verlagId}`);
          this.verlag = response.data;
        } catch (error) {
          console.error('Fehler beim Laden des Verlags:', error);
        }
      },
      async submitForm() {
        try {
          if (this.isEdit) {
            await axios.put(`/verlag/${this.verlagId}`, this.verlag);
          } else {
            await axios.post('/verlag', this.verlag);
          }
          this.$router.push('/'); // Navigiere zurück zur Hauptansicht nach dem Absenden
        } catch (error) {
          console.error('Fehler beim Speichern des Verlags:', error);
        }
      }
    }
  };
  </script>
  