"""
Exemplo de Agente de Pesquisa usando SerperAPI (Busca Real na Web)

Este exemplo demonstra como integrar uma API real (SerperAPI) com agentes LangChain
para realizar buscas na web e obter informações atualizadas.

SerperAPI é uma API de busca do Google que permite:
- Buscar informações na web
- Obter resultados em tempo real
- Acessar informações atualizadas

Arquitetura:
- Tool: Integração com SerperAPI
- Agent: Agente LangChain que usa a ferramenta de busca
- AgentExecutor: Executa o agente com capacidade de busca web
"""

from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from dotenv import load_dotenv

load_dotenv()

# Verificando se a API key está configurada
if not os.getenv("SERPER_API_KEY"):
    print("⚠️  AVISO: SERPER_API_KEY não encontrada no arquivo .env")
    print("   Para usar este exemplo, você precisa:")
    print("   1. Criar uma conta em https://serper.dev")
    print("   2. Obter sua API key")
    print("   3. Adicionar SERPER_API_KEY=sua_chave no arquivo .env")
    print("\n   Por enquanto, o exemplo usará uma função simulada.\n")


def buscar_web_simulada(query: str) -> str:
    """
    Função simulada de busca web (usada quando SerperAPI não está configurada).
    
    Args:
        query: Termo de busca
        
    Returns:
        String com resultados simulados
    """
    resultados_simulados = {
        "paris": "Paris é a capital da França, conhecida como Cidade Luz. Principais atrações: Torre Eiffel, Museu do Louvre, Arco do Triunfo. Clima temperado, melhor época: primavera e verão.",
        "tokyo": "Tóquio é a capital do Japão, uma metrópole moderna e tradicional. Principais atrações: Templo Senso-ji, Torre de Tóquio, Palácio Imperial. Clima subtropical úmido.",
        "rio de janeiro": "Rio de Janeiro é uma cidade brasileira famosa por suas praias e paisagens. Principais atrações: Cristo Redentor, Pão de Açúcar, Copacabana. Clima tropical.",
    }
    
    query_lower = query.lower()
    for key, value in resultados_simulados.items():
        if key in query_lower:
            return value
    
    return f"Resultados de busca para '{query}': Informações gerais sobre o tópico. Para resultados reais, configure a SerperAPI."


# Criando a ferramenta de busca web
def criar_ferramenta_busca():
    """Cria a ferramenta de busca web usando SerperAPI ou simulação"""
    
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if serper_api_key:
        # Usando SerperAPI real
        search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
        
        ferramenta_busca = Tool(
            name="buscar_na_web",
            func=search.run,
            description="""Busca informações atualizadas na web usando Google Search.
            Use esta ferramenta para:
            - Pesquisar informações sobre destinos turísticos
            - Buscar notícias e informações atualizadas
            - Encontrar dados que não estão nas ferramentas simuladas
            Entrada: termo de busca (ex: 'clima em Paris hoje', 'atrações em Tokyo')
            """
        )
        print("✅ Usando SerperAPI real para buscas na web\n")
    else:
        # Usando função simulada
        ferramenta_busca = Tool(
            name="buscar_na_web",
            func=buscar_web_simulada,
            description="""Busca informações na web (modo simulado).
            Para usar busca real, configure SERPER_API_KEY no arquivo .env
            Entrada: termo de busca
            """
        )
        print("⚠️  Usando busca simulada (configure SERPER_API_KEY para busca real)\n")
    
    return ferramenta_busca


# Criando ferramentas adicionais (das ferramentas simuladas)
from tools import calcular_orcamento, buscar_atracoes

ferramenta_orcamento = Tool(
    name="calcular_orcamento",
    func=lambda entrada: str(calcular_orcamento(
        entrada.split(",")[0].strip(),
        int(entrada.split(",")[1].strip()),
        entrada.split(",")[2].strip() if len(entrada.split(",")) > 2 else "hotel"
    )),
    description="Calcula orçamento de viagem. Entrada: 'destino, dias, tipo_hospedagem' (hotel/hostel/airbnb)"
)

ferramenta_atracoes = Tool(
    name="buscar_atracoes",
    func=lambda destino: str(buscar_atracoes(destino)),
    description="Busca atrações turísticas de um destino. Entrada: nome do destino"
)

