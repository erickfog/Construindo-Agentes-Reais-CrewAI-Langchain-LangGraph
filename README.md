# 🚀 Aula Prática: Construindo Agentes com CrewAI, LangChain e LangGraph

## 📚 Objetivo da Aula

Esta aula prática ensina os conceitos fundamentais de construção de agentes de IA através de uma aplicação real: **planejamento de viagens**. Você aprenderá a implementar a mesma funcionalidade usando três frameworks diferentes, compreendendo suas diferenças, vantagens e casos de uso.

## 🎯 Conceitos Aprendidos

- **Tools (Ferramentas)**: Como agentes interagem com o mundo externo
- **Planejamento**: Como agentes organizam e planejam tarefas
- **Memória/Estado**: Como agentes mantêm contexto durante a execução
- **Execução de Tarefas**: Como agentes executam ações sequenciais ou paralelas
- **Orquestração**: Como coordenar múltiplos agentes ou etapas

---

## 🏗️ Arquitetura da Aplicação

Nossa aplicação de **Planejamento de Viagem** realiza as seguintes tarefas:

1. **Pesquisar Clima**: Consulta condições climáticas do destino
2. **Buscar Atrações**: Encontra pontos turísticos principais
3. **Verificar Visto**: Checa requisitos de documentação
4. **Calcular Orçamento**: Estima custos da viagem
5. **Criar Plano Final**: Gera um roteiro completo e organizado

### Ferramentas Simuladas

Todas as ferramentas estão em `tools.py` e são funções Python simples que simulam APIs externas:
- `consultar_clima()`: Retorna informações climáticas
- `buscar_atracoes()`: Lista atrações turísticas
- `verificar_visto()`: Informa sobre requisitos de visto
- `calcular_orcamento()`: Calcula custos estimados

---

## 🛠️ Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_api_aqui
SERPER_API_KEY=sua_chave_serper_aqui  # Opcional: para busca web real
```

**Nota Importante**: 
- Os exemplos **LangChain** e **LangGraph** requerem uma API key da OpenAI
- O exemplo **CrewAI** também usa LLM, mas pode ser configurado com outros modelos
- O exemplo **SerperAPI** funciona sem API key (modo simulado), mas para busca real você precisa:
  1. Criar uma conta em [serper.dev](https://serper.dev)
  2. Obter sua API key gratuita
  3. Adicionar `SERPER_API_KEY=sua_chave` no arquivo `.env`
- Para testar apenas as ferramentas simuladas, você pode executar diretamente o arquivo `tools.py` ou criar um script simples que as chama

### 3. Testar as Ferramentas (Opcional)

Antes de executar os agentes, você pode testar as ferramentas isoladamente:

```bash
python test_tools.py
```

Ou teste manualmente:

```python
from tools import consultar_clima, buscar_atracoes, calcular_orcamento

# Testar ferramentas
print(consultar_clima("Paris", "2024-06-01"))
print(buscar_atracoes("Tokyo"))
print(calcular_orcamento("Rio de Janeiro", 7, "hotel"))
```

---

## 📖 Implementações

### 1. CrewAI - Agentes em Equipe

**Arquivo**: `crewai_example.py`

#### Conceito
CrewAI facilita a criação de **equipes de agentes especializados**. Cada agente tem um papel específico e trabalha em conjunto.

#### Arquitetura
```
┌─────────────────┐
│  Agent 1        │ → Pesquisa informações
│  (Pesquisador)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent 2        │ → Cria plano de viagem
│  (Planejador)   │
└─────────────────┘
```

#### Características
- ✅ **Fácil de usar**: Abstração de alto nível
- ✅ **Multi-agente**: Suporta equipes de agentes
- ✅ **Delegação**: Agentes podem delegar tarefas
- ⚠️ **Menos controle**: Menos flexibilidade para casos específicos

#### Executar
```bash
python crewai_example.py
```

---

### 2. LangChain - Controle Total

**Arquivo**: `langchain_example.py`

#### Conceito
LangChain oferece **controle granular** sobre cada aspecto do agente. Você define explicitamente ferramentas, prompts e comportamento.

#### Arquitetura
```
┌─────────────────┐
│   Agent         │
│   (LLM + Tools) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AgentExecutor  │ → Loop até completar
│  (Orquestrador) │
└─────────────────┘
```

#### Características
- ✅ **Flexível**: Controle total sobre o comportamento
- ✅ **Granular**: Acesso a cada etapa do processo
- ✅ **Ecosystem**: Grande ecossistema de integrações
- ⚠️ **Mais código**: Requer mais configuração manual

#### Executar
```bash
python langchain_example.py
```

---

### 3. LangGraph - Fluxos Definidos

**Arquivo**: `langgraph_example.py`

#### Conceito
LangGraph permite criar **fluxos de trabalho complexos** com controle de estado. Ideal para processos com etapas bem definidas.

#### Arquitetura
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Nó 1    │ → │  Nó 2    │ → │  Nó 3    │ → │  Nó 4    │
│  Clima   │    │ Atrações │    │  Visto   │    │Orçamento│
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                     │
                                                     ▼
                                              ┌──────────┐
                                              │  Nó 5    │
                                              │  Plano   │
                                              └──────────┘
```

