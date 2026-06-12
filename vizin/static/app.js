// TELA DE PERFIL

// Função para gerenciar a mudança de foto e mostrar um preview
function iniciarPerfil() {
    // Busca os elementos que criamos no HTML
    const fileInput = document.getElementById('change-avatar-input');
    const avatarImage = document.querySelector('.profile-avatar');

    // Se os elementos existirem nessa página...
    if (fileInput && avatarImage) {
        // Escuta o evento de mudança do input
        fileInput.addEventListener('change', (event) => {
            // Pega o primeiro arquivo que foi selecionado
            const file = event.target.files[0];
            
            // Se houver um arquivo...
            if (file) {
                // Cria um objeto FileReader para ler o arquivo
                const reader = new FileReader();
                
                // Quando a leitura do arquivo terminar...
                reader.onload = (e) => {
                    // Altera a fonte (src) da imagem de perfil para o resultado da leitura
                    avatarImage.src = e.target.result; // Cria o preview
                    
                    // Alerta opcional para a apresentação:
                    alert('Nova foto de perfil selecionada para envio para o Back-End!');
                };
                
                // Inicia a leitura do arquivo como uma URL de dados
                reader.readAsDataURL(file);
            }
        });
    }
}


iniciarPerfil();