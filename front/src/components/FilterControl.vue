<template>
  <v-text-field filled v-model="value" />
</template>

<script>
export default {
  props: ["emitter", "ikey", "getData", "putData"],
  data() {
    return {
      value: "",
    };
  },
  watch: {
    value() {
      if (this.ikey) this.putData(this.ikey, this.value);
    },
  },
  mounted() {
    this.value = this.getData(this.ikey);
  },
};
</script>

<style>
</style>