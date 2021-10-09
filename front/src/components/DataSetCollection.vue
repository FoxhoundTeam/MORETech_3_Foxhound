<template>
  <div>
    <v-card class="mx-auto">
      <v-toolbar elevation="0">
        <v-text-field
          hide-details
          prepend-icon="mdi-magnify"
          placeholder="Поиск по названию и тегу"
          single-line
          v-model="searchline"
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-switch
          label="Только бесплатные"
          inset
          v-model="searchfreeonly"
        ></v-switch>
      </v-toolbar>
      <v-divider></v-divider>
      <template v-for="(item, index) in filtereditems">
        <v-list-item
          two-line
          :key="item.name"
        >
          <v-list-item-action>
            <v-checkbox
              v-model="item.selected"
              color="primary"
            ></v-checkbox>
          </v-list-item-action>
          <v-list-item-icon class="mr-5">
            <v-badge
              :value="!item.price"
              bottom
              avatar
              bordered
              overlap
              color="green"
            >
              <template v-slot:badge>
                <v-icon color="white" small> mdi-currency-usd-off </v-icon>
              </template>
              <v-avatar max-height="100" max-width="100">
                <!-- <v-img :src="item.icon"></v-img> -->
                <v-icon>storage</v-icon>
              </v-avatar>
            </v-badge>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title
              class="text-lg-h6"
              v-text="item.name"
            ></v-list-item-title>
            <v-list-item-subtitle
              v-text="item.description"
            ></v-list-item-subtitle>
            <v-row>
              <template v-for="tagname in item.tags">
                <v-chip :key="tagname" small class="ma-4" label>{{
                  tagname
                }}</v-chip>
              </template>
            </v-row>
            <v-item>Цена: {{ item.price == 0 ? 'Бесплатно' : `${item.price} руб.`}}</v-item>
          </v-list-item-content>
        </v-list-item>
        <v-divider
          v-if="index + 1 < datasetitems.length"
          :key="index"
        ></v-divider>
      </template>
    </v-card>
    <v-btn block class="mt-2" color="primary" v-if='$store.getters.selectedTables.length && $route.name != "SelectDataset"' @click="$router.push({name: 'Editor'})">Перейти в редактор</v-btn>
    <v-pagination v-model="page" :length="Math.ceil(datasetitems.length / 10)">
    </v-pagination>
  </div>
</template>

<script>
export default {
  data: () => ({
    searchline: "",
    searchfreeonly: false,
    page: 1,
  }),
  computed: {
      selectedItems: {
        get(){
            return []
        },
        set(value) {
            console.log(value);
        }
      },
    pagecount() {
      return Math.ceil(this.datasetitems.length / 10);
    },
    datasetitems() {
      return this.$store.state.datasetitems;
    },
    filtereditems() {
      return this.datasetitems.filter((item) => {
        return (
          (item.name.toLowerCase().match(this.searchline.toLowerCase()) ||
            //item.tags.includes(this.searchline.toLowerCase())
            item.tags.filter((tag_item) => {
              return tag_item.match(this.searchline.toLowerCase());
            }).length > 0) &&
          //item.tags.includes(this.searchline.toLowerCase() )
          (item.price == 0 || (this.searchfreeonly ? item.price == 0 : true))
        );
      });
    },
  },
};
</script>

<style>
</style>