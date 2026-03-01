# 🔍 Guia: Integrando SerperAPI com Agentes

## 📚 O que é SerperAPI?

SerperAPI é uma API de busca do Google que permite realizar pesquisas na web de forma programática. É uma alternativa mais simples e barata do que usar a Google Search API diretamente.

### Por que usar SerperAPI?

- ✅ **Fácil de usar**: API simples e bem documentada
- ✅ **Custo baixo**: Plano gratuito disponível
- ✅ **Resultados rápidos**: Respostas em tempo real
- ✅ **Integração simples**: Funciona bem com LangChain

---

## 🚀 Configuração Rápida

### 1. Criar Conta no SerperAPI

1. Acesse [serper.dev](https://serper.dev)
2. Crie uma conta gratuita
3. Obtenha sua API key no dashboard

### 2. Configurar no Projeto

Adicione no arquivo `.env`:

```env
SERPER_API_KEY=sua_chave_aqui
```

### 3. Instalar Dependências

```bash
pip install google-search-results langchain-community
```

---

## 💡 Como Funciona o Exemplo

### Arquitetura

```
┌──────────────┐
│   Usuário    │
│  (Pergunta)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Agent      │ → Decide usar busca web
│  (LangChain) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  SerperAPI   │ → Busca no Google
│  (Tool)      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Resultados  │ → Informações atualizadas
└──────────────┘
```

### Fluxo de Execução

1. **Usuário faz uma pergunta** sobre um destino
2. **Agente analisa** e decide que precisa buscar informações atualizadas
3. **Agente usa SerperAPI** para buscar na web
4. **Resultados são processados** pelo LLM
5. **Resposta final** é gerada com informações atualizadas

---

## 🎯 Casos de Uso

### 1. Informações Atualizadas

**Problema**: Ferramentas simuladas têm dados estáticos

**Solução**: SerperAPI busca informações em tempo real

```python
# Busca informações atuais sobre eventos
planejar_viagem_com_busca_web(
    destino="Paris",
    dias=5,
    pergunta_especifica="eventos em junho de 2024"
)
```

### 2. Notícias e Eventos

**Problema**: Precisa saber sobre eventos recentes

**Solução**: SerperAPI busca notícias e eventos atuais

```python
pesquisar_topicos_atuais([
    "festivais em Paris 2024",
    "melhores restaurantes em Tokyo"
])
```

### 3. Dados que Mudam Frequentemente

**Problema**: Clima, preços, disponibilidade mudam constantemente

**Solução**: SerperAPI sempre retorna dados atualizados

---

## 🔧 Modo Simulado vs Real

### Modo Simulado (Sem API Key)

Quando `SERPER_API_KEY` não está configurada:

- ✅ Código funciona normalmente
- ✅ Demonstra a estrutura
- ⚠️ Retorna dados simulados
- ⚠️ Não busca na web real

**Uso**: Para aprender e testar a estrutura

### Modo Real (Com API Key)

Quando `SERPER_API_KEY` está configurada:

- ✅ Busca real no Google
- ✅ Dados atualizados em tempo real
- ✅ Informações precisas
- ⚠️ Consome créditos da API

**Uso**: Para aplicações reais

---

## 📝 Exemplos de Queries

### Busca Simples

```python
# O agente automaticamente formata a query
"clima em Paris hoje"
```

### Busca Específica

```python
# Query mais específica
"melhores restaurantes em Tokyo 2024"
```

### Múltiplas Buscas

```python
# O agente pode fazer múltiplas buscas
pesquisar_topicos_atuais([
    "atrações em Paris",
    "clima em Paris",
    "eventos em Paris"
])
```

---

## 🎓 Conceitos Aprendidos

### 1. Integração de APIs Reais

- Como conectar APIs externas com agentes
- Tratamento de erros e fallbacks
- Modo simulado para desenvolvimento

### 2. Tools (Ferramentas) em LangChain

- Como criar tools customizadas
- Integração com wrappers de APIs
- Combinação de múltiplas ferramentas

### 3. Agentes com Acesso à Web

- Agentes que decidem quando buscar na web
- Processamento de resultados de busca
- Combinação de informações de múltiplas fontes

---

## ⚠️ Limitações e Considerações

### Limitações do SerperAPI

1. **Custo**: Plano gratuito tem limite de requisições
2. **Rate Limiting**: Pode ter limites de requisições por minuto
3. **Resultados**: Dependem da qualidade da busca do Google

### Boas Práticas

1. **Cache**: Considere cachear resultados para queries repetidas
2. **Validação**: Sempre valide resultados antes de usar
3. **Fallback**: Tenha um modo simulado como fallback
4. **Rate Limiting**: Implemente controle de taxa de requisições

---

## 🔄 Comparação: Simulado vs Real

| Aspecto | Ferramentas Simuladas | SerperAPI |
|---------|----------------------|-----------|
| **Dados** | Estáticos | Atualizados |
| **Custo** | Gratuito | Pode ter custo |
| **Velocidade** | Instantâneo | Depende da API |
| **Precisão** | Limitada | Alta |
| **Manutenção** | Manual | Automática |

---

## 🚀 Próximos Passos

1. **Experimente**: Teste com e sem API key
2. **Customize**: Adicione mais ferramentas de busca
3. **Combine**: Use SerperAPI com outras ferramentas
4. **Otimize**: Implemente cache e rate limiting

---

## 📚 Recursos

- [Documentação SerperAPI](https://serper.dev/docs)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [GoogleSerperAPIWrapper](https://python.langchain.com/docs/integrations/tools/google_serper)

---

## 💡 Dicas

- **Comece sem API key**: Entenda o código primeiro
- **Teste com API key**: Veja a diferença com dados reais
- **Monitore uso**: Acompanhe seu consumo de créditos
- **Use cache**: Evite buscas repetidas desnecessárias

---

**Boa busca! 🔍**
