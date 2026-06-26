// Variáveis globais
let API_URL = 'http://localhost:5000';
let agents = [];
let currentReport = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Carregar URL da API do localStorage
    const savedUrl = localStorage.getItem('apiUrl');
    if (savedUrl) {
        API_URL = savedUrl;
        document.getElementById('apiUrl').value = API_URL;
    }

    // Event listeners
    document.getElementById('apiUrl').addEventListener('change', function(e) {
        API_URL = e.target.value;
        localStorage.setItem('apiUrl', API_URL);
    });

    document.getElementById('testConnection').addEventListener('click', testConnection);
    document.getElementById('loadData').addEventListener('click', loadReport);
    document.getElementById('addMachine').addEventListener('click', addMachine);

    // Carregar agentes ao iniciar
    loadAgents();
    
    // Definir mês/ano atual
    const now = new Date();
    document.getElementById('monthSelect').value = now.getMonth() + 1;
    document.getElementById('yearSelect').value = now.getFullYear();
    document.getElementById('newMachineMonth').value = now.getMonth() + 1;
    document.getElementById('newMachineYear').value = now.getFullYear();
});

// ==================== CONEXÃO ====================

async function testConnection() {
    try {
        const response = await fetch(`${API_URL}/api/health`);
        if (response.ok) {
            const data = await response.json();
            showStatus('✅ Conexão estabelecida com sucesso!', 'success');
            loadAgents();
        } else {
            showStatus('❌ Erro ao conectar com a API', 'error');
        }
    } catch (error) {
        showStatus(`❌ Erro de conexão: ${error.message}`, 'error');
    }
}

// ==================== AGENTES ====================

