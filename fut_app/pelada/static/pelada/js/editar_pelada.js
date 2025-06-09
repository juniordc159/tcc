// Calcular média de um jogador
function calculatePlayerAverage(playerRow) {
    const attack = parseInt(playerRow.querySelector('input[name*="attack"]').value) || 0;
    const defense = parseInt(playerRow.querySelector('input[name*="defense"]').value) || 0;
    const speed = parseInt(playerRow.querySelector('input[name*="speed"]').value) || 0;
    const control = parseInt(playerRow.querySelector('input[name*="control"]').value) || 0;
    const pass = parseInt(playerRow.querySelector('input[name*="pass"]').value) || 0;
    
    return (attack + defense + speed + control + pass) / 5;
}

// Atualizar média de um jogador
function updatePlayerAverage(playerRow) {
    const average = calculatePlayerAverage(playerRow);
    const avgBadge = playerRow.querySelector('.avg-badge');
    
    avgBadge.textContent = average.toFixed(1);
    
    // Atualizar classe de cor
    avgBadge.classList.remove('avg-high', 'avg-medium', 'avg-low');
    if (average >= 7) {
        avgBadge.classList.add('avg-high');
    } else if (average >= 5) {
        avgBadge.classList.add('avg-medium');
    } else {
        avgBadge.classList.add('avg-low');
    }
}

// Atualizar estatísticas gerais
function updateStats() {
    const playerRows = document.querySelectorAll('#players-tbody tr');
    let totalPlayers = playerRows.length;
    let selectedPlayers = 0;
    let totalAverage = 0;
    let selectedAverage = 0;
    
    playerRows.forEach(row => {
        if (row.querySelector('.no-players-message')) return;
        
        const isSelected = row.querySelector('input[type="checkbox"]').checked;
        const playerAvg = calculatePlayerAverage(row);
        
        totalAverage += playerAvg;
        
        if (isSelected) {
            selectedPlayers++;
            selectedAverage += playerAvg;
        }
    });
    
    // Atualizar estatísticas na página
    document.getElementById('total-players').textContent = totalPlayers;
    document.getElementById('selected-players').textContent = selectedPlayers;
    
    const avgRating = totalPlayers > 0 ? (totalAverage / totalPlayers).toFixed(1) : 0;
    document.getElementById('avg-rating').textContent = avgRating;
    
    const avgSelected = selectedPlayers > 0 ? (selectedAverage / selectedPlayers).toFixed(1) : 0;
    document.getElementById('avg-selected').textContent = avgSelected;
}