#### Características
- ✅ **Fluxo explícito**: Cada etapa é um nó definido
- ✅ **Estado compartilhado**: Fácil gerenciamento de contexto
- ✅ **Condicionais**: Suporta ramificações e loops
- ⚠️ **Mais complexo**: Requer mais planejamento inicial

#### Executar
```bash
python langgraph_example.py
```

---

### 4. SerperAPI - Busca Web Real

**Arquivo**: `serperapi_example.py`

#### Conceito
Este exemplo demonstra como integrar uma **API real** (SerperAPI) com agentes LangChain para realizar buscas na web e obter informações atualizadas em tempo real.

#### Arquitetura
```
┌─────────────────┐
│   Agent         │
│   (LLM + Tools) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SerperAPI      │ → Busca real na web
│  (Google Search)│
└─────────────────┘
```

#### Características
- ✅ **Busca Real**: Acesso a informações atualizadas da web
- ✅ **Tempo Real**: Dados em tempo real via Google Search
- ✅ **Flexível**: Combina busca web com ferramentas simuladas
- ✅ **Modo Simulado**: Funciona sem API key (para testes)
- ⚠️ **Requer API Key**: Para busca real, precisa de conta SerperAPI

#### Configuração

1. **Criar conta no SerperAPI** (gratuito):
   - Acesse [serper.dev](https://serper.dev)
   - Crie uma conta e obtenha sua API key

2. **Adicionar no `.env`**:
   ```env
   SERPER_API_KEY=sua_chave_aqui
   ```

3. **Sem API key**: O exemplo funciona em modo simulado

#### Executar
```bash
python serperapi_example.py
```

#### Exemplos de Uso

```python
# Exemplo 1: Planejamento com busca web
planejar_viagem_com_busca_web(
    destino="Paris",
    dias=5,
    pergunta_especifica="eventos em junho de 2024"
)

# Exemplo 2: Pesquisa de tópicos atuais
pesquisar_topicos_atuais([
    "melhores destinos 2024",
    "dicas de viagem para Paris"
])
```

---

## 🔍 Comparação das Abordagens

| Característica | CrewAI | LangChain | LangGraph |
|---------------|--------|-----------|-----------|
| **Complexidade** | Baixa | Média | Alta |
| **Controle** | Baixo | Alto | Muito Alto |
| **Multi-agente** | ✅ Nativo | ⚠️ Manual | ⚠️ Manual |
| **Fluxo Explícito** | ❌ | ❌ | ✅ |
| **Estado Compartilhado** | ⚠️ Limitado | ⚠️ Manual | ✅ Nativo |
| **Melhor Para** | Equipes simples | Agentes únicos | Processos complexos |

### Quando Usar Cada Um?

- **CrewAI**: Quando você precisa de uma equipe de agentes trabalhando juntos de forma simples
- **LangChain**: Quando você precisa de controle total e flexibilidade máxima
- **LangGraph**: Quando você tem um processo com etapas bem definidas e fluxo complexo

---

## 💡 Pontos Fortes e Limitações

### CrewAI
**Pontos Fortes:**
- Abstração de alto nível facilita prototipagem rápida
- Suporte nativo para equipes de agentes
- Menos código necessário

**Limitações:**
- Menos controle sobre o comportamento interno
- Pode ser limitante para casos muito específicos
- Menos flexível para processos não-lineares

### LangChain
**Pontos Fortes:**
- Máxima flexibilidade e controle
- Grande ecossistema de integrações
- Ideal para agentes únicos com múltiplas ferramentas

**Limitações:**
- Requer mais código e configuração
- Gerenciamento de estado manual
- Multi-agente requer mais trabalho

### LangGraph
**Pontos Fortes:**
- Fluxo de trabalho explícito e visualizável
- Gerenciamento de estado robusto
- Ideal para processos com múltiplas etapas

**Limitações:**
- Requer planejamento prévio do fluxo
- Pode ser excessivo para casos simples
- Curva de aprendizado mais íngreme

---

## 🎓 Exercícios para Prática

### Exercício 1: Adicionar Nova Ferramenta
**Objetivo**: Adicione uma nova ferramenta `buscar_hoteis()` em `tools.py` e integre-a nas três implementações.

**Dica**: Crie uma função que retorne uma lista de hotéis simulados para o destino.

---

### Exercício 2: Modificar o Fluxo (LangGraph)
**Objetivo**: No `langgraph_example.py`, adicione uma etapa condicional: se o orçamento for maior que R$ 5000, busque opções de hospedagem mais baratas.

**Dica**: Use `add_conditional_edges()` para criar ramificações no grafo.

---

### Exercício 3: Adicionar Novo Agente (CrewAI)
**Objetivo**: No `crewai_example.py`, adicione um terceiro agente "Especialista em Economia" que sugere formas de reduzir custos.

**Dica**: Crie um novo `Agent` e uma nova `Task` que use o contexto das tarefas anteriores.

---

### Exercício 4: Melhorar o Prompt (LangChain)
**Objetivo**: No `langchain_example.py`, modifique o prompt do sistema para que o agente sempre sugira 3 destinos alternativos similares.

**Dica**: Edite a mensagem do sistema no `ChatPromptTemplate`.

---

### Exercício 5: Criar Versão Híbrida
**Objetivo**: Combine LangGraph com LangChain: use LangGraph para o fluxo principal e LangChain Agents dentro de alguns nós.

**Dica**: Crie um nó que use um `AgentExecutor` do LangChain para realizar uma subtarefa complexa.

---

### Exercício 6: Adicionar Memória
**Objetivo**: Implemente memória de conversação para que o agente lembre de preferências do usuário entre execuções.

**Dica**: Use `ConversationBufferMemory` do LangChain ou salve estado em arquivo.

---

### Exercício 7: Validação de Entrada
**Objetivo**: Adicione validação para garantir que o destino existe e o número de dias é válido antes de executar o planejamento.

**Dica**: Crie uma função de validação e adicione como primeiro nó no LangGraph ou como pré-processamento nas outras abordagens.

---

## 📝 Estrutura do Projeto

```
.
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências Python
├── tools.py                  # Ferramentas simuladas compartilhadas
├── test_tools.py             # Script para testar ferramentas isoladamente
├── crewai_example.py         # Implementação com CrewAI
├── langchain_example.py      # Implementação com LangChain
├── langgraph_example.py      # Implementação com LangGraph
└── serperapi_example.py      # Exemplo com busca web real (SerperAPI)
```

---

## 🚀 Próximos Passos

1. **Experimente**: Execute cada implementação e compare os resultados
2. **Modifique**: Tente os exercícios propostos
3. **Estenda**: Adicione novas funcionalidades (ex: recomendações de restaurantes)
4. **Integre**: Conecte com APIs reais (ex: OpenWeather, Google Places)

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [Documentação CrewAI](https://docs.crewai.com/)
- [Documentação LangChain](https://python.langchain.com/)
- [Documentação LangGraph](https://langchain-ai.github.io/langgraph/)

### Documentação do Projeto
- **[README_LANGCHAIN_VS_LANGGRAPH.md](README_LANGCHAIN_VS_LANGGRAPH.md)**: Guia detalhado sobre as diferenças entre LangChain e LangGraph
- **[README_SERPERAPI.md](README_SERPERAPI.md)**: Guia completo sobre integração com SerperAPI para busca web real

---

## 🤝 Contribuindo

Sinta-se à vontade para sugerir melhorias, adicionar novos exemplos ou reportar problemas!

---

**Bons estudos e boas viagens! ✈️🌍**
