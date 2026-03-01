"""
Exemplo de Agente de Planejamento de Viagem usando CrewAI

CrewAI é um framework que facilita a criação de equipes de agentes especializados.
Cada agente tem um papel específico e trabalha em conjunto para resolver tarefas complexas.

Arquitetura:
- Agent: Define o papel e especialidade do agente
- Task: Define o que o agente precisa fazer
- Crew: Orquestra os agentes e tarefas
"""

from crewai import Agent, Task, Crew
from tools import consultar_clima, calcular_orcamento, buscar_atracoes, verificar_visto


# Criando agentes especializados
agente_pesquisador = Agent(
    role='Pesquisador de Destinos',
    goal='Coletar informações sobre clima, atrações e requisitos de visto',
    backstory='Você é um especialista em pesquisa de destinos turísticos.',
    verbose=True,
    allow_delegation=False
)

agente_planejador = Agent(
    role='Planejador de Viagem',
    goal='Criar um plano de viagem completo com orçamento e roteiro',
    backstory='Você é um planejador experiente que cria roteiros detalhados.',
    verbose=True,
    allow_delegation=False
)

# Criando tarefas
tarefa_pesquisa = Task(
    description='''Pesquise informações sobre o destino {destino}:
    1. Consulte o clima usando a função consultar_clima
    2. Busque atrações turísticas usando buscar_atracoes
    3. Verifique requisitos de visto usando verificar_visto
    4. Compile todas as informações em um relatório''',
    agent=agente_pesquisador,
    expected_output='Relatório com clima, atrações e requisitos de visto'
)

tarefa_planejamento = Task(
    description='''Com base nas informações coletadas, crie um plano de viagem:
    1. Calcule o orçamento usando calcular_orcamento para {dias} dias
    2. Organize as atrações em um roteiro diário
    3. Inclua recomendações de hospedagem
    4. Crie um resumo final do plano''',
    agent=agente_planejador,
    expected_output='Plano de viagem completo com orçamento e roteiro detalhado',
    context=[tarefa_pesquisa]
)

# Criando a equipe (Crew)
equipe = Crew(
    agents=[agente_pesquisador, agente_planejador],
    tasks=[tarefa_pesquisa, tarefa_planejamento],
    verbose=True
)


def planejar_viagem_crewai(destino: str, dias: int):
    """
    Função principal para planejar uma viagem usando CrewAI.
    
    Args:
        destino: Nome do destino
        dias: Número de dias da viagem
    """
    print(f"\n{'='*60}")
    print(f"PLANEJANDO VIAGEM COM CREWAI")
    print(f"{'='*60}\n")
    
    # Executando a equipe
    resultado = equipe.kickoff(inputs={
        'destino': destino,
        'dias': dias
    })
    
    print(f"\n{'='*60}")
    print("RESULTADO FINAL:")
    print(f"{'='*60}")
    print(resultado)
    
    return resultado


if __name__ == "__main__":
    # Exemplo de uso
    planejar_viagem_crewai("Paris", 5)
