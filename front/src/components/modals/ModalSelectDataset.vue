<template>
  <v-dialog v-model="show" max-width="1000px" @click:outside="closeModal()">
    <v-card>
      <template>
        <v-card-title>
          <span class="text-h5">Выбрать датасет</span>
        </v-card-title>
        <v-card-text><data-set-collection/></v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeModal()"> Ок </v-btn>
        </v-card-actions>
      </template>
    </v-card>
  </v-dialog>
</template>
<script>
import DataSetCollection from '../DataSetCollection.vue';
export default {
  components: { DataSetCollection },
  data() {
    return {};
  },
  computed: {
    show() {
      return this.$route.name == "SelectDataset";
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