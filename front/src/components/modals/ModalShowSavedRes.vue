<template>
  <v-dialog v-model="show" max-width="1000px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">Данные успешно обработаны</span>
        </v-card-title>
        <v-card-text><vue-json-pretty :path="'res'" :data="$store.state.schemaResponse"> </vue-json-pretty></v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeModal()"> Ок </v-btn>
        </v-card-actions>
      </template>
    </v-card>
  </v-dialog>
</template>
<script>
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";
export default {
  components: {
    VueJsonPretty,
  },
  data() {
    return {};
  },
  computed: {
    show() {
      return this.$route.name == "ShowResult";
    },
  },
  methods: {
    closeModal() {
      var q = { ...this.$route.query };
      this.$router.replace({
        name: "Editor",
        query: q,
      });
    },
    addItem() {},
    deleteItem() {},
  },
};
</script>
<style>
</style>