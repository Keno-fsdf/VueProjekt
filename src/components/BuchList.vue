<template>
  <div>
    <h1>Bücher Liste</h1>

    <!-- Eingabeformular für ein neues Buch -->
    <div class="form-group">
      <input v-model="newBuchTitel" class="input-field" placeholder="Buchtitel eingeben" />
      <input v-model="newVerlagId" class="input-field" type="number" placeholder="Verlag-ID eingeben" />
      <button class="action-button" @click="addBuch">Buch hinzufügen</button>
    </div>

    <!-- Fehlermeldung anzeigen -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Liste der Bücher -->
    <div class="buch-list">
      <div v-for="buch in buecher" :key="buch.id" class="buch-item">
        <div class="buch-info">
          <div class="buch-titel-verlag">
            <strong>{{ buch.titel }}</strong>
            <small class="verlag-id">Verlag-ID: {{ buch.verlag_id }}</small>
          </div>
          <div class="buch-buttons">
            <button class="edit-button" @click="editBuch(buch)">Bearbeiten</button>
            <button class="delete-button" @click="deleteBuch(buch.id)">Löschen</button>
          </div>
        </div>

        <!-- Bearbeitungsformular -->
        <div v-if="editingBuch && editingBuch.id === buch.id" class="edit-form">
          <h2>Buch bearbeiten</h2>
          <input v-model="editingBuch.titel" class="input-field" placeholder="Buchtitel" />
          <input v-model="editingBuch.verlag_id" class="input-field" type="number" placeholder="Verlag-ID" />
          <button class="action-button" @click="updateBuch">Buch aktualisieren</button>
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
      buecher: [],
      newBuchTitel: "",
      newVerlagId: null,
      errorMessage: "",
      editingBuch: null,
    };
  },
  mounted() {
    this.fetchBuecher();
  },
  methods: {
    async fetchBuecher() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/buecher");
        this.buecher = response.data;
      } catch (error) {
        console.error("Fehler beim Abrufen der Bücher:", error);
      }
    },
    async addBuch() {
      if (!this.newBuchTitel || !this.newVerlagId) {
        alert("Bitte Titel und Verlag-ID eingeben!");
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/buch", {
          titel: this.newBuchTitel,
          verlag_id: this.newVerlagId,
        });

        this.buecher.push(response.data);
        this.newBuchTitel = "";
        this.newVerlagId = null;
        this.errorMessage = "";
      } catch (error) {
        console.error("Fehlerdetails:", error);
        this.errorMessage = "Es gab ein Problem beim Hinzufügen des Buches. Möglicherweise liegt es an einer ungültigen Verlag-ID. Bitte überprüfen Sie die ID und versuchen Sie es erneut.";
      }
    },
    async deleteBuch(id) {
      try {
        await axios.delete(`http://127.0.0.1:5000/buch/${id}`);
        this.buecher = this.buecher.filter(buch => buch.id !== id);
      } catch (error) {
        console.error("Fehler beim Löschen des Buches:", error);
        this.errorMessage = "Fehler beim Löschen des Buches.";
      }
    },
    editBuch(buch) {
      this.editingBuch = { ...buch };
    },
    async updateBuch() {
      if (!this.editingBuch.titel || !this.editingBuch.verlag_id) {
        alert("Bitte Titel und Verlag-ID eingeben!");
        return;
      }

      try {
        const response = await axios.put(`http://127.0.0.1:5000/buch/${this.editingBuch.id}`, {
          titel: this.editingBuch.titel,
          verlag_id: this.editingBuch.verlag_id,
        });

        const index = this.buecher.findIndex(buch => buch.id === this.editingBuch.id);
        this.buecher[index] = response.data;
        this.editingBuch = null;
        this.errorMessage = "";
      } catch (error) {
        console.error("Fehler beim Aktualisieren des Buches:", error);
        this.errorMessage = "Fehler beim Aktualisieren des Buches.";
      }
    },
    cancelEdit() {
      this.editingBuch = null;
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



.edit-button {
  background-color: #FF9800; /* Orange */
}

.edit-button:hover {
  background-color: #FB8C00; /* Dunkleres Orange */
}



/* Spezifischer Button-Stil für "Löschen" */
.delete-button {
  background-color: #f44336; /* Rot */
}

.delete-button:hover {
  background-color: #e53935; /* Dunkleres Rot */
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

.buch-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.buch-item {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.buch-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.buch-titel-verlag {
  display: flex;
  flex-direction: column;
}

.verlag-id {
  font-size: 12px;
  color: #666;
}

.buch-buttons {
  display: flex;
  gap: 8px;
}
</style>
