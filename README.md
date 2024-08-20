# BackEnd_Kora_ITSM

/my_flask_project/
│
├── /app/
│   ├── /models/
│   │   ├── __init__.py
│   │   ├── tb_tickets.py
│   │   └── tb_tickets_tasks.py
│   │   └── ...
│   │
│   ├── /controllers/
│   │   ├── __init__.py
│   │   ├── tickets_controller.py
│   │   └── ...
│   │
│   ├── /views/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── __init__.py
│   └── config.py
│
├── run.py
├── .env
├── .env.example
└── requirements.txt

## Configuração do Ambiente Virtual

### Linux/WSL

Para configurar o ambiente virtual no Linux ou WSL, siga os passos abaixo:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

Para configurar o ambiente virtual no Windows, siga os passos abaixo:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## Instalação das Dependências

Após ativar o ambiente virtual, instale as dependências do projeto utilizando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## Executando o Projeto

Para iniciar o servidor Flask, utilize o seguinte comando:

```bash
python app.py
```