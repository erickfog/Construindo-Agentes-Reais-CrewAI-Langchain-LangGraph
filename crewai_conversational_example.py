"""
Exemplo Conversacional de Agente de Planejamento de Viagem usando CrewAI

Este exemplo demonstra como criar um agente conversacional que:
1. Faz perguntas ao usuário para coletar informações
2. Mantém uma conversa natural
3. Coleta todas as informações necessárias
4. Executa o planejamento com base nas respostas

Arquitetura:
- Agent Conversacional: Faz perguntas e coleta informações
- Agent Pesquisador: Pesquisa informações sobre o destino
- Agent Planejador: Cria o plano final
"""

from crewai import Agent, Task, Crew
from crewai.tools import tool
from tools import consultar_clima, calcular_orcamento, buscar_atracoes, verificar_visto


# ============================================================================
# CUSTOM TOOLS
# ============================================================================

@tool('buscar_recomendacoes_hospedagem')
def buscar_recomendacoes_hospedagem(destino: str, tipo: str = "hotel") -> str:
    """Busca recomendações de hospedagem para um destino."""
    recomendacoes = {
        "paris": {
            "hotel": "Hotel Le Meurice (5 estrelas), Hotel Ritz Paris (luxo), Hotel des Invalides (3 estrelas)",
            "hostel": "Generator Paris, St Christopher's Inn, Les Piaules",
            "airbnb": "Apartamentos no Marais, Studios em Montmartre, Lofts em Le Marais"
        },
        "tokyo": {
            "hotel": "The Ritz-Carlton Tokyo, Park Hyatt Tokyo, Hotel Gracery Shinjuku",
            "hostel": "Khaosan Tokyo, Book and Bed Tokyo, Nui. Hostel & Bar Lounge",
            "airbnb": "Apartamentos em Shibuya, Studios em Shinjuku, Casas tradicionais em Asakusa"
        },
        "rio de janeiro": {
            "hotel": "Copacabana Palace, Belmond Hotel das Cataratas, Hotel Fasano Rio",
            "hostel": "Mango Tree Hostel, Che Lagarto Copacabana, Books Hostel",
            "airbnb": "Apartamentos em Copacabana, Studios em Ipanema, Casas em Santa Teresa"
        }
    }
    
    destino_lower = destino.lower()
    tipo_lower = tipo.lower()
    
    if destino_lower in recomendacoes and tipo_lower in recomendacoes[destino_lower]:
        return f"Recomendações de {tipo} em {destino}:\n{recomendacoes[destino_lower][tipo_lower]}"
    else:
        return f"Recomendações gerais de {tipo} em {destino}: Consulte sites de reserva como Booking.com ou Airbnb."


@tool('calcular_tempo_viagem')
def calcular_tempo_viagem(origem: str, destino: str, meio_transporte: str = "aviao") -> str:
    """Calcula tempo estimado de viagem entre dois destinos."""
    tempos_aviao = {
        ("sao paulo", "paris"): "11h 30min",
        ("sao paulo", "tokyo"): "24h 30min",
        ("sao paulo", "nova york"): "10h 15min",
        ("rio de janeiro", "paris"): "11h 45min",
        ("rio de janeiro", "londres"): "11h 20min",
    }
    
    origem_lower = origem.lower()
    destino_lower = destino.lower()
    
    if meio_transporte.lower() == "aviao":
        chave = (origem_lower, destino_lower)
        if chave in tempos_aviao:
            return f"Tempo de viagem de {origem} para {destino} de avião: {tempos_aviao[chave]}"
        else:
            return f"Tempo estimado de avião de {origem} para {destino}: Consulte companhias aéreas para horários exatos."
    elif meio_transporte.lower() == "carro":
        return f"Tempo estimado de carro: Depende da distância. Use Google Maps para cálculo preciso."
    else:
        return f"Tempo estimado de {meio_transporte}: Consulte horários oficiais."


# ============================================================================
# AGENTE CONVERSACIONAL
# ============================================================================

agente_conversacional = Agent(
    role='Assistente de Viagem Conversacional',
    goal='Fazer perguntas ao usuário de forma natural e amigável para coletar informações sobre a viagem',
    backstory='''Você é um assistente de viagem muito amigável e conversacional. 
    Você gosta de fazer perguntas de forma natural, como se estivesse conversando com um amigo.
    Você sempre é educado, paciente e ajuda o usuário a pensar sobre sua viagem.
    Faça uma pergunta por vez e espere a resposta antes de fazer a próxima.
    Se o usuário não souber algo, ofereça sugestões ou pule para a próxima pergunta.''',
    verbose=True,
    allow_delegation=False
)


# ============================================================================
# AGENTES DE PROCESSAMENTO
# ============================================================================

