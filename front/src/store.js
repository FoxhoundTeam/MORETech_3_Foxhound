import Vuex from 'vuex'
import http from './http'
import Axios from 'axios'
import Vue from 'vue'
import { createComponentOperation, COMPONENTS, createComponentTable } from './Graph'


Vue.use(Vuex)


const store = new Vuex.Store({
    state: {
        user: null,
        isAuthenticated: false,
        operations: [],
        tableComponents: {},
        projectName: "Default",
        datasetitems: [],
        schemaResponse: {},
    },
    getters: {
        selectedTables(state) {
            return state.datasetitems.filter(v => v.selected == true);
        }
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuthenticated(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setOperations(state, operations) {
            for (const operation of operations) {
                state.operations.push(
                    {
                        ...operation,
                        component: createComponentOperation(COMPONENTS[operation.type], operation.name, operation.inputs, operation.outputs, operation.many),
                    }
                )
            }
        },
        addTableComponent(state, table) {
            state.tableComponents[table.name] = createComponentTable(table.name, table.fields);
        },
        addSelectedTable(state, table) {
            if (state.datasetitems.filter(v => v.selected == true).findIndex(v => v.name == table.name) != -1) {
                return
            }
            table.selected = true;
            Vue.set(state.datasetitems, state.datasetitems.findIndex(v => v.name == table.name), table)
            // state.selectedTables.push(table);
        },
        removeSelectedTable(state, name) {
            let ind = state.datasetitems.findIndex(v => v.name == name);
            let table = state.datasetitems[ind];
            table.selected = false;
            Vue.set(state.datasetitems, ind, table)
            // Vue.delete(state.selectedTables, state.selectedTables.findIndex(v => v.name == name));
        },
        setProjectName(state, name) {
            state.projectName = name;
        },
        setDatasetItems(state, items) {
            state.datasetitems = items;
        },
        setSchemaResponse(state, schema){
            state.schemaResponse = schema;
        }
    },
    actions: {
        async setOperations(context) {
            let response = (await http.getList('Operation', {}, true)).data.operations;
            context.commit('setOperations', response);
        },
        async setDataSets(context) {
            let response = (await http.getList('DataTable', {}, true)).data.data_table;
            context.commit('setDatasetItems', response);
        },
        async addItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let response = (await http.createItem(data.url, item_data, true)).data;
            let items = context.state[data.items_name]
            items.push(response);
            context.commit(mutation, items);
        },
        async updateItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let dataID = data.dataID;
            let response = (await http.updateItem(data.url, dataID, item_data, true)).data;
            let items = context.state[data.items_name]
            let index = items.findIndex(v => v.id == dataID);
            if (index != -1) {
                Vue.set(items, index, response);
            }
            context.commit(mutation, items);
        },
        async login(context, creds) {
            var username = creds.username;
            var password = creds.password;
            var reg_exp_mail = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/
            var login_info = {
                email: username,
                password: password
            }
            if (username.match(reg_exp_mail) != null) {
                login_info = {
                    email: username,
                    password: password
                }
            } else {
                login_info = {
                    username: username,
                    password: password
                }
            }
            var status = false;
            try {
                await (Axios.post("/rest_api/auth/login/", login_info));
                status = true;
            } catch (error) {
                var data = error.response.data;
                if (data.non_field_errors) {
                    Vue.showErrorModal(data.non_field_errors);
                } else {
                    var result = '';
                    for (var k in data) {
                        result += `${k}: ${data[k]}\n`
                    }
                    Vue.showErrorModal(result);
                }
            }
            await context.dispatch('checkAuth');
            return status;
        },
        async logout(context) {
            await Axios.post("/rest_api/auth/logout/");
            context.commit('setAuthenticated', false);
            context.commit('setUser', {});
        },
        async checkAuth(context) {
            try {
                var result = await Axios.get("/rest_api/auth/user/");
                if (result.status != 200) {
                    context.commit('setUser', {});
                    return
                }
                context.commit('setAuthenticated', true);
                context.commit('setUser', result.data);
            } catch (e) {
                context.commit('setUser', {});
            }
        },
    }
})

export default store;
