import Rete from "rete";
import AddRemoveFieldControl from './components/AddRemoveFieldControl.vue'
import FilterControl from './components/FilterControl.vue'

var numberSocket = new Rete.Socket('Number')
var stringSocket = new Rete.Socket('String')
var booleanSocket = new Rete.Socket('Boolean')
var dateSocket = new Rete.Socket('Date')
var datetimeSocket = new Rete.Socket('DateTime')
var joinNumberSocket = new Rete.Socket('JOINNumber')
var anySocket = new Rete.Socket('Any')
numberSocket.combineWith(joinNumberSocket)
stringSocket.combineWith(joinNumberSocket)
numberSocket.combineWith(anySocket)
stringSocket.combineWith(anySocket)
booleanSocket.combineWith(anySocket)
dateSocket.combineWith(anySocket)
datetimeSocket.combineWith(anySocket)

const SOCKETS = {
    number: numberSocket,
    string: stringSocket,
    bool: booleanSocket,
    date: dateSocket,
    datetime: datetimeSocket,
    any: anySocket,
    joinNumber: joinNumberSocket,
}

class TableComponent extends Rete.Component {
    constructor(name, fields) {
        super(name);
        this.fields = fields;
    }

    builder(node) {
        for (const field of this.fields) {
            node.addOutput(new Rete.Output(field.key, field.name, SOCKETS[field.socket]));
            node.data[field.key] = {
                nodeName: this.name,
                field: field,
                fields: this.fields,
            }
        }
        node.data.nodeName = this.name;
        return node
    }
    worker(node, inputs, outputs) {
        for (const key in node.data) {
            outputs[key] = node.data[key]
        }
        return node, inputs, outputs
    }
}


class RemoveAddFieldControl extends Rete.Control {
    constructor(key, add, remove) {
        super(key);
        this.render = 'vue';
        this.component = AddRemoveFieldControl;
        this.props = { add: add, remove: remove }
    }
}

class FilterFuncControl extends Rete.Control {
    constructor(emitter, key) {
        super(key);
        this.render = 'vue';
        this.component = FilterControl;
        this.props = { emitter, ikey: key };
    }
}

class OperationComponent extends Rete.Component {
    constructor(name, inputs, outputs, many = false) {
        super(name);
        this.inputs = inputs;
        this.outputs = outputs;
        this.many = many;
        this.minInputs = this.inputs.length;
        this.countOfInputs = this.minInputs;
    }

    builder(node) {
        for (const output of this.outputs) {
            node.addOutput(new Rete.Output(output.key, output.name, SOCKETS[output.socket]));
            node.data[output.key] = {
                field: output,
                fields: this.outputs,
                nodeName: this.name
            }
        }
        for (const input of this.inputs) {
            node.addInput(new Rete.Input(input.key, input.name, SOCKETS[input.socket]));
        }
        if (this.many) {
            let inputSample = this.inputs[0];
            let t = this;
            node.addControl(new RemoveAddFieldControl(this.name,
                () => {
                    t.countOfInputs += 1;
                    node.addInput(new Rete.Input(inputSample.key + t.countOfInputs, inputSample.name, SOCKETS[inputSample.socket]));
                    node.update()
                },
                () => {
                    if (t.countOfInputs - 1 < t.minInputs)
                        return
                    t.countOfInputs -= 1;
                    let input = [...node.inputs][node.inputs.size - 1][1]
                    input.connections.map(
                        c => {
                            c.remove();
                            t.editor.removeConnection(c);
                        }
                    );
                    node.removeInput(input)
                    node.update()
                }
            )
            )
        }
        return node
    }
    worker(node, inputs, outputs) {
        for (const key in node.data) {
            outputs[key] = node.data[key]
        }
        return node, inputs, outputs
    }
}

class OutputComponent extends OperationComponent {
    constructor(name, fields) {
        super(name, fields, [], true);
    }
}

class JOINComponent extends OperationComponent {
    worker(node, inputs, outputs) {
        let index = this.editor.nodes.findIndex(v => v.id == node.id)
        node = this.editor.nodes[index]
        let inputsVal = Object.values(inputs);
        let _this = this;
        let newLeft = inputsVal[0].length != 0 ? inputsVal[0][0].nodeName : null
        let newRight = inputsVal[1].length != 0 ? inputsVal[1][0].nodeName : null
        let prevLeft = node.data.prevLeft
        let prevRight = node.data.prevRight
        node.data.prevLeft = inputsVal[0].length != 0 ? inputsVal[0][0].nodeName : null
        node.data.prevRight = inputsVal[1].length != 0 ? inputsVal[1][0].nodeName : null
        let needChange = newLeft != prevLeft || newRight != prevRight;
        if (needChange) {
            for (let output of node.outputs) {
                output[1].connections.map(
                    c => {
                        c.remove();
                        _this.editor.removeConnection(c);
                    }
                );
                node.removeOutput(output[1]);
            }
            if (inputsVal[0].length == 1 && inputsVal[1].length == 1) {
                let fields = [];
                for (const input of Object.values(inputs)){
                    let tmpFields = [...input[0].fields];
                    for (let field of tmpFields) {
                        field.key = field.key + input[0].nodeName
                    }
                    fields = fields.concat(...tmpFields);
                }
                for (const input of Object.values(inputs)) {
                    let data = input[0]
                    for (const field of Object.values(data.fields)) {
                        node.addOutput(new Rete.Output(field.key + data.nodeName, field.name, SOCKETS[field.socket]));
                        node.data[field.key + data.nodeName] = {
                            nodeName: this.name,
                            field: field,
                            fields: fields,
                        }
                    }
                }
            }
        }
        this.editor.nodes[index] = node;
        node.update();
        for (const key in node.data) {
            outputs[key] = node.data[key]
        }
        return node, inputs, outputs
    }
}

class FilterComponent extends OperationComponent {
    builder(node) {
        super.builder(node)
        node.addControl(new FilterFuncControl(this.editor, 'filter'))
    }
    worker(node, inputs, outputs) {
        let index = this.editor.nodes.findIndex(v => v.id == node.id)
        let _this = this;
        node = this.editor.nodes[index]
        let inputsVal = Object.values(inputs);
        let newCon = inputsVal[0].length != 0 ? inputsVal[0][0].nodeName : null
        let prevCon = node.data.prevCon
        node.data.prevCon = inputsVal[0].length != 0 ? inputsVal[0][0].nodeName : null
        if (newCon != prevCon) {
            for (let output of node.outputs) {
                output[1].connections.map(
                    c => {
                        c.remove();
                        _this.editor.removeConnection(c);
                    }
                );
                node.removeOutput(output[1]);
            }
            if (inputsVal[0].length == 1) {
                let data = inputsVal[0][0]
                for (const field of Object.values(data.fields)) {
                    node.addOutput(new Rete.Output(field.key + data.nodeName, field.name, SOCKETS[field.socket]));
                    node.data[field.key + data.nodeName] = {
                        nodeName: this.name,
                        field: field,
                        fields: Object.values(data.fields),
                    }
                }
            }
        }
        this.editor.nodes[index] = node;
        node.update();
        for (const key in node.data) {
            outputs[key] = node.data[key]
        }
        return node, inputs, outputs
    }
}


export const COMPONENTS = {
    join: JOINComponent,
    operation: OperationComponent,
    filter: FilterComponent,
    output: OutputComponent,
}

export function createComponentTable(name, fields) {
    return new TableComponent(name, fields)
}

export function createComponentOperation(componentClass, name, inputs, outputs, many) {
    return new componentClass(name, inputs, outputs, many)
}