agente_pesquisador = Agent(
    role='Pesquisador de Destinos',
    goal='Coletar informações sobre clima, atrações e requisitos de visto',
    backstory='Você é um especialista em pesquisa de destinos turísticos.',
    verbose=True,
    allow_delegation=False,
    tools=[calcular_tempo_viagem]
)

agente_planejador = Agent(
    role='Planejador de Viagem',
    goal='Criar um plano de viagem completo com orçamento e roteiro',
    backstory='Você é um planejador experiente que cria roteiros detalhados.',
    verbose=True,
    allow_delegation=False,
    tools=[buscar_recomendacoes_hospedagem]
)


# ============================================================================
# FUNÇÃO CONVERSACIONAL
# ============================================================================

def coletar_informacoes_conversacional():
    """
    Coleta informações do usuário através de uma conversa natural.
    O agente faz perguntas e o usuário responde.
    """
    print("\n" + "="*60)
    print("🤖 ASSISTENTE DE VIAGEM - MODO CONVERSACIONAL")
    print("="*60)
    print("\nOlá! Sou seu assistente de viagem. Vou fazer algumas perguntas")
    print("para entender melhor o que você precisa. Vamos começar?\n")
    print("-"*60 + "\n")
    
    # Informações que precisamos coletar
    informacoes = {
        'destino': None,
        'dias': None,
        'origem': None,
        'tipo_hospedagem': None,
        'orcamento_aproximado': None
    }
    
    # Criando tarefa conversacional
    tarefa_conversacao = Task(
        description='''Você precisa coletar as seguintes informações do usuário através de uma conversa natural:
        1. Destino da viagem (ex: Paris, Tokyo, Rio de Janeiro)
        2. Número de dias da viagem
        3. Cidade de origem (para calcular tempo de viagem)
        4. Tipo de hospedagem preferido (hotel, hostel, airbnb)
        5. Orçamento aproximado (opcional)
        
        Faça perguntas de forma natural, uma por vez.
        Seja amigável e ofereça sugestões quando apropriado.
        Quando tiver todas as informações, resuma o que coletou.''',
        agent=agente_conversacional,
        expected_output='Resumo com todas as informações coletadas: destino, dias, origem, tipo_hospedagem, orçamento'
    )
    
    # Criando crew conversacional
    crew_conversacao = Crew(
        agents=[agente_conversacional],
        tasks=[tarefa_conversacao],
        verbose=True
    )
    
    # Loop de conversação
    contexto_conversacao = ""
    perguntas_feitas = 0
    max_perguntas = 10  # Limite de segurança
    
    print("💬 Iniciando conversa...\n")
    
    while perguntas_feitas < max_perguntas:
        # Preparando o contexto da conversa
        prompt = f"""Você está conversando com um usuário sobre planejamento de viagem.
        
Contexto da conversa até agora:
{contexto_conversacao}

Informações já coletadas:
- Destino: {informacoes['destino'] or 'Ainda não informado'}
- Dias: {informacoes['dias'] or 'Ainda não informado'}
- Origem: {informacoes['origem'] or 'Ainda não informado'}
- Tipo de hospedagem: {informacoes['tipo_hospedagem'] or 'Ainda não informado'}
- Orçamento: {informacoes['orcamento_aproximado'] or 'Ainda não informado'}

Faça uma pergunta natural e amigável para coletar uma informação que ainda falta.
Se já tiver todas as informações essenciais (destino, dias, origem), faça uma pergunta opcional ou resuma o que coletou.
"""
        
        try:
            resultado = crew_conversacao.kickoff(inputs={
                'contexto': contexto_conversacao,
                'informacoes_coletadas': str(informacoes)
            })
            
            resposta_agente = str(resultado)
            print(f"🤖 Assistente: {resposta_agente}\n")
            
            # Verificando se o agente está resumindo (sinal de que terminou)
            if "resumo" in resposta_agente.lower() or "coletadas" in resposta_agente.lower():
                # Tentar extrair informações do resumo
                break
            
            # Coletando resposta do usuário
            resposta_usuario = input("👤 Você: ").strip()
            
            if not resposta_usuario:
                print("⚠️  Por favor, responda à pergunta.\n")
                continue
            
            # Atualizando contexto
            contexto_conversacao += f"\nAssistente: {resposta_agente}\nUsuário: {resposta_usuario}\n"
            
            # Tentando extrair informações da resposta
            resposta_lower = resposta_usuario.lower()
            
            # Extrair destino
            if not informacoes['destino']:
                destinos = ['paris', 'tokyo', 'rio de janeiro', 'nova york', 'londres', 'rio']
                for destino in destinos:
                    if destino in resposta_lower:
                        informacoes['destino'] = destino.title()
                        break
            
            # Extrair número de dias
            if not informacoes['dias']:
                palavras = resposta_usuario.split()
                for palavra in palavras:
                    if palavra.isdigit():
                        num = int(palavra)
                        if 1 <= num <= 30:
                            informacoes['dias'] = num
                            break
            
            # Extrair origem
            if not informacoes['origem']:
                origens = ['são paulo', 'sao paulo', 'rio de janeiro', 'rio', 'brasília', 'brasilia']
                for origem in origens:
                    if origem in resposta_lower:
                        informacoes['origem'] = origem.title()
                        break
            
            # Extrair tipo de hospedagem
            if not informacoes['tipo_hospedagem']:
                if 'hotel' in resposta_lower:
                    informacoes['tipo_hospedagem'] = 'hotel'
                elif 'hostel' in resposta_lower:
                    informacoes['tipo_hospedagem'] = 'hostel'
                elif 'airbnb' in resposta_lower:
                    informacoes['tipo_hospedagem'] = 'airbnb'
            
            perguntas_feitas += 1
            
            # Verificando se temos informações suficientes
            if informacoes['destino'] and informacoes['dias'] and informacoes['origem']:
                print("\n✅ Informações essenciais coletadas! Vou criar seu plano de viagem...\n")
                break
                
        except Exception as e:
            print(f"❌ Erro na conversa: {e}")
            break
    
    # Preenchendo valores padrão se necessário
    if not informacoes['origem']:
        informacoes['origem'] = 'São Paulo'
    if not informacoes['tipo_hospedagem']:
        informacoes['tipo_hospedagem'] = 'hotel'
    
    return informacoes


