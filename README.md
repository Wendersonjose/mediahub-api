# Posts API - FastAPI

API REST para upload e gerenciamento de posts com imagens e vídeos, utilizando FastAPI e ImageKit para armazenamento de mídia.

## 🚀 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido para construção de APIs
- **SQLAlchemy** - ORM para interação com banco de dados
- **SQLite** - Banco de dados leve (com suporte assíncrono via aiosqlite)
- **ImageKit** - Serviço de CDN e otimização de imagens
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI de alta performance
- **UV** - Gerenciador de pacotes Python moderno

## 📁 Estrutura do Projeto

```
.
├── app/
│   ├── __init__.py         # Inicializador do módulo
│   ├── main.py             # Aplicação FastAPI principal
│   ├── db.py               # Configuração do banco de dados
│   ├── images.py           # Integração com ImageKit
│   ├── schemas.py          # Schemas Pydantic
│   └── routes/
│       ├── __init__.py     # Inicializador de rotas
│       └── posts.py        # Endpoints de posts
├── .env                    # Variáveis de ambiente (não versionado)
├── .env.example            # Template de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── pyproject.toml          # Dependências e configurações
└── README.md               # Este arquivo
```

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd streamlit
```

### 2. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure suas credenciais do ImageKit:

1. Acesse [https://imagekit.io/](https://imagekit.io/)
2. Faça login ou crie uma conta
3. Vá em **Developer options**
4. Copie as chaves e cole no arquivo `.env`:

```env
IMAGEKIT_PRIVATE_KEY=sua_chave_privada
IMAGEKIT_PUBLIC_KEY=sua_chave_publica
IMAGEKIT_URL=https://ik.imagekit.io/seu_id
```

### 3. Instale as dependências

Este projeto usa [UV](https://github.com/astral-sh/uv) como gerenciador de pacotes:

```bash
uv sync
```

## 🏃 Como Executar

Execute a aplicação com o comando:

```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em:

- **API**: http://127.0.0.1:8000
- **Documentação Swagger**: http://127.0.0.1:8000/docs
- **Documentação ReDoc**: http://127.0.0.1:8000/redoc

## 📚 Endpoints Disponíveis

### `GET /`
Health check da API.

**Resposta:**
```json
{
  "message": "Posts API is running",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### `POST /posts/upload`
Faz upload de uma imagem ou vídeo.

**Parâmetros:**
- `file` (UploadFile) - Arquivo de imagem ou vídeo
- `caption` (string, opcional) - Legenda do post

**Resposta:**
```json
{
  "id": "uuid",
  "caption": "Minha foto",
  "url": "https://...",
  "file_type": "image",
  "file_name": "foto.jpg",
  "created_at": "2026-05-12T10:30:00"
}
```

### `GET /posts/feed`
Retorna todos os posts ordenados por data (mais recentes primeiro).

**Resposta:**
```json
{
  "posts": [
    {
      "id": "uuid",
      "caption": "Minha foto",
      "url": "https://...",
      "file_type": "image",
      "file_name": "foto.jpg",
      "created_at": "2026-05-12T10:30:00"
    }
  ]
}
```

### `DELETE /posts/{post_id}`
Deleta um post específico.

**Parâmetros:**
- `post_id` (UUID) - ID do post a ser deletado

**Resposta:**
```json
{
  "success": true,
  "message": "Post deleted"
}
```

## 🧪 Testando a API

### Usando a documentação interativa (Swagger)

1. Acesse http://127.0.0.1:8000/docs
2. Clique no endpoint que deseja testar
3. Clique em **"Try it out"**
4. Preencha os parâmetros necessários
5. Clique em **"Execute"**

### Usando cURL

**Upload de arquivo:**
```bash
curl -X POST "http://127.0.0.1:8000/posts/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/para/imagem.jpg" \
  -F "caption=Minha foto"
```

**Obter feed:**
```bash
curl -X GET "http://127.0.0.1:8000/posts/feed"
```

**Deletar post:**
```bash
curl -X DELETE "http://127.0.0.1:8000/posts/{post_id}"
```

## 🗃️ Banco de Dados

O projeto utiliza SQLite com suporte assíncrono. O arquivo `teste.db` é criado automaticamente na primeira execução.

**Modelo Post:**
- `id` (UUID) - Identificador único
- `caption` (Text) - Legenda do post
- `url` (String) - URL da mídia no ImageKit
- `file_type` (String) - Tipo: "image" ou "video"
- `file_name` (String) - Nome do arquivo
- `created_at` (DateTime) - Data de criação

## 📝 Desenvolvimento

### Adicionar novas rotas

1. Crie um novo arquivo em `app/routes/`
2. Defina seu `APIRouter`
3. Inclua o router em `app/main.py`:

```python
from app.routes import novo_router

app.include_router(novo_router.router)
```

### Estrutura de uma rota

```python
from fastapi import APIRouter

router = APIRouter(prefix="/exemplo", tags=["exemplo"])

@router.get("/")
async def exemplo():
    return {"message": "Hello World"}
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é para fins educacionais.

## 👨‍💻 Autor

Desenvolvido como parte da disciplina **Tópicos Especiais em S.I** - Faculdade ADS
