# BackEnd_Kora_ITSM

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