def planejar_viagem_conversacional():
    """
    Função principal que combina conversação com planejamento.
    """
    # Passo 1: Coletar informações através de conversa
    informacoes = coletar_informacoes_conversacional()
    
    if not informacoes['destino'] or not informacoes['dias']:
        print("❌ Não foi possível coletar informações suficientes.")
        return None
    
    print("\n" + "="*60)
    print("📋 INFORMAÇÕES COLETADAS")
    print("="*60)
    for chave, valor in informacoes.items():
        print(f"  {chave.replace('_', ' ').title()}: {valor or 'Não informado'}")
    print("="*60 + "\n")
    
    # Passo 2: Executar planejamento
    print("🔍 Pesquisando informações sobre o destino...\n")
    
    # Criando tarefas de pesquisa e planejamento
    tarefa_pesquisa = Task(
        description=f'''Pesquise informações sobre {informacoes['destino']}:
        1. Use calcular_tempo_viagem para descobrir o tempo de viagem de {informacoes['origem']} para {informacoes['destino']}
        2. Consulte o clima
        3. Busque atrações turísticas
        4. Verifique requisitos de visto
        5. Compile todas as informações em um relatório''',
        agent=agente_pesquisador,
        expected_output='Relatório com tempo de viagem, clima, atrações e requisitos de visto'
    )
    
    tarefa_planejamento = Task(
        description=f'''Com base nas informações coletadas, crie um plano de viagem:
        1. Calcule o orçamento para {informacoes['dias']} dias
        2. Use buscar_recomendacoes_hospedagem para encontrar opções de {informacoes['tipo_hospedagem']}
        3. Organize as atrações em um roteiro diário
        4. Inclua as recomendações de hospedagem
        5. Crie um resumo final personalizado com todas as informações''',
        agent=agente_planejador,
        expected_output='Plano de viagem completo e personalizado',
        context=[tarefa_pesquisa]
    )
    
    # Criando crew de planejamento
    crew_planejamento = Crew(
        agents=[agente_pesquisador, agente_planejador],
        tasks=[tarefa_pesquisa, tarefa_planejamento],
        verbose=True
    )
    
    # Executando planejamento
    print("✈️  Criando seu plano de viagem...\n")
    resultado = crew_planejamento.kickoff(inputs={
        'destino': informacoes['destino'],
        'dias': informacoes['dias'],
        'origem': informacoes['origem'],
        'tipo_hospedagem': informacoes['tipo_hospedagem']
    })
    
    print("\n" + "="*60)
    print("🎉 SEU PLANO DE VIAGEM ESTÁ PRONTO!")
    print("="*60)
    print(resultado)
    print("="*60 + "\n")
    
    return resultado


