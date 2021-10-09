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
        selectedTables: [
            {
                name: 'Users',
                fields: [
                    {
                        key: 'id',
                        name: 'id (number)',
                        socket: 'number',
                    },
                    {
                        key: 'first_name',
                        name: 'first_name (string)',
                        socket: 'string',
                    },
                    {
                        key: 'age',
                        name: 'age (number)',
                        socket: 'number',
                    },
                    {
                        key: 'gender',
                        name: 'gender (string)',
                        socket: 'string',
                    },
                ]
            },
            {
                name: 'Accounts',
                fields: [
                    {
                        key: 'id',
                        name: 'id (number)',
                        socket: 'number',
                    },
                    {
                        key: 'user_id',
                        name: 'user_id (number)',
                        socket: 'number',
                    },
                    {
                        key: 'balance',
                        name: 'balance (number)',
                        socket: 'number',
                    },
                    {
                        key: 'date_update',
                        name: 'date_update (date)',
                        socket: 'date',
                    },
                ]
            }
        ],
        projectName: "Default",
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
            if (state.selectedTables.findIndex(v => v.name == table.name) != -1) {
                return
            }
            state.selectedTables.push(table);
        },
        removeSelectedTable(state, name) {
            Vue.delete(state.selectedTables, state.selectedTables.findIndex(v => v.name == name));
        },
        setProjectName(state, name){
            state.projectName = name;
        }
    },
    actions: {
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
