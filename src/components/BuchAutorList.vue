<template>
    <div>
      <h2>Buch-Autor-Verknüpfungen</h2>
      <ul>
        <li v-for="buchAutor in buchAutoren" :key="buchAutor.id">
          {{ buchAutor.buch.title }} - {{ buchAutor.autor.name }}
          <button @click="deleteBuchAutor(buchAutor.id)">Löschen</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        buchAutoren: []  // Liste der Buch-Autor-Verknüpfungen
      };
    },
    created() {
      this.fetchBuchAutoren();  // Ruft die Buch-Autor-Verknüpfungen ab
    },
    methods: {
      async fetchBuchAutoren() {
        try {
          const response = await axios.get('/buchautor');  // GET-Anfrage an den Endpunkt '/buchautor'
          this.buchAutoren = response.data;  // Speichert die Buch-Autor-Verknüpfungen
        } catch (error) {
          console.error('Fehler beim Laden der Buch-Autor-Verknüpfungen:', error);
        }
      },
      async deleteBuchAutor(id) {
        try {
          await axios.delete(`/buchautor/${id}`);  // DELETE-Anfrage an den Endpunkt '/buchautor/{id}'
          this.fetchBuchAutoren();  // Lädt die Liste der Buch-Autor-Verknüpfungen nach dem Löschen neu
        } catch (error) {
          console.error('Fehler beim Löschen der Buch-Autor-Verknüpfung:', error);
        }
      }
    }
  };
  </script>
  