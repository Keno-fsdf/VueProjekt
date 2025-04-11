<template>
    <div>
      <h1>Bibliothek Verwaltung</h1>
      <nav>
        <ul>
          <li><router-link to="/verlage">Verlage</router-link></li>
          <li><router-link to="/autoren">Autoren</router-link></li>
          <li><router-link to="/buecher">Bücher</router-link></li>
          <!-- <li><router-link to="/buchautoren">Buch-Autor-Verknüpfungen</router-link></li> -->
        </ul>
      </nav>
      <router-view></router-view>  <!-- Hier werden die anderen Komponenten angezeigt -->
    </div>
  </template>
  
  <script>
  export default {
    name: 'Home',
  };
  </script>
  
  <style scoped>
  nav ul {
    list-style-type: none;
    padding: 0;
  }
  nav li {
    display: inline;
    margin-right: 10px;
  }
  </style>
  