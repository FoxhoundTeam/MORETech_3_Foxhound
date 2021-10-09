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
  beforeMount() {
    ErrorModal.ErrorEvent.$on("show", (params) => {
      this.modalContent = params.data;
      this.showErrorModal = true;
    });
    this.$store.commit("setOperations", [
      {
        name: "Left join",
        icon: "join_left",
        type: 'join',
        inputs: [
          {
            key: "left",
            name: "Left",
            socket: "joinNumber",
          },
          {
            key: "right",
            name: "Right",
            socket: "joinNumber",
          },
        ],
        outputs: [],
      },
      {
        name: "SUM",
        icon: "SUM",
        type: 'operation',
        inputs: [
          {
            key: "innumber",
            name: "Column (number)",
            socket: "number",
          },
        ],
        outputs: [
          {
            key: "outnumber",
            name: "Output number",
            socket: "number",
          },
        ],
      },
      {
        name: "SUM VEC",
        icon: "SUM VEC",
        type: 'operation',
        many: true,
        inputs: [
          {
            key: "innumber",
            name: "Column1 (number)",
            socket: "number",
          },
          {
            key: "innumber2",
            name: "Column2 (number)",
            socket: "number",
          },
        ],
        outputs: [
          {
            key: "outnumber",
            name: "Output column",
            socket: "number",
          },
        ],
      },
      {
        name: "AVG",
        icon: "AVG",
        type: 'operation',
        inputs: [
          {
            key: "innumber",
            name: "Column (number)",
            socket: "number",
          },
        ],
        outputs: [
          {
            key: "outnumber",
            name: "Output number",
            socket: "number",
          },
        ],
      },
      {
        name: "MUL VEC",
        icon: "MUL VEC",
        type: 'operation',
        many: true,
        inputs: [
          {
            key: "innumber",
            name: "Column1 (number)",
            socket: "number",
          },
          {
            key: "innumber2",
            name: "Column2 (number)",
            socket: "number",
          },
        ],
        outputs: [
          {
            key: "outnumber",
            name: "Output column",
            socket: "number",
          },
        ],
      },
      {
        name: "NumFilter",
        icon: "filter_alt",
        type: 'filter',
        inputs: [
          {
            key: "incolumn",
            name: "Column",
            socket: "number",
          },
        ],
        outputs: [],
      },
      {
        name: "StrFilter",
        icon: "filter_alt",
        type: 'filter',
        inputs: [
          {
            key: "incolumn",
            name: "Column",
            socket: "string",
          },
        ],
        outputs: [],
      },
      {
        name: "OutputToCSV",
        icon: "CSV",
        type: 'output',
        inputs: [
          {
            key: "incolumn",
            name: "Column",
            socket: "any",
          },
        ],
        outputs: [],
      },
    ]);
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