# Configurando o modelo LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Criando o prompt do agente
prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente especializado em planejamento de viagens com acesso à internet.
    Sua tarefa é ajudar a planejar viagens usando informações atualizadas da web.
    
    Você tem acesso a:
    1. Busca na web (SerperAPI) - para informações atualizadas e em tempo real
    2. Cálculo de orçamento - para estimar custos
    3. Busca de atrações - para encontrar pontos turísticos
    
    Sempre priorize informações atualizadas da web quando disponível.
    Combine informações da web com cálculos de orçamento para criar planos completos."""),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])


def planejar_viagem_com_busca_web(destino: str, dias: int, pergunta_especifica: str = None):
    """
    Função principal para planejar uma viagem usando busca web real.
    
    Args:
        destino: Nome do destino
        dias: Número de dias da viagem
        pergunta_especifica: Pergunta específica sobre o destino (opcional)
    """
    print(f"\n{'='*60}")
    print(f"PLANEJANDO VIAGEM COM BUSCA WEB (SERPERAPI)")
    print(f"{'='*60}\n")
    
    # Criando ferramentas
    ferramenta_busca = criar_ferramenta_busca()
    ferramentas = [ferramenta_busca, ferramenta_orcamento, ferramenta_atracoes]
    
    # Criando o agente
    agente = create_openai_functions_agent(
        llm=llm,
        tools=ferramentas,
        prompt=prompt
    )
    
    # Criando o executor
    executor = AgentExecutor(
        agent=agente,
        tools=ferramentas,
        verbose=True,
        max_iterations=5
    )
    
    # Criando a instrução
    if pergunta_especifica:
        instrucao = f"""Planeje uma viagem para {destino} com {dias} dias.
        
        Pergunta específica: {pergunta_especifica}
        
        Siga estes passos:
        1. Busque informações atualizadas na web sobre {destino}, especialmente sobre: {pergunta_especifica}
        2. Busque as principais atrações turísticas
        3. Calcule o orçamento estimado para {dias} dias
        4. Crie um resumo final com todas as informações organizadas, incluindo as informações atualizadas da web"""
    else:
        instrucao = f"""Planeje uma viagem completa para {destino} com duração de {dias} dias.
        
        Siga estes passos:
        1. Busque informações atualizadas na web sobre {destino} (clima atual, eventos, notícias)
        2. Busque as principais atrações turísticas
        3. Calcule o orçamento estimado para {dias} dias
        4. Crie um resumo final com todas as informações organizadas"""
    
    # Executando o agente
    resultado = executor.invoke({"input": instrucao})
    
    print(f"\n{'='*60}")
    print("RESULTADO FINAL:")
    print(f"{'='*60}")
    print(resultado["output"])
    
    return resultado


def pesquisar_topicos_atuais(topicos: list):
    """
    Função para pesquisar tópicos atuais usando busca web.
    
    Args:
        topicos: Lista de tópicos para pesquisar
    """
    print(f"\n{'='*60}")
    print(f"PESQUISANDO TÓPICOS ATUAIS COM SERPERAPI")
    print(f"{'='*60}\n")
    
    # Criando ferramentas
    ferramenta_busca = criar_ferramenta_busca()
    ferramentas = [ferramenta_busca]
    
    # Criando o agente
    agente = create_openai_functions_agent(
        llm=llm,
        tools=ferramentas,
        prompt=ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente de pesquisa. Use a busca web para encontrar informações atualizadas."),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
    )
    
    executor = AgentExecutor(
        agent=agente,
        tools=ferramentas,
        verbose=True,
        max_iterations=3
    )
    
    topicos_str = ", ".join(topicos)
    instrucao = f"Pesquise informações atualizadas sobre: {topicos_str}. Forneça um resumo de cada tópico."
    
    resultado = executor.invoke({"input": instrucao})
    
    print(f"\n{'='*60}")
    print("RESULTADO DA PESQUISA:")
    print(f"{'='*60}")
    print(resultado["output"])
    
    return resultado


if __name__ == "__main__":
    # Exemplo 1: Planejamento de viagem com busca web
    print("=" * 60)
    print("EXEMPLO 1: Planejamento de Viagem com Busca Web")
    print("=" * 60)
    planejar_viagem_com_busca_web(
        destino="Paris",
        dias=5,
        pergunta_especifica="eventos e festivais em junho de 2024"
    )
    
    print("\n\n")
    
    # Exemplo 2: Pesquisa de tópicos atuais
    print("=" * 60)
    print("EXEMPLO 2: Pesquisa de Tópicos Atuais")
    print("=" * 60)
    pesquisar_topicos_atuais([
        "melhores destinos para viajar em 2024",
        "dicas de viagem para Paris"
    ])
