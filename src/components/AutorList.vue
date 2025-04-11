<template>
  <div>
    <h1>Autoren Liste</h1>

    <!-- Eingabeformular für einen neuen Autor -->
    <div class="form-group">
      <input v-model="newAutorName" class="input-field" placeholder="Autorenname eingeben" />
      <button class="action-button" @click="addAutor">Autor hinzufügen</button>
    </div>

    <!-- Fehlermeldung anzeigen -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Liste der Autoren -->
    <div class="autor-list">
      <div v-for="autor in autoren" :key="autor.id" class="autor-item">
        <div class="autor-info">
          <div class="autor-details">
            <strong>{{ autor.name }}</strong>
            <small class="autor-id">ID: {{ autor.id }}</small>
          </div>
          <div class="autor-buttons">
            <button class="edit-button" @click="editAutor(autor)">Bearbeiten</button>
            <button class="delete-button" @click="deleteAutor(autor.id)">Löschen</button>
          </div>
        </div>

        <!-- Bearbeitungsformular -->
        <div v-if="editingAutor && editingAutor.id === autor.id" class="edit-form">
          <h2>Autor bearbeiten</h2>
          <input v-model="editingAutor.name" class="input-field" placeholder="Autorenname" />
          <button class="action-button" @click="updateAutor">Autor aktualisieren</button>
          <button class="action-button" @click="cancelEdit">Abbrechen</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      autoren: [],
      newAutorName: "",
      errorMessage: "",
      editingAutor: null,
    };
  },
  mounted() {
    this.fetchAutoren();
  },
  methods: {
    async fetchAutoren() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/autoren");
        this.autoren = response.data;
      } catch (error) {
        console.error("Fehler beim Abrufen der Autoren:", error);
      }
    },
    async addAutor() {
      if (!this.newAutorName) {
        alert("Bitte Autorenname eingeben!");
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/autor", {
          name: this.newAutorName,
        });

        this.autoren.push(response.data);
        this.newAutorName = "";
        this.errorMessage = "";
      } catch (error) {
        console.error("Fehlerdetails:", error);
        this.errorMessage = "Fehler beim Hinzufügen des Autors.";
      }
    },
    async deleteAutor(id) {
      try {
        await axios.delete(`http://127.0.0.1:5000/autor/${id}`);
        this.autoren = this.autoren.filter(autor => autor.id !== id);
      } catch (error) {
        console.error("Fehler beim Löschen des Autors:", error);
        this.errorMessage = "Fehler beim Löschen des Autors.";
      }
    },
    editAutor(autor) {
      this.editingAutor = { ...autor };
    },
    async updateAutor() {
      if (!this.editingAutor.name) {
        alert("Bitte Autorenname eingeben!");
        return;
      }

      try {
        const response = await axios.put(`http://127.0.0.1:5000/autor/${this.editingAutor.id}`, {
          name: this.editingAutor.name,
        });

        const index = this.autoren.findIndex(autor => autor.id === this.editingAutor.id);
        this.autoren[index] = response.data;
        this.editingAutor = null;
        this.errorMessage = "";
      } catch (error) {
        console.error("Fehler beim Aktualisieren des Autors:", error);
        this.errorMessage = "Fehler beim Aktualisieren des Autors.";
      }
    },
    cancelEdit() {
      this.editingAutor = null;
    }
  }
};
</script>

<style scoped>
input {
  margin: 8px 0;
  padding: 10px;
  width: 100%;
  max-width: 300px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

button {
  padding: 8px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

button:hover {
  background-color: #45a049;
}

/* Bearbeiten-Button */
.edit-button {
  background-color: #FF9800;
}

.edit-button:hover {
  background-color: #FB8C00;
}

/* Löschen-Button */
.delete-button {
  background-color: #f44336;
}

.delete-button:hover {
  background-color: #e53935;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.autor-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.autor-item {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.autor-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.autor-details {
  display: flex;
  flex-direction: column;
}

.autor-id {
  font-size: 12px;
  color: #666;
}

.autor-buttons {
  display: flex;
  gap: 8px;
}
</style>
