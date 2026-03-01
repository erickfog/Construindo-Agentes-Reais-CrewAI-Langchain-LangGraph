"""
Exemplo de Agente de Planejamento de Viagem usando LangChain

LangChain oferece uma abordagem mais flexível e granular para construir agentes.
Você tem controle total sobre cada etapa do processo.

Arquitetura:
- Tools: Ferramentas que o agente pode usar
- Agent: Define o comportamento do agente
- AgentExecutor: Executa o agente em loop até completar a tarefa
"""

from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import consultar_clima, calcular_orcamento, buscar_atracoes, verificar_visto
import os
from dotenv import load_dotenv

load_dotenv()

# Criando as ferramentas (Tools)
ferramentas = [
    Tool(
        name="consultar_clima",
        func=lambda destino_data: consultar_clima(
            destino_data.split(",")[0].strip(),
            destino_data.split(",")[1].strip() if "," in destino_data else "2024-06-01"
        ),
        description="Consulta o clima de um destino. Entrada: 'destino, data' (formato: YYYY-MM-DD)"
    ),
    Tool(
        name="calcular_orcamento",
        func=lambda entrada: str(calcular_orcamento(
            entrada.split(",")[0].strip(),
            int(entrada.split(",")[1].strip()),
            entrada.split(",")[2].strip() if len(entrada.split(",")) > 2 else "hotel"
        )),
        description="Calcula orçamento de viagem. Entrada: 'destino, dias, tipo_hospedagem' (hotel/hostel/airbnb)"
    ),
    Tool(
        name="buscar_atracoes",
        func=lambda destino: str(buscar_atracoes(destino)),
        description="Busca atrações turísticas de um destino. Entrada: nome do destino"
    ),
    Tool(
        name="verificar_visto",
        func=lambda destino: verificar_visto(destino),
        description="Verifica necessidade de visto. Entrada: nome do destino"
    )
]

# Configurando o modelo LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Criando o prompt do agente
prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente especializado em planejamento de viagens.
    Sua tarefa é ajudar a planejar viagens completas, coletando informações e criando planos detalhados.
    
    Use as ferramentas disponíveis para:
    1. Consultar clima do destino
    2. Buscar atrações turísticas
    3. Verificar requisitos de visto
    4. Calcular orçamento
    
    Sempre forneça respostas completas e organizadas."""),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Criando o agente
agente = create_openai_functions_agent(
    llm=llm,
    tools=ferramentas,
    prompt=prompt
)

# Criando o executor do agente
executor = AgentExecutor(
    agent=agente,
    tools=ferramentas,
    verbose=True,
    max_iterations=5
)


def planejar_viagem_langchain(destino: str, dias: int):
    """
    Função principal para planejar uma viagem usando LangChain.
    
    Args:
        destino: Nome do destino
        dias: Número de dias da viagem
    """
    print(f"\n{'='*60}")
    print(f"PLANEJANDO VIAGEM COM LANGCHAIN")
    print(f"{'='*60}\n")
    
    # Criando a instrução para o agente
    instrucao = f"""Planeje uma viagem completa para {destino} com duração de {dias} dias.
    
    Siga estes passos:
    1. Consulte o clima para {destino}
    2. Busque as principais atrações turísticas
    3. Verifique se é necessário visto
    4. Calcule o orçamento estimado para {dias} dias
    5. Crie um resumo final com todas as informações organizadas"""
    
    # Executando o agente
    resultado = executor.invoke({"input": instrucao})
    
    print(f"\n{'='*60}")
    print("RESULTADO FINAL:")
    print(f"{'='*60}")
    print(resultado["output"])
    
    return resultado


if __name__ == "__main__":
    # Exemplo de uso
    planejar_viagem_langchain("Paris", 5)
