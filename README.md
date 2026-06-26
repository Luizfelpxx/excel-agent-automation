# Excel Agent Automation

Uma solução completa de automação para contagem de máquinas por severidade em planilhas Excel, utilizando uma API Python e um complemento Excel.

## 📋 Funcionalidades

- **API Python** para gerenciar dados de agentes e contagem de máquinas
- **Complemento Excel** para integração direta com suas planilhas
- **Categorização automática** de máquinas: High, Medium, Critical, Low, Not Reported
- **Relatórios mensais** de contagem de máquinas por agente
- **Interface simples** e intuitiva

## 🏗️ Arquitetura

```
excel-agent-automation/
├── api/                    # API Python
│   ├── app.py
│   ├── requirements.txt
│   ├── models.py
│   ├── routes.py
│   └── config.py
├── excel-addon/            # Complemento Excel
│   ├── taskpane.html
│   ├── taskpane.js
│   ├── taskpane.css
│   └── manifest.xml
└── README.md
```

## 🚀 Quick Start

### API Python

```bash
cd api
pip install -r requirements.txt
python app.py
```

A API estará disponível em `http://localhost:5000`

### Complemento Excel

1. Abra o Excel
2. Vá para **Inserir > Obter Complementos > Meus Complementos > Carregar Complemento Personalizado**
3. Selecione o arquivo `manifest.xml` do diretório `excel-addon`

## 📚 Endpoints da API

### Agentes

- `GET /api/agents` - Listar todos os agentes
- `POST /api/agents` - Criar novo agente
- `GET /api/agents/<id>` - Obter agente específico
- `PUT /api/agents/<id>` - Atualizar agente
- `DELETE /api/agents/<id>` - Deletar agente

### Máquinas

- `GET /api/machines` - Listar todas as máquinas
- `POST /api/machines` - Criar nova máquina
- `GET /api/machines/count-by-severity` - Obter contagem por severidade
- `GET /api/machines/monthly-report/<agent_id>/<month>/<year>` - Relatório mensal

## 🔧 Configuração

Configure as variáveis de ambiente em `.env`:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///machines.db
API_PORT=5000
API_HOST=localhost
```

## 📝 Severidades Suportadas

- **High** - Alta prioridade
- **Medium** - Média prioridade
- **Critical** - Crítica
- **Low** - Baixa prioridade
- **Not Reported** - Não reportado

## 👨‍💻 Desenvolvimento

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT.

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.