def conversa_interativa():
    """
    Versão interativa onde o agente faz perguntas e o usuário responde.
    Mais natural e conversacional.
    """
    print("\n" + "="*60)
    print("🤖 ASSISTENTE DE VIAGEM - MODO CONVERSACIONAL")
    print("="*60)
    print("\nOlá! Sou seu assistente de viagem. Vou fazer algumas perguntas")
    print("para entender melhor o que você precisa. Vamos começar?\n")
    print("-"*60 + "\n")
    
    informacoes = {}
    historico = []
    
    # Perguntas que o agente deve fazer
    perguntas = [
        {
            'chave': 'destino',
            'pergunta': '📍 Para onde você gostaria de viajar? (ex: Paris, Tokyo, Rio de Janeiro)',
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
    
    # Fazendo perguntas de forma conversacional
    for i, pergunta_info in enumerate(perguntas, 1):
        while True:
            resposta = input(f"🤖 {pergunta_info['pergunta']}\n👤 Você: ").strip()
            
            if not resposta and 'padrao' in pergunta_info:
                resposta = pergunta_info['padrao']
                print(f"   ✓ Usando: {resposta}")
            
            if not resposta and 'padrao' not in pergunta_info:
                print("   ⚠️  Por favor, responda à pergunta.\n")
                continue
            
            # Validando resposta
            if pergunta_info['tipo'] == 'numero':
                try:
                    valor = int(resposta)
                    if valor > 0:
                        informacoes[pergunta_info['chave']] = valor
                        historico.append(f"Pergunta {i}: {pergunta_info['pergunta']} → Resposta: {valor}")
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
                    historico.append(f"Pergunta {i}: {pergunta_info['pergunta']} → Resposta: {resposta_lower}")
                    print(f"   ✓ Ótima escolha! {resposta_lower}.\n")
                    break
                else:
                    print(f"   ⚠️  Por favor, escolha uma das opções: {', '.join(pergunta_info['opcoes'])}\n")
            
            else:  # texto
                informacoes[pergunta_info['chave']] = resposta
                historico.append(f"Pergunta {i}: {pergunta_info['pergunta']} → Resposta: {resposta}")
                print(f"   ✓ Perfeito! {resposta}.\n")
                break
    
    # Resumo
    print("\n" + "="*60)
    print("📋 RESUMO DAS INFORMAÇÕES COLETADAS")
    print("="*60)
    print(f"  🎯 Destino: {informacoes.get('destino', 'N/A')}")
    print(f"  📅 Duração: {informacoes.get('dias', 'N/A')} dias")
    print(f"  ✈️  Origem: {informacoes.get('origem', 'N/A')}")
    print(f"  🏨 Hospedagem: {informacoes.get('tipo_hospedagem', 'N/A')}")
    print("="*60 + "\n")
    
    return informacoes


if __name__ == "__main__":
    # Coletando informações através de conversa interativa
    informacoes = conversa_interativa()
    
    if not informacoes.get('destino') or not informacoes.get('dias'):
        print("❌ Não foi possível coletar informações suficientes.")
        exit(1)
    
    print("✅ Perfeito! Vou criar seu plano de viagem agora...\n")
    
    # Executando planejamento
    destino = informacoes.get('destino')
    dias = informacoes.get('dias')
    origem = informacoes.get('origem', 'São Paulo')
    tipo_hosp = informacoes.get('tipo_hospedagem', 'hotel')
    
    tarefa_pesquisa = Task(
        description=f'''Pesquise informações sobre {destino}:
        1. Use calcular_tempo_viagem para descobrir o tempo de viagem de {origem} para {destino}
        2. Consulte o clima
        3. Busque atrações turísticas
        4. Verifique requisitos de visto
        5. Compile todas as informações em um relatório''',
        agent=agente_pesquisador,
        expected_output='Relatório com tempo de viagem, clima, atrações e requisitos de visto'
    )
    
    tarefa_planejamento = Task(
        description=f'''Com base nas informações coletadas, crie um plano de viagem:
        1. Calcule o orçamento para {dias} dias
        2. Use buscar_recomendacoes_hospedagem para encontrar opções de {tipo_hosp}
        3. Organize as atrações em um roteiro diário
        4. Inclua as recomendações de hospedagem
        5. Crie um resumo final personalizado e amigável''',
        agent=agente_planejador,
        expected_output='Plano de viagem completo e personalizado',
        context=[tarefa_pesquisa]
    )
    
    crew_planejamento = Crew(
        agents=[agente_pesquisador, agente_planejador],
        tasks=[tarefa_pesquisa, tarefa_planejamento],
        verbose=True
    )
    
    print("🔍 Pesquisando e criando seu plano...\n")
    resultado = crew_planejamento.kickoff(inputs={
        'destino': destino,
        'dias': dias,
        'origem': origem,
        'tipo_hospedagem': tipo_hosp
    })
    
    print("\n" + "="*60)
    print("🎉 SEU PLANO DE VIAGEM ESTÁ PRONTO!")
    print("="*60)
    print(resultado)
    print("="*60 + "\n")