// Adicionar novo jogador
function addNewPlayer() {
    const name = prompt('Digite o nome do novo jogador:');
    if (name && name.trim()) {
        const tbody = document.getElementById('players-tbody');
        
        // Remove a mensagem de "Nenhum jogador" se existir
        const noPlayersMsg = tbody.querySelector('.no-players-message');
        if (noPlayersMsg) {
            noPlayersMsg.closest('tr').remove();
        }
        
        const newId = 'new_' + Date.now();
        
        const newRow = document.createElement('tr');
        newRow.className = 'player-row';
        newRow.dataset.playerId = newId;
        newRow.innerHTML = `
            <td class="player-name">
                <input type="text" name="player_name" value="${name.trim()}" class="player-name-input" required>
            </td>
            <td>
                <div class="checkbox-wrapper">
                    <label class="custom-checkbox">
                        <input type="checkbox" name="player_selected">
                        <span class="checkmark"></span>
                    </label>
                </div>
            </td>
            <td>
                <input type="number" class="skill-input" name="player_attack" min="0" max="10" value="5" required>
            </td>
            <td>
                <input type="number" class="skill-input" name="player_defense" min="0" max="10" value="5" required>
            </td>
            <td>
                <input type="number" class="skill-input" name="player_speed" min="0" max="10" value="5" required>
            </td>
            <td>
                <input type="number" class="skill-input" name="player_control" min="0" max="10" value="5" required>
            </td>
            <td>
                <input type="number" class="skill-input" name="player_pass" min="0" max="10" value="5" required>
            </td>
            <td class="player-avg">
                <span class="avg-badge avg-medium">5.0</span>
            </td>
            <td>
                <div class="action-buttons">
                    <input type="hidden" name="player_id" value="${newId}">
                    <button type="button" class="btn-icon btn-delete" onclick="removePlayer('${newId}')" title="Remover jogador">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        
        tbody.appendChild(newRow);
        updateStats();
        
        // Feedback visual
        newRow.style.background = 'rgba(0, 204, 102, 0.3)';
        setTimeout(() => {
            newRow.style.background = '';
        }, 2000);
    }
}

// Adicionar múltiplos jogadores
function addMultiplePlayers() {
    const names = prompt('Digite os nomes dos jogadores separados por vírgula:');
    if (names && names.trim()) {
        const nameList = names.split(',').map(name => name.trim()).filter(name => name);
        const tbody = document.getElementById('players-tbody');
        
        // Remove a mensagem de "Nenhum jogador" se existir
        const noPlayersMsg = tbody.querySelector('.no-players-message');
        if (noPlayersMsg) {
            noPlayersMsg.closest('tr').remove();
        }
        
        nameList.forEach(name => {
            if (name) {
                const newId = 'new_' + (Date.now() + Math.floor(Math.random() * 1000));
                
                const newRow = document.createElement('tr');
                newRow.className = 'player-row';
                newRow.dataset.playerId = newId;
                newRow.innerHTML = `
                    <td class="player-name">
                        <input type="text" name="player_name" value="${name}" class="player-name-input" required>
                    </td>
                    <td>
                        <div class="checkbox-wrapper">
                            <label class="custom-checkbox">
                                <input type="checkbox" name="player_selected">
                                <span class="checkmark"></span>
                            </label>
                        </div>
                    </td>
                    <td>
                        <input type="number" class="skill-input" name="player_attack" min="0" max="10" value="5" required>
                    </td>
                    <td>
                        <input type="number" class="skill-input" name="player_defense" min="0" max="10" value="5" required>
                    </td>
                    <td>
                        <input type="number" class="skill-input" name="player_speed" min="0" max="10" value="5" required>
                    </td>
                    <td>
                        <input type="number" class="skill-input" name="player_control" min="0" max="10" value="5" required>
                    </td>
                    <td>
                        <input type="number" class="skill-input" name="player_pass" min="0" max="10" value="5" required>
                    </td>
                    <td class="player-avg">
                        <span class="avg-badge avg-medium">5.0</span>
                    </td>
                    <td>
                        <div class="action-buttons">
                            <input type="hidden" name="player_id" value="${newId}">
                            <button type="button" class="btn-icon btn-delete" onclick="removePlayer('${newId}')" title="Remover jogador">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                `;
                
                tbody.appendChild(newRow);
            }
        });
        
        updateStats();
        alert(`${nameList.length} jogador(es) adicionado(s) com sucesso!`);
    }
}

// Remover jogador
function removePlayer(playerId) {
    if (confirm('Tem certeza que deseja remover este jogador?')) {
        const row = document.querySelector(`tr[data-player-id="${playerId}"]`);
        if (row) {
            row.remove();
            updateStats();
            
            // Se não houver mais jogadores, mostra a mensagem
            const tbody = document.getElementById('players-tbody');
            if (tbody.children.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="9" class="text-center">
                            <div class="no-players-message">
                                Nenhum jogador cadastrado ainda
                            </div>
                        </td>
                    </tr>
                `;
            }
        }
    }
}

// Inicializar eventos
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar médias quando os valores mudam
    document.getElementById('players-tbody').addEventListener('change', function(e) {
        if (e.target.classList.contains('skill-input') || e.target.type === 'checkbox') {
            const playerRow = e.target.closest('tr');
            if (playerRow) {
                updatePlayerAverage(playerRow);
                updateStats();
            }
        }
    });

    // Atualizar estatísticas iniciais
    updateStats();
}); 