async function loadAgents() {
    try {
        const response = await fetch(`${API_URL}/api/agents`);
        if (response.ok) {
            agents = await response.json();
            
            // Atualizar select de carregamento
            const select1 = document.getElementById('agentSelect');
            select1.innerHTML = '<option value="">-- Selecione um agente --</option>';
            agents.forEach(agent => {
                const option = document.createElement('option');
                option.value = agent.id;
                option.textContent = agent.name;
                select1.appendChild(option);
            });

            // Atualizar select de inserção
            const select2 = document.getElementById('newAgentSelect');
            select2.innerHTML = '';
            agents.forEach(agent => {
                const option = document.createElement('option');
                option.value = agent.id;
                option.textContent = agent.name;
                select2.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Erro ao carregar agentes:', error);
        showStatus(`❌ Erro ao carregar agentes: ${error.message}`, 'error');
    }
}

// ==================== RELATÓRIOS ====================

async function loadReport() {
    const agentId = document.getElementById('agentSelect').value;
    const month = document.getElementById('monthSelect').value;
    const year = document.getElementById('yearSelect').value;

    if (!agentId) {
        showStatus('⚠️ Selecione um agente', 'warning');
        return;
    }

    try {
        const endpoint = `/api/machines/monthly-report/${agentId}/${month}/${year}`;
        const response = await fetch(`${API_URL}${endpoint}`);
        
        if (response.ok) {
            const data = await response.json();
            currentReport = data;
            displayReport(data);
            showStatus('✅ Relatório carregado com sucesso', 'success');
        } else {
            const error = await response.json();
            showStatus(`❌ ${error.error}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Erro ao carregar relatório: ${error.message}`, 'error');
    }
}

function displayReport(data) {
    const resultDiv = document.getElementById('result');
    const { agent_name, month, year, machines, summary } = data;
    
    const monthNames = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    
    let html = `
        <div class="report">
            <h3>📊 Relatório Mensal</h3>
            <p><strong>Agente:</strong> ${agent_name}</p>
            <p><strong>Período:</strong> ${monthNames[month]}/${year}</p>
            
            <h4>Contagem por Severidade:</h4>
            <table class="table">
                <thead>
                    <tr>
                        <th>Severidade</th>
                        <th>Quantidade</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    for (const [severity, count] of Object.entries(summary.counts)) {
        const badge = getSeverityBadge(severity);
        html += `
            <tr>
                <td>${badge} ${severity}</td>
                <td><strong>${count}</strong></td>
            </tr>
        `;
    }
    
    html += `
                </tbody>
            </table>
            
            <h4>Total de Máquinas: <span class="badge">${summary.total}</span></h4>
            
            <h4>Máquinas Listadas:</h4>
            <table class="table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Severidade</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    if (machines.length > 0) {
        machines.forEach(machine => {
            const badge = getSeverityBadge(machine.severity);
            html += `
                <tr>
                    <td>${machine.name}</td>
                    <td>${badge} ${machine.severity}</td>
                </tr>
            `;
        });
    } else {
        html += '<tr><td colspan="2">Nenhuma máquina encontrada</td></tr>';
    }
    
    html += `
                </tbody>
            </table>
            
            <button class="btn btn-primary" onclick="insertIntoExcel()">📊 Inserir na Planilha</button>
    `;
    
    resultDiv.innerHTML = html;
}

function getSeverityBadge(severity) {
    const badges = {
        'Critical': '🔴',
        'High': '🟠',
        'Medium': '🟡',
        'Low': '🟢',
        'Not Reported': '⚪'
    };
    return badges[severity] || '❓';
}

// ==================== INSERÇÃO DE DADOS ====================

async function addMachine() {
    const agentId = document.getElementById('newAgentSelect').value;
    const name = document.getElementById('machineName').value;
    const severity = document.getElementById('machineSeverity').value;
    const month = document.getElementById('newMachineMonth').value;
    const year = document.getElementById('newMachineYear').value;

    // Validações
    if (!agentId) {
        showStatus('⚠️ Selecione um agente', 'warning');
        return;
    }
    if (!name) {
        showStatus('⚠️ Insira o nome da máquina', 'warning');
        return;
    }
    if (!severity) {
        showStatus('⚠️ Selecione uma severidade', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/machines`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                severity: severity,
                agent_id: parseInt(agentId),
                month: parseInt(month),
                year: parseInt(year)
            })
        });

        if (response.status === 201) {
            const data = await response.json();
            showStatus('✅ Máquina adicionada com sucesso!', 'success');
            
            // Limpar formulário
            document.getElementById('machineName').value = '';
            document.getElementById('machineSeverity').value = '';
            
            // Recarregar relatório se houver um carregado
            if (currentReport) {
                loadReport();
            }
        } else {
            const error = await response.json();
            showStatus(`❌ ${error.error}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Erro ao adicionar máquina: ${error.message}`, 'error');
    }
}

// ==================== INTEGRAÇÃO EXCEL ====================

function insertIntoExcel() {
    if (!currentReport) {
        showStatus('⚠️ Nenhum relatório carregado', 'warning');
        return;
    }

    Office.onReady((reason) => {
        if (reason === Office.HostType.Excel) {
            Excel.run(async (context) => {
                try {
                    const { agent_name, month, year, summary } = currentReport;
                    
                    // Encontrar ou criar planilha
                    let sheet = context.workbook.worksheets.getItemOrNullObject('Relatório');
                    
                    if (sheet.isNullObject) {
                        sheet = context.workbook.worksheets.add('Relatório');
                    }
                    
                    sheet.activate();
                    
                    // Limpar conteúdo anterior
                    sheet.getUsedRange().clear();
                    
                    // Cabeçalho
                    const monthNames = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                                        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
                    
                    sheet.getCell(0, 0).values = [['Relatório de Máquinas']];
                    sheet.getCell(1, 0).values = [['Agente: ' + agent_name]];
                    sheet.getCell(2, 0).values = [['Período: ' + monthNames[month] + '/' + year]];
                    sheet.getCell(4, 0).values = [['Severidade', 'Quantidade']];
                    
                    // Dados de contagem
                    let row = 5;
                    for (const [severity, count] of Object.entries(summary.counts)) {
                        sheet.getCell(row, 0).values = [[severity, count]];
                        row++;
                    }
                    
                    row++;
                    sheet.getCell(row, 0).values = [['Total', summary.total]];
                    
                    // Formatar
                    const range = sheet.getUsedRange();
                    range.format.autofitColumns();
                    range.format.autofitRows();
                    
                    // Formatar cabeçalho
                    sheet.getCell(4, 0).format.font.bold = true;
                    sheet.getCell(4, 1).format.font.bold = true;
                    
                    await context.sync();
                    showStatus('✅ Dados inseridos na planilha com sucesso!', 'success');
                    
                } catch (error) {
                    showStatus(`❌ Erro ao inserir dados: ${error.message}`, 'error');
                }
            });
        }
    });
}

// ==================== UTILITÁRIOS ====================

function showStatus(message, type = 'info') {
    const statusDiv = document.getElementById('connectionStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-message status-${type}`;
    
    // Auto-limpar após 5 segundos
    if (type !== 'error') {
        setTimeout(() => {
            statusDiv.textContent = '';
            statusDiv.className = 'status-message';
        }, 5000);
    }
}