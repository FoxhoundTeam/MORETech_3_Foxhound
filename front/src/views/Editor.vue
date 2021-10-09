<template>
  <div>
    <graph />
    <router-view />
  </div>
</template>

<script>
import Graph from "../components/Graph.vue";
export default {
  components: { Graph },
};
</script>

<style>
</style>