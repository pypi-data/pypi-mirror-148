import { CustomNodeModel } from "../components/CustomNodeModel";

interface GeneralComponentLibraryProps{
    model : any;
}

export function GeneralComponentLibrary(props: GeneralComponentLibraryProps){
    let node = null;
    const nodeData = props.model;
    const nodeName = nodeData.task;
    // For now, comment this first until we've use for it
    // if (props.type === 'math') {

    //     node = new CustomNodeModel({ name: props.name, color: props.color, extras: { "type": props.type } });

    //     node.addInPortEnhance('▶', 'in-0');
    //     node.addInPortEnhance('A', 'in-1');
    //     node.addInPortEnhance('B', 'in-2');

    //     node.addOutPortEnhance('▶', 'out-0');
    //     node.addOutPortEnhance('value', 'out-1');

    // } else if (props.type === 'convert') {

    //     node = new CustomNodeModel({ name: props.name, color: props.color, extras: { "type": props.type } });

    //     node.addInPortEnhance('▶', 'in-0');
    //     node.addInPortEnhance('model', 'parameter-string-in-1');

    //     node.addOutPortEnhance('▶', 'out-0');
    //     node.addOutPortEnhance('converted', 'out-1');

    // } else 
    if (nodeData.type === 'string') {

        if ((nodeName).startsWith("Literal")) {

            let theResponse = window.prompt('Enter String Value (Without Quotes):');
            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(theResponse, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter String Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (String): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');

        }

    } else if (nodeData.type === 'int') {

        if ((nodeName).startsWith("Literal")) {

            let theResponse = window.prompt('Enter Int Value (Without Quotes):');
            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(theResponse, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter Int Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (Int): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');

        }

    } else if (nodeData.type === 'float') {

        if ((nodeName).startsWith("Literal")) {

            let theResponse = window.prompt('Enter Float Value (Without Quotes):');
            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(theResponse, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter Float Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (Float): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');

        }

    } else if (nodeData.type === 'boolean') {

        if ((nodeName).startsWith("Literal")) {

            let portLabel = nodeName.split(' ');
            portLabel = portLabel[portLabel.length - 1];

            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(portLabel, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter Boolean Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (Boolean): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');

        }

    } else if (nodeData.type === 'list') {

        if ((nodeName).startsWith("Literal")) {

            let theResponse = window.prompt('Enter List Values (Without [] Brackets):');
            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(theResponse, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter List Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (List): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');

        }

    } else if (nodeData.type === 'tuple') {

        if ((nodeName).startsWith("Literal")) {

            let theResponse = window.prompt('Enter Tuple Values (Without () Brackets):');
            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(theResponse, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter Tuple Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (Tuple): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');
        }

    } else if (nodeData.type === 'dict') {

        if ((nodeName).startsWith("Literal")) {

            let theResponse = window.prompt('Enter Dict Values (Without {} Brackets):');
            node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance(theResponse, 'out-0');

        } else {

            let theResponse = window.prompt('notice', 'Enter Dict Name (Without Quotes):');
            node = new CustomNodeModel({ name: "Hyperparameter (Dict): " + theResponse, color: nodeData.color, extras: { "type": nodeData.type } });
            node.addOutPortEnhance('▶', 'parameter-out-0');

        }

    // } else if (props.type === 'debug') {
    //     node = new CustomNodeModel({ name: props.name, color: props.color, extras: { "type": props.type } });
    //     node.addInPortEnhance('▶', 'in-0');
    //     node.addInPortEnhance('props Set', 'parameter-in-1');
    //     node.addOutPortEnhance('▶', 'out-0');

    // } else if (props.type === 'enough') {

    //     node = new CustomNodeModel({ name: props.name, color: props.color, extras: { "type": props.type } });

    //     node.addInPortEnhance('▶', 'in-0');
    //     node.addInPortEnhance('Target Accuracy', 'parameter-float-in-1');
    //     node.addInPortEnhance('Max Retries', 'parameter-int-in-2');
    //     node.addInPortEnhance('Metrics', 'parameter-string-in-3');

    //     node.addOutPortEnhance('▶', 'out-0');
    //     node.addOutPortEnhance('Should Retrain', 'out-1');

    } else if (nodeData.type === 'literal') {

        node = new CustomNodeModel({ name: nodeName, color: nodeData.color, extras: { "type": nodeData.type } });
        node.addOutPortEnhance('Value', 'out-0');
    }
    return node;
}