# API - Inventário de Jogos

API RESTful desenvolvida em Python utilizando Flask e SQLite para gerenciamento de um inventário de jogos. A aplicação permite operações completas de CRUD seguindo boas práticas de APIs REST.

---

## Objetivo

Fornecer um serviço backend para cadastro, consulta, atualização e remoção de jogos, com persistência em banco de dados SQLite.

---

## Funcionalidades

* Listar todos os jogos cadastrados
* Buscar um jogo por ID
* Inserir novos jogos
* Atualizar dados de jogos existentes
* Remover jogos do sistema

---

## Tecnologias utilizadas

* Python
* Flask
* SQLite
* JSON

---

## Estrutura do projeto

```bash
CRUD/
│
├── app.py          # API Flask com rotas
├── init_db.py      # Script de criação do banco
└── database.db     # Banco de dados (gerado automaticamente)
```

---

## Instalação e execução

### 1. Instalar dependências

```bash
pip install flask
```

---

### 2. Inicializar o banco de dados

```bash
python init_db.py
```

---

### 3. Executar a aplicação

```bash
python app.py
```

---

## Acesso

Servidor local:

```
http://127.0.0.1:5000
```

---

## Endpoints da API

### 1. Listar todos os jogos

* Método: GET
* Rota: `/jogos`
* Status: 200 OK

```bash
curl http://127.0.0.1:5000/jogos
```

---

### 2. Buscar jogo por ID

* Método: GET
* Rota: `/jogos/{id}`
* Status: 200 OK / 404 Not Found

```bash
curl http://127.0.0.1:5000/jogos/1
```

---

### 3. Inserir novo jogo

* Método: POST
* Rota: `/jogos`
* Status: 201 Created

#### Corpo da requisição:

```json
{
  "titulo": "Minecraft",
  "genero": "Sandbox",
  "plataforma": "PC",
  "preco": 79.90
}
```

```bash
curl -X POST http://127.0.0.1:5000/jogos \
-H "Content-Type: application/json" \
-d '{"titulo":"Minecraft","genero":"Sandbox","plataforma":"PC","preco":79.90}'
```

---

### 4. Atualizar jogo

* Método: PUT
* Rota: `/jogos/{id}`
* Status: 204 No Content / 404 Not Found

```bash
curl -X PUT http://127.0.0.1:5000/jogos/1 \
-H "Content-Type: application/json" \
-d '{"titulo":"Minecraft","genero":"Sandbox","plataforma":"PC","preco":89.90}'
```

---

### 5. Remover jogo

* Método: DELETE
* Rota: `/jogos/{id}`
* Status: 200 OK / 404 Not Found

```bash
curl -X DELETE http://127.0.0.1:5000/jogos/1
```

---

## Testes via PowerShell

### Listar jogos

```powershell
Invoke-RestMethod http://127.0.0.1:5000/jogos
```

---

### Inserir jogo

```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:5000/jogos -Headers @{ "Content-Type" = "application/json" } -Body '{"titulo":"GTA V","genero":"Acao","plataforma":"PC","preco":99.90}'
```

---

## Modelo de dados

Tabela: `jogos`

| Campo      | Tipo    | Descrição           |
| ---------- | ------- | ------------------- |
| id         | INTEGER | Identificador único |
| titulo     | TEXT    | Nome do jogo        |
| genero     | TEXT    | Gênero do jogo      |
| plataforma | TEXT    | Plataforma          |
| preco      | REAL    | Preço               |

---

## Boas práticas aplicadas

* Uso de padrão REST
* Organização do código
* Retorno em formato JSON
* Uso correto de códigos de status HTTP
* Persistência com SQLite

---

## Observações

* O arquivo `database.db` é criado automaticamente ao executar `init_db.py`.
* O banco de dados não deve ser enviado ao repositório.
* Em ambientes Windows, pode haver problemas com acentuação no PowerShell.

---

## Autor

Geovane Alves
