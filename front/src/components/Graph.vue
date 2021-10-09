<template>
  <div class="w-100">
    <v-toolbar>
      <v-toolbar-title class="mr-5"
        ><v-text-field class="mt-5" dense v-model="name"></v-text-field
      ></v-toolbar-title>
      <v-divider class="mx-5" vertical></v-divider>
      <v-btn icon @click="$router.push({ name: 'SelectDataset' })">
        <v-icon>add</v-icon>
      </v-btn>
      <v-btn icon @click="removeNode">
        <v-icon>delete</v-icon>
      </v-btn>
      <v-divider class="mx-5" vertical></v-divider>
      <v-btn
        icon
        @click="addNode(operation.component)"
        v-for="operation in $store.state.operations.filter(
          (v) => v.type === 'join'
        )"
        :key="operation.name"
      >
        <v-icon>{{ operation.icon }}</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>join_right</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>join_full</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>join_inner </v-icon>
      </v-btn>
      <v-divider class="mx-5" vertical></v-divider>
      <v-btn
        elevation="0"
        rounded
        @click="addNode(operation.component)"
        v-for="operation in $store.state.operations
          .filter((v) => v.type === 'operation')
          .splice(0, 3)"
        :key="operation.name"
      >
        {{ operation.icon }}
      </v-btn>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            @click="addNode(operation.component)"
            v-for="operation in $store.state.operations
              .filter((v) => v.type === 'operation')
              .splice(3)"
            :key="operation.name"
          >
            <v-list-item-title>{{ operation.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-divider class="mx-5" vertical></v-divider>
      <v-btn icon>
        <v-icon>functions</v-icon>
      </v-btn>
      <v-divider class="mx-5" vertical></v-divider>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>filter_alt</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            @click="addNode(operation.component)"
            v-for="operation in $store.state.operations.filter(
              (v) => v.type === 'filter'
            )"
            :key="operation.name"
          >
            <v-list-item-title>{{ operation.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-divider class="mx-5" vertical></v-divider>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>file_download</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            @click="addNode(operation.component)"
            v-for="operation in $store.state.operations.filter(
              (v) => v.type === 'output'
            )"
            :key="operation.name"
          >
            <v-list-item-title>{{ operation.icon }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-divider class="mx-5" vertical></v-divider>
      <v-btn plain>Сохранить</v-btn>
    </v-toolbar>
    <div ref="rete" style="height: 79vh"></div>
  </div>
</template>

<script>
import Rete from "rete";
import ConnectionPlugin from "rete-connection-plugin";
import VueRenderPlugin from "rete-vue-render-plugin";
import AreaPlugin from "rete-area-plugin";

export default {
  data() {
    return {
      editor: null,
      engine: null,
      drawedTables: [],
    };
  },
  computed: {
    name: {
      get() {
        return this.$store.state.projectName;
      },
      set(value) {
        this.$store.commit("setProjectName", value);
      },
    },
    selectedTables() {
      return this.$store.getters.selectedTables;
    },
  },
  watch: {
    async selectedTables() {
      await this.drawTables();
    },
  },
  async mounted() {
    var container = this.$refs["rete"];
    this.editor = new Rete.NodeEditor(this.name + "@0.1.0", container);
    this.editor.use(ConnectionPlugin);
    this.editor.use(VueRenderPlugin);
    this.editor.use(AreaPlugin);
    this.engine = new Rete.Engine(this.name + "@0.1.0");
    var t = this;
    this.$store.state.operations.map((c) => {
      t.editor.register(c.component);
      t.engine.register(c.component);
    });
    await this.drawTables();
    this.editor.on(
      "process nodecreated noderemoved connectioncreated connectionremoved",
      async () => {
        await t.engine.abort();
        await t.engine.process(t.editor.toJSON());
      }
    );
  },
  methods: {
    async addNode(component) {
      var node = await component.createNode();
      node.position = [210, 100];
      await this.editor.addNode(node);
    },
    removeNode() {
      for (const selected of this.editor.selected.list) {
        if (
          this.selectedTables.findIndex((v) => v.name == selected.name) != -1
        ) {
          this.$store.commit("removeSelectedTable", selected.name);
          this.$delete(
            this.drawedTables,
            this.drawedTables.findIndex((v) => v.name == selected.name)
          );
        }
        this.editor.removeNode(selected);
      }
    },
    async drawTables() {
      for (let table of this.drawedTables) {
        if (this.selectedTables.findIndex((v) => v.name == table.name) == -1) {
          this.editor.removeNode(table.node);
          this.$delete(
            this.drawedTables,
            this.drawedTables.findIndex((v) => v.name == table.name)
          );
        }
      }
      let index = this.drawedTables.length;
      for (let table of this.selectedTables) {
        if (this.drawedTables.findIndex((v) => v.name == table.name) != -1) continue;
        await this.addTable(table, index);
        index += 1;
      }
    },
    async addTable(table, index) {
      if (this.drawedTables.findIndex((v) => v.name == table.name) != -1)
        return;
      if (!this.$store.state.tableComponents[table.name])
        this.$store.commit("addTableComponent", table);
      var tableComponent = this.$store.state.tableComponents[table.name];
      try {
        this.editor.register(tableComponent);
        this.engine.register(tableComponent);
      } catch {
        console.log("already registered");
      }
      let node = await tableComponent.createNode();
      node.position = [10, 100 * index];
      this.$store.commit("addSelectedTable", table);
      await this.editor.addNode(node);
      this.drawedTables.push({name: table.name, node: node});
    },
  },
};
</script>

<style>
html,
body {
  height: 100%;
  width: 100%;
}
.node {
  background: rgb(255, 255, 255) !important;
  border: 2px solid #000000 !important;
  border-radius: 10px;
  cursor: pointer;
  min-width: 180px;
  height: auto;
  padding-bottom: 6px;
  box-sizing: content-box;
  position: relative;
  user-select: none;
}
.node.selected {
  background: #e2e2e2 !important;
  border-color: #000000 !important;
}
.node .title {
  color: black !important;
}
.node .output-title {
  color: black !important;
}
.node .input-title {
  color: black !important;
}
</style>