<template>
  <div>
    <h1>Verlage Liste</h1>

    <!-- Eingabeformular für einen neuen Verlag -->
    <div class="form-group">
      <input v-model="newVerlagName" class="input-field" placeholder="Verlagsname eingeben" />
      <button class="action-button" @click="addVerlag">Verlag hinzufügen</button>
    </div>

    <!-- Fehlermeldung anzeigen -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Liste der Verlage -->
    <div class="verlag-list">
      <div v-for="verlag in verlage" :key="verlag.id" class="verlag-item">
        <div class="verlag-info">
          <div class="verlag-details">
            <strong>{{ verlag.name }}</strong>
            <small class="verlag-id">ID: {{ verlag.id }}</small>
          </div>
          <div class="verlag-buttons">
            <button class="edit-button" @click="editVerlag(verlag)">Bearbeiten</button>
            <button class="delete-button" @click="deleteVerlag(verlag.id)">Löschen</button>
          </div>
        </div>

        <!-- Bearbeitungsformular -->
        <div v-if="editingVerlag && editingVerlag.id === verlag.id" class="edit-form">
          <h2>Verlag bearbeiten</h2>
          <input v-model="editingVerlag.name" class="input-field" placeholder="Verlagsname" />
          <button class="action-button" @click="updateVerlag">Verlag aktualisieren</button>
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
      verlage: [],
      newVerlagName: "",
      errorMessage: "",
      editingVerlag: null,
    };
  },
  mounted() {
    this.fetchVerlage();
  },
  methods: {
    async fetchVerlage() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/verlage");
        this.verlage = response.data;
      } catch (error) {
        console.error("Fehler beim Abrufen der Verlage:", error);
      }
    },
    async addVerlag() {
      if (!this.newVerlagName) {
        alert("Bitte Verlagsname eingeben!");
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/verlag", {
          name: this.newVerlagName,
        });

        this.verlage.push(response.data);
        this.newVerlagName = "";
        this.errorMessage = "";
      } catch (error) {
        console.error("Fehlerdetails:", error);
        this.errorMessage = "Fehler beim Hinzufügen des Verlags.";
      }
    },
    async deleteVerlag(id) {
      try {
        await axios.delete(`http://127.0.0.1:5000/verlag/${id}`);
        this.verlage = this.verlage.filter(verlag => verlag.id !== id);
      } catch (error) {
        console.error("Fehler beim Löschen des Verlags:", error);
        this.errorMessage = "Fehler beim Löschen des Verlags.";
      }
    },
    editVerlag(verlag) {
      this.editingVerlag = { ...verlag };
    },
    async updateVerlag() {
      if (!this.editingVerlag.name) {
        alert("Bitte Verlagsname eingeben!");
        return;
      }

      try {
        const response = await axios.put(`http://127.0.0.1:5000/verlag/${this.editingVerlag.id}`, {
          name: this.editingVerlag.name,
        });

        const index = this.verlage.findIndex(verlag => verlag.id === this.editingVerlag.id);
        this.verlage[index] = response.data;
        this.editingVerlag = null;
        this.errorMessage = "";
      } catch (error) {
        console.error("Fehler beim Aktualisieren des Verlags:", error);
        this.errorMessage = "Fehler beim Aktualisieren des Verlags.";
      }
    },
    cancelEdit() {
      this.editingVerlag = null;
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

.verlag-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.verlag-item {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.verlag-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.verlag-details {
  display: flex;
  flex-direction: column;
}

.verlag-id {
  font-size: 12px;
  color: #666;
}

.verlag-buttons {
  display: flex;
  gap: 8px;
}
</style>
