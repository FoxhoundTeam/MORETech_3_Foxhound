<template>
  <div id="app">
    <v-app style="min-height: 100vh">
      <nav-bar />
      <v-main class="m-2">
        <router-view></router-view>
      </v-main>
      <v-dialog v-model="showErrorModal" max-width="300">
        <v-card>
          <v-card-title class="text-h5"> Ошибка </v-card-title>

          <v-card-text>
            {{ modalContent }}
          </v-card-text>

          <v-card-actions>
            <v-btn color="green darken-1" text @click="showErrorModal = false">
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import ErrorModal from "./plugins/ErrorModal";

export default {
  components: { NavBar },
  name: "app",
  data() {
    return {
      showErrorModal: false,
      modalContent: null,
    };
  },
  async beforeMount() {
    ErrorModal.ErrorEvent.$on("show", (params) => {
      this.modalContent = params.data;
      this.showErrorModal = true;
    });
    await this.$store.dispatch("setOperations");
    await this.$store.dispatch("setDataSets");
  },
};
</script>
<style>
#app {
}
a {
  text-decoration: none !important;
}
</style>
