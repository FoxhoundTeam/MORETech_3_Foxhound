<template>
  <div>
    <v-btn @click="add" icon>+</v-btn
    ><v-btn @click="remove" icon>-</v-btn>
  </div>
</template>

<script>
export default {
  props: ["add", "remove"],
};
</script>

<style>
</style>