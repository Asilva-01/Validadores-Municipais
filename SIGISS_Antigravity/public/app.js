document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const cidadeSelect = document.getElementById('cidade-select');
    
    // Results DOM
    const resultsPanel = document.getElementById('results-panel');
    const badgeSucesso = document.getElementById('badge-sucesso');
    const badgeErro = document.getElementById('badge-erro');
    const progressFill = document.getElementById('progress-fill');
    
    // Stats
    const statLinhas = document.getElementById('stat-linhas');
    const statErros = document.getElementById('stat-erros');
    const statAvisos = document.getElementById('stat-avisos');
    const logContainer = document.getElementById('log-container');

    // UI Effects
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.name.endsWith('.txt') && !file.name.endsWith('.csv')) {
            alert('Apenas arquivos .txt ou .csv são suportados.');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            validateFile(content, file.name);
        };
        reader.readAsText(file, 'UTF-8');
    }

    async function validateFile(content, fileName) {
        const cidade = cidadeSelect.value;
        const payload = {
            cidade: cidade,
            conteudo: content
        };

        // Reset UI
        resultsPanel.style.display = 'block';
        logContainer.innerHTML = '<div class="log-entry" style="border-left-color: var(--accent-blue);"><div class="log-msg">Analisando Arquivo...</div></div>';
        progressFill.style.width = '20%';
        badgeSucesso.style.display = 'none';
        badgeErro.style.display = 'none';

        try {
            const response = await fetch('/api/validar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.erro || 'Erro desconhecido HTTP');
            }

            renderResults(data);

        } catch (error) {
            progressFill.style.width = '100%';
            progressFill.style.background = 'var(--error-red)';
            badgeErro.style.display = 'inline-flex';

            logContainer.innerHTML = '';

            const isNetworkError = error instanceof TypeError && (
                error.message === 'Failed to fetch' ||
                error.message.includes('NetworkError') ||
                error.message.includes('fetch')
            );

            if (isNetworkError) {
                badgeErro.textContent = 'SERVIDOR OFFLINE';
                appendLog({
                    nivel: 'ERRO',
                    linha: '—',
                    campo: 'Conexão',
                    mensagem: 'Não foi possível conectar ao servidor de validação. Certifique-se de que o servidor Python está em execução.',
                    valor: 'Execute: python web_server.py',
                    regra: 'Acesse a URL impressa no terminal (ex: http://localhost:PORTA)'
                });
            } else {
                badgeErro.textContent = 'ERRO DE API';
                appendLog({
                    nivel: 'ERRO',
                    linha: '—',
                    campo: 'API /validar',
                    mensagem: error.message,
                    valor: fileName,
                    regra: 'Comunicação API'
                });
            }
        }
    }

    function renderResults(data) {
        progressFill.style.width = '100%';
        
        if (data.sucesso) {
            badgeSucesso.style.display = 'inline-flex';
            progressFill.style.background = 'var(--success-green)';
        } else {
            badgeErro.style.display = 'inline-flex';
            badgeErro.textContent = 'FALHOU';
            progressFill.style.background = 'var(--error-red)';
        }

        let numErros = 0;
        let numAvisos = 0;

        logContainer.innerHTML = '';

        if (data.ocorrencias && data.ocorrencias.length > 0) {
            data.ocorrencias.forEach(ocorrencia => {
                if (ocorrencia.nivel === 'ERRO') numErros++;
                if (ocorrencia.nivel === 'AVISO') numAvisos++;
                appendLog(ocorrencia);
            });
        } else {
            logContainer.innerHTML = '<div class="log-entry" style="border-left-color: var(--success-green);"><div class="log-msg">Validação superada sem ressalvas! Arquivo perfeito.</div></div>';
        }

        statLinhas.textContent = data.total_linhas || 0;
        statErros.textContent = numErros;
        statAvisos.textContent = numAvisos;

        // Micro animation counts
        animateValue(statErros, 0, numErros, 500);
        animateValue(statAvisos, 0, numAvisos, 500);
        animateValue(statLinhas, 0, data.total_linhas || 0, 500);
    }

    function appendLog(log) {
        const isError = log.nivel === 'ERRO';
        const entry = document.createElement('div');
        entry.className = `log-entry ${isError ? 'log-error' : 'log-warn'}`;

        const linhaLabel = log.linha != null ? `L${log.linha}` : '—';

        entry.innerHTML = `
            <div class="log-meta">
                <span class="bag-linha">${linhaLabel}</span>
                <span class="bag-campo">${log.campo}</span>
            </div>
            <div class="log-msg">${log.mensagem}</div>
            <div class="log-detail"><strong>Detalhe:</strong> ${log.valor} &nbsp;|&nbsp; <em>${log.regra}</em></div>
        `;
        logContainer.appendChild(entry);
    }

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            obj.innerHTML = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = end; // Garantir valor final exato
            }
        };
        window.requestAnimationFrame(step);
    }
});
