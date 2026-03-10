"""
Exemplo Conversacional de Agente de Planejamento de Viagem usando LangChain

Este exemplo demonstra como criar um agente conversacional com LangChain que:
1. Conversa naturalmente com o usuário
2. Faz perguntas para coletar informações
3. Usa tools quando necessário
4. Mantém contexto da conversa
5. Valida informações coletadas

Arquitetura:
- Agent: Agente conversacional que interage com o usuário
- Tools: Ferramentas disponíveis para o agente
- Memory: Memória de conversação para manter contexto
- AgentExecutor: Executa o agente em loop conversacional
"""

from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from tools import consultar_clima, calcular_orcamento, buscar_atracoes, verificar_visto
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# CRIANDO FERRAMENTAS (TOOLS)
# ============================================================================

ferramentas = [
    Tool(
        name="consultar_clima",
        func=lambda entrada: consultar_clima(
            entrada.split(",")[0].strip(),
            entrada.split(",")[1].strip() if "," in entrada else "2024-06-01"
        ),
        description="Consulta o clima de um destino. Entrada: 'destino, data' (formato: YYYY-MM-DD). Exemplo: 'Paris, 2024-06-15'"
    ),
    Tool(
        name="calcular_orcamento",
        func=lambda entrada: str(calcular_orcamento(
            entrada.split(",")[0].strip(),
            int(entrada.split(",")[1].strip()),
            entrada.split(",")[2].strip() if len(entrada.split(",")) > 2 else "hotel"
        )),
        description="Calcula orçamento de viagem. Entrada: 'destino, dias, tipo_hospedagem' (hotel/hostel/airbnb). Exemplo: 'Paris, 5, hotel'"
    ),
    Tool(
        name="buscar_atracoes",
        func=lambda destino: str(buscar_atracoes(destino)),
        description="Busca atrações turísticas de um destino. Entrada: nome do destino. Exemplo: 'Paris'"
    ),
    Tool(
        name="verificar_visto",
        func=lambda destino: verificar_visto(destino),
        description="Verifica necessidade de visto para um destino. Entrada: nome do destino. Exemplo: 'Paris'"
    )
]


# ============================================================================
# CONFIGURANDO MEMÓRIA DE CONVERSAÇÃO
# ============================================================================

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


# ============================================================================
# CONFIGURANDO O MODELO LLM
# ============================================================================

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)


# ============================================================================
# CRIANDO PROMPT CONVERSACIONAL
# ============================================================================

prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente de viagem muito amigável e conversacional.
    
    Sua personalidade:
    - Você é prestativo, educado e entusiasmado
    - Você faz perguntas de forma natural, como se estivesse conversando com um amigo
    - Você sempre mantém um tom positivo e encorajador
    - Você oferece sugestões quando apropriado
    
    Sua tarefa:
    - Conversar com o usuário sobre planejamento de viagem
    - Fazer perguntas para coletar informações necessárias:
      * Destino da viagem
      * Número de dias
      * Cidade de origem
      * Tipo de hospedagem preferido
      * Orçamento aproximado (opcional)
    - Usar as ferramentas disponíveis quando precisar de informações específicas
    - Criar um plano de viagem completo baseado nas informações coletadas
    
    Instruções importantes:
    - Faça uma pergunta por vez e espere a resposta
    - Seja natural e conversacional
    - Use as ferramentas quando necessário para obter informações atualizadas
    - Quando tiver todas as informações, crie um plano detalhado
    - Sempre seja amigável e prestativo"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])


# ============================================================================
# CRIANDO O AGENTE
# ============================================================================

agente = create_openai_functions_agent(
    llm=llm,
    tools=ferramentas,
    prompt=prompt
)

# Criando o executor com memória
executor = AgentExecutor(
    agent=agente,
    tools=ferramentas,
    verbose=True,
    memory=memory,
    max_iterations=5,
    handle_parsing_errors=True
)


# ============================================================================
# FUNÇÃO CONVERSACIONAL PRINCIPAL
# ============================================================================

