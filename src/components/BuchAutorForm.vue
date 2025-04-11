f <template>
    <div>
      <h2>{{ isEdit ? 'Buch-Autor-Verknüpfung Bearbeiten' : 'Buch-Autor-Verknüpfung Hinzufügen' }}</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="buch">Buch</label>
          <select v-model="buchAutor.buchId" id="buch" required>
            <option v-for="buch in buecher" :key="buch.id" :value="buch.id">{{ buch.title }}</option>
          </select>
        </div>
        <div>
          <label for="autor">Autor</label>
          <select v-model="buchAutor.autorId" id="autor" required>
            <option v-for="autor in autoren" :key="autor.id" :value="autor.id">{{ autor.name }}</option>
          </select>
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
        buchAutor: { buchId: '', autorId: '' },  // Buch-Autor-Verknüpfung (IDs von Buch und Autor)
        isEdit: false,  // Flag für Bearbeitung
        buecher: [],  // Liste der Bücher
        autoren: []  // Liste der Autoren
      };
    },
    created() {
      // Ruft die Daten ab, wenn die Komponente erstellt wird
      this.fetchBuecher();
      this.fetchAutoren();
      // Wenn eine ID in der URL vorhanden ist, handelt es sich um eine Bearbeitung
      if (this.$route.params.id) {
        this.isEdit = true;
        this.fetchBuchAutor(this.$route.params.id);  // Ruft die Buch-Autor-Verknüpfung für die Bearbeitung ab
      }
    },
    methods: {
      // Holt alle Bücher aus der API
      async fetchBuecher() {
        try {
          const response = await axios.get('/buch');
          this.buecher = response.data;
        } catch (error) {
          console.error('Fehler beim Laden der Bücher:', error);
        }
      },
      // Holt alle Autoren aus der API
      async fetchAutoren() {
        try {
          const response = await axios.get('/autor');
          this.autoren = response.data;
        } catch (error) {
          console.error('Fehler beim Laden der Autoren:', error);
        }
      },
      // Holt eine spezifische Buch-Autor-Verknüpfung zur Bearbeitung
      async fetchBuchAutor(id) {
        try {
          const response = await axios.get(`/buchautor/${id}`);
          this.buchAutor = response.data;
        } catch (error) {
          console.error('Fehler beim Abrufen der Buch-Autor-Verknüpfung:', error);
        }
      },
      // Formular absenden (entweder POST oder PUT)
      async submitForm() {
        if (this.isEdit) {
          await this.updateBuchAutor();  // PUT-Anfrage für die Bearbeitung der Buch-Autor-Verknüpfung
        } else {
          await this.createBuchAutor();  // POST-Anfrage für das Erstellen einer neuen Buch-Autor-Verknüpfung
        }
      },
      // POST-Anfrage zum Erstellen einer neuen Buch-Autor-Verknüpfung
      async createBuchAutor() {
        try {
          await axios.post('/buchautor', this.buchAutor);
          this.$router.push('/buchautor');  // Weiterleitung zur Buch-Autor-Verknüpfungsliste
        } catch (error) {
          console.error('Fehler beim Erstellen der Buch-Autor-Verknüpfung:', error);
        }
      },
      // PUT-Anfrage zum Aktualisieren einer bestehenden Buch-Autor-Verknüpfung
      async updateBuchAutor() {
        try {
          await axios.put(`/buchautor/${this.buchAutor.id}`, this.buchAutor);
          this.$router.push('/buchautor');  // Weiterleitung zur Buch-Autor-Verknüpfungsliste
        } catch (error) {
          console.error('Fehler beim Aktualisieren der Buch-Autor-Verknüpfung:', error);
        }
      }
    }
  };
  </script>
  