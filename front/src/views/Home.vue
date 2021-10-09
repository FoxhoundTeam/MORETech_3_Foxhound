<template>
  <!-- Тут список датасетов -->
  <div>
    <v-card
      class="mx-auto">
      <v-toolbar
      
      >
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
      <v-item></v-item>
      <template v-for="(item, index) in filtereditems">
        <v-list-item two-line :key="item.title">
              <v-list-item-icon>
                <v-badge
                  :value="item.isfree"
                  bottom
                  avatar
                  bordered
                  overlap
                  color="green"
                >
                  <template v-slot:badge>
                    <v-icon color="white" small>
                      mdi-currency-usd-off
                    </v-icon>
                  </template>
                  <v-avatar max-height="80" max-width="80">
                    <v-img
                      :src="item.icon"
                    ></v-img>
                  </v-avatar>
              </v-badge>           
            </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="text-lg-h6" v-text="item.title"></v-list-item-title>
            <v-list-item-subtitle v-text="item.description"></v-list-item-subtitle>
            <v-row>
            <template v-for="(tagname) in item.tags">
              <v-chip :key="tagname"
                small
                class="ma-4"
                label
              >{{tagname}}</v-chip>
            </template>
            </v-row>
          </v-list-item-content>
        </v-list-item>
        <v-divider
            v-if="index + 1 < datasetitems.length"
            :key="index"
          ></v-divider>
      </template>
      
    </v-card>

    <v-pagination
        v-model="page"
        :length="Math.ceil(datasetitems.length/10)">
    </v-pagination>
  </div>
</template>

<script>
export default {
  data: () => ({
    searchline: '',
    searchfreeonly:false,
    datasetitems: [
      {
        title: 'Датасет 1',
        description: 'Описание датасета 1',
        source: 'vtb',
        icon:'default_dataset_icon.png',
        size:'100000',
        isfree:true,
        tags:['транзакции', '2021', 'втб', 'анонимизированный'],
        loaddate:"2021-04-12"
      },
      {
        title: 'Датасет 2',
        description: 'Описание датасета 2',
        source: 'datahub',
        icon:'default_dataset_icon.png',
        size:'1000',
        isfree:false,
        tags:['кредиты', '2019', 'анонимизированный'],
        loaddate:"2020-11-15"
      }]
      }),
  computed: {
      pagecount () {
          return Math.ceil(this.datasetitems.length / 10)
        },
      
      filtereditems () {
        return this.datasetitems.filter( (item) =>{
          return (
                item.title.toLowerCase().match(this.searchline.toLowerCase())
                ||
                //item.tags.includes(this.searchline.toLowerCase())
                (item.tags.filter( (tag_item) =>{
                  return (tag_item.match(this.searchline.toLowerCase()))
                }).length > 0)
              //item.tags.includes(this.searchline.toLowerCase() )
              )
              &&
              (item.isfree === true || item.isfree === this.searchfreeonly)
          })
        
        }
  }
};
</script>

<style>
</style>