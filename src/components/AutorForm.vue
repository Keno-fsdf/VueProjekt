<template>
    <div>
      <h2>{{ isEdit ? 'Autor bearbeiten' : 'Neuen Autor hinzufügen' }}</h2>
      <form @submit.prevent="submitForm">
        <input v-model="autor.name" placeholder="Autor Name" required />
        <button type="submit">{{ isEdit ? 'Speichern' : 'Hinzufügen' }}</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: ['autorId'],
    data() {
      return {
        autor: {
          name: ''
        },
        isEdit: false
      };
    },
    created() {
      if (this.autorId) {
        this.isEdit = true;
        this.fetchAutor();
      }
    },
    methods: {
      async fetchAutor() {
        try {
          const response = await axios.get(`/autor/${this.autorId}`);
          this.autor = response.data;
        } catch (error) {
          console.error('Fehler beim Laden des Autors:', error);
        }
      },
      async submitForm() {
        try {
          if (this.isEdit) {
            await axios.put(`/autor/${this.autorId}`, this.autor);
          } else {
            await axios.post('/autor', this.autor);
          }
          this.$router.push('/'); // Navigiere zurück zur Hauptansicht nach dem Absenden
        } catch (error) {
          console.error('Fehler beim Speichern des Autors:', error);
        }
      }
    }
  };
  </script>
  