def conversar_com_agente():
    """
    Loop conversacional onde o agente LangChain conversa com o usuário.
    """
    print("\n" + "="*70)
    print("🤖 ASSISTENTE DE VIAGEM - LANGCHAIN (MODO CONVERSACIONAL)")
    print("="*70)
    print("\nOlá! Sou seu assistente de viagem. Vamos planejar sua viagem juntos!")
    print("Posso ajudar com informações sobre clima, atrações, orçamentos e muito mais.")
    print("\nDigite 'sair' para encerrar a conversa.")
    print("Digite 'novo' para começar uma nova conversa.")
    print("-"*70 + "\n")
    
    # Mensagem inicial do agente
    mensagem_inicial = """Olá! Que prazer em conhecê-lo! 👋

Estou aqui para ajudar você a planejar a viagem dos seus sonhos. 
Vou fazer algumas perguntas para entender melhor o que você precisa.

Para começar, me diga: para onde você gostaria de viajar?"""
    
    print(f"🤖 Assistente: {mensagem_inicial}\n")
    
    # Adicionando mensagem inicial ao histórico
    memory.chat_memory.add_user_message("Olá")
    memory.chat_memory.add_ai_message(mensagem_inicial)
    
    while True:
        try:
            # Entrada do usuário
            mensagem_usuario = input("👤 Você: ").strip()
            
            if not mensagem_usuario:
                continue
            
            # Comandos especiais
            if mensagem_usuario.lower() in ['sair', 'exit', 'quit', 'tchau']:
                resposta_despedida = "Foi um prazer ajudar! Espero que tenha uma viagem incrível! ✈️🌍 Boa viagem!"
                print(f"\n🤖 Assistente: {resposta_despedida}\n")
                break
            
            if mensagem_usuario.lower() in ['novo', 'reset', 'nova conversa']:
                memory.clear()
                print("\n🔄 Nova conversa iniciada!\n")
                mensagem_inicial = "Olá! Vamos começar de novo. Para onde você gostaria de viajar?"
                print(f"🤖 Assistente: {mensagem_inicial}\n")
                memory.chat_memory.add_user_message("Nova conversa")
                memory.chat_memory.add_ai_message(mensagem_inicial)
                continue
            
            # Executando o agente
            print()  # Linha em branco para melhor visualização
            
            resultado = executor.invoke({
                "input": mensagem_usuario
            })
            
            resposta = resultado.get("output", "Desculpe, não consegui processar sua mensagem.")
            
            print(f"\n🤖 Assistente: {resposta}\n")
            print("-"*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Conversa interrompida. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            print("Por favor, tente novamente ou digite 'sair' para encerrar.\n")


# ============================================================================
# FUNÇÃO PARA CONVERSA GUIADA (COM PERGUNTAS ESPECÍFICAS)
# ============================================================================

def conversa_guiada():
    """
    Versão guiada onde o agente faz perguntas específicas em sequência.
    """
    print("\n" + "="*70)
    print("🤖 ASSISTENTE DE VIAGEM - LANGCHAIN (MODO GUIADO)")
    print("="*70)
    print("\nVou fazer algumas perguntas para planejar sua viagem.\n")
    print("-"*70 + "\n")
    
    informacoes = {}
    
    # Perguntas em sequência
    perguntas = [
        {
            'chave': 'destino',
            'pergunta': '📍 Para onde você gostaria de viajar?',
            'tipo': 'texto'
        },
        {
            'chave': 'dias',
            'pergunta': '📅 Quantos dias você pretende ficar?',
            'tipo': 'numero'
        },
        {
            'chave': 'origem',
            'pergunta': '✈️  De qual cidade você vai partir? (Enter para São Paulo)',
            'tipo': 'texto',
            'padrao': 'São Paulo'
        },
        {
            'chave': 'tipo_hospedagem',
            'pergunta': '🏨 Que tipo de hospedagem você prefere? (hotel/hostel/airbnb - Enter para hotel)',
            'tipo': 'opcao',
            'opcoes': ['hotel', 'hostel', 'airbnb'],
            'padrao': 'hotel'
        }
    ]
    
    # Fazendo perguntas
    for pergunta_info in perguntas:
        while True:
            resposta = input(f"🤖 {pergunta_info['pergunta']}\n👤 Você: ").strip()
            
            if not resposta and 'padrao' in pergunta_info:
                resposta = pergunta_info['padrao']
                print(f"   ✓ Usando: {resposta}\n")
            
            if not resposta and 'padrao' not in pergunta_info:
                print("   ⚠️  Por favor, responda à pergunta.\n")
                continue
            
            # Validando resposta
            if pergunta_info['tipo'] == 'numero':
                try:
                    valor = int(resposta)
                    if valor > 0:
                        informacoes[pergunta_info['chave']] = valor
                        print(f"   ✓ Entendido! {valor} dias.\n")
                        break
                    else:
                        print("   ⚠️  Por favor, digite um número válido (maior que 0).\n")
                except:
                    print("   ⚠️  Por favor, digite um número válido.\n")
            
            elif pergunta_info['tipo'] == 'opcao':
                resposta_lower = resposta.lower()
                if resposta_lower in pergunta_info['opcoes']:
                    informacoes[pergunta_info['chave']] = resposta_lower
                    print(f"   ✓ Ótima escolha! {resposta_lower}.\n")
                    break
                else:
                    print(f"   ⚠️  Por favor, escolha uma das opções: {', '.join(pergunta_info['opcoes'])}\n")
            
            else:  # texto
                informacoes[pergunta_info['chave']] = resposta
                print(f"   ✓ Perfeito! {resposta}.\n")
                break
    
    # Resumo
    print("="*70)
    print("📋 INFORMAÇÕES COLETADAS")
    print("="*70)
    for chave, valor in informacoes.items():
        print(f"  {chave.replace('_', ' ').title()}: {valor}")
    print("="*70 + "\n")
    
    # Criando plano com o agente
    print("🔍 Criando seu plano de viagem...\n")
    
    instrucao = f"""Com base nas informações coletadas, crie um plano de viagem completo:

Destino: {informacoes.get('destino')}
Duração: {informacoes.get('dias')} dias
Origem: {informacoes.get('origem', 'São Paulo')}
Tipo de hospedagem: {informacoes.get('tipo_hospedagem', 'hotel')}

Siga estes passos:
1. Use consultar_clima para obter informações sobre o clima
2. Use buscar_atracoes para encontrar as principais atrações
3. Use verificar_visto para verificar requisitos de visto
4. Use calcular_orcamento para calcular o orçamento
5. Crie um plano detalhado e organizado com todas as informações"""
    
    resultado = executor.invoke({"input": instrucao})
    
    print("\n" + "="*70)
    print("🎉 SEU PLANO DE VIAGEM ESTÁ PRONTO!")
    print("="*70)
    print(resultado["output"])
    print("="*70 + "\n")


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def menu_principal():
    """Menu para escolher o modo de conversa."""
    print("\n" + "="*70)
    print("🤖 ASSISTENTE DE VIAGEM - LANGCHAIN")
    print("="*70)
    print("\nEscolha o modo de conversa:")
    print("1. Conversa Livre (agente faz perguntas naturalmente)")
    print("2. Conversa Guiada (perguntas em sequência)")
    print("3. Sair")
    print("-"*70)
    
    escolha = input("\nEscolha uma opção (1-3): ").strip()
    
    if escolha == "1":
        conversar_com_agente()
    elif escolha == "2":
        conversa_guiada()
    elif escolha == "3":
        print("\n👋 Até logo!")
    else:
        print("\n⚠️  Opção inválida. Tente novamente.")
        menu_principal()


if __name__ == "__main__":
    # Executando menu principal
    menu_principal()
    
    # Ou executar diretamente um dos modos:
    # conversar_com_agente()  # Modo conversacional livre
    # conversa_guiada()        # Modo guiado com perguntas específicas
