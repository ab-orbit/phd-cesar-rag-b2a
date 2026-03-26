# 🔐 Pre-Commit Security Hook

## O que é?

Um **git hook** que **automaticamente detecta e bloqueia** commits contendo chaves API e secrets antes que eles cheguem ao GitHub.

## Por que foi criado?

**Você já perdeu 2 chaves API** que foram para o histórico do GitHub. Este hook **previne** que isso aconteça novamente.

## Como funciona?

Antes de cada `git commit`, o hook:

1. ✅ Verifica todos os arquivos que você está commitando
2. 🔍 Procura por padrões de chaves API (OpenAI, AWS, GitHub, etc.)
3. ⛔ **BLOQUEIA o commit** se encontrar algum secret
4. 📋 Mostra exatamente onde o secret foi encontrado (mascarado)

## Tipos de Secrets Detectados

- **OpenAI API Keys** (`sk-...`, `sk-proj-...`)
- **AWS Access Keys** (`AKIA...`)
- **GitHub Tokens** (`ghp_...`, `github_pat_...`)
- **Anthropic API Keys** (`sk-ant-...`)
- **Google API Keys** (`AIza...`)
- **Stripe API Keys** (`sk_live_...`)
- **Slack Tokens** (`xoxb-...`, `xoxp-...`)
- **Private Keys** (`-----BEGIN PRIVATE KEY-----`)
- **Langfuse Keys** (`pk-lf-...`, `sk-lf-...`)

## Exemplo de Uso

```bash
# Você tenta commitar um arquivo com uma chave API
$ git add notebook.ipynb
$ git commit -m "add new feature"

🔐 Verificando secrets antes do commit...
📋 Verificando 1 arquivo(s)...

❌ SECRETS DETECTADOS!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tipo: OpenAI API Key (proj)
Arquivo: notebook.ipynb
Linhas:
  → Linha 102: OPENAI_API_KEY = "sk-p***MASKED***EFGH"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ COMMIT BLOQUEADO POR SEGURANÇA
```

## Como Corrigir

### Opção 1: Mover para .env (RECOMENDADO)

```bash
# Crie/edite .env (já está no .gitignore)
echo "OPENAI_API_KEY=sk-proj-..." >> .env

# No código, use dotenv
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

### Opção 2: Usar Exemplo Falso

```python
# ❌ ERRADO: Chave real
OPENAI_API_KEY = "sk-proj-abc123..."

# ✅ CORRETO: Chave falsa óbvia
OPENAI_API_KEY = "sk-YOUR_KEY_HERE"
OPENAI_API_KEY = "sk-xxxxxxxx"
```

### Opção 3: Já Commitou? Desfaça!

```bash
# Desfazer último commit (mantém mudanças)
git reset HEAD~1

# Remova os secrets
vim arquivo.py

# Commit novamente (agora seguro)
git add arquivo.py
git commit -m "add feature (without secrets)"
```

## Forçar Commit (NÃO RECOMENDADO)

Se você **realmente** precisa fazer commit (ex: `.env.example` com valores falsos):

```bash
git commit --no-verify -m "mensagem"
```

⚠️ **ATENÇÃO:** Só use `--no-verify` se tiver **CERTEZA** de que não há secrets reais!

## Localização do Hook

```
.git/hooks/pre-commit
```

## Como Desabilitar (Temporariamente)

```bash
# Renomear hook (desabilita)
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled

# Reabilitar depois
mv .git/hooks/pre-commit.disabled .git/hooks/pre-commit
```

## Verificar se Está Ativo

```bash
# Testar o hook com uma chave falsa (20+ chars para ativar detector)
echo 'API_KEY=sk-proj-FAKE_KEY_FOR_TESTING_12345678' > test.txt
git add test.txt
git commit -m "test"

# Deveria BLOQUEAR com mensagem de erro
# Se bloqueou = ✅ Hook funcionando!

# Limpar teste
git reset && rm test.txt
```

## Importante

- ✅ Funciona **automaticamente** em todo commit
- ✅ Não afeta arquivos já commitados (só novos commits)
- ✅ Compatível com macOS, Linux e Windows (Git Bash)
- ✅ Não envia dados para lugar nenhum (100% local)

## Se GitHub Já Detectou Uma Chave

```bash
# 1. REVOGUE a chave imediatamente no provedor
#    (OpenAI: https://platform.openai.com/api-keys)

# 2. Gere uma nova chave

# 3. Atualize seu .env local
echo "OPENAI_API_KEY=nova_chave" > .env

# 4. NÃO TENTE limpar o histórico git
#    (a chave já foi exposta, não adianta)
```

## Referências

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Git Hooks Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Anthropic Best Practices for API Key Security](https://docs.anthropic.com/en/api/security)

---

**✅ Instalado automaticamente por Claude Code**
**📅 Data de instalação:** 2026-03-17
