function addInputs(inputIds) {
    inputIds.forEach( id => {
        let inputToAdd = document.getElementById(id);
        let inputContainer = inputToAdd.parentNode;

        inputToAdd.required = true;
        inputContainer.style.display = "";
    })
}

function removeInputs(inputIds) {
    inputIds.forEach( id => {
        let inputToAdd = document.getElementById(id);
        let inputContainer = inputToAdd.parentNode;

        inputToAdd.required = false;
        inputContainer.style.display = "None";
    })
}

function changeForm(selectInput ,trigger, inputIds){

    let selected = [...selectInput.options].find(element => element.selected);
    if (selected.value === trigger) {
        addInputs(inputIds);
    } else {
        removeInputs(inputIds);
    }

}

