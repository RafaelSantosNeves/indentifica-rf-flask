                //pega o input cpf pelo id e coloca ele em uma var
                const cpfInput = document.getElementById("inpCpf");

//adiciona um evento sempre que for escrever algo no input e onoloca o encente no input
cpfInput.addEventListener("input", (event) => {

    // remove tudo que não é número
    let value = event.target.value.replace(/\D/g, "");
    
    // limita o valor a 11 caracteres
    value = value.substring(0, 11); 

    // adiciona pontos e traço para formatar o CPF
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    //devolve as configs do input para os input
    event.target.value = value;
});