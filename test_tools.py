"""
Script simples para testar as ferramentas sem precisar de API key.
Execute este arquivo para entender como as ferramentas funcionam antes de usar os agentes.
"""

from tools import consultar_clima, buscar_atracoes, calcular_orcamento, verificar_visto


def testar_ferramentas():
    """Testa todas as ferramentas disponíveis"""
    print("=" * 60)
    print("TESTANDO FERRAMENTAS DE PLANEJAMENTO DE VIAGEM")
    print("=" * 60)
    
    destino = "Paris"
    
    print(f"\n📍 Destino: {destino}\n")
    
    # Teste 1: Consultar clima
    print("1️⃣  CONSULTANDO CLIMA")
    print("-" * 60)
    clima = consultar_clima(destino, "2024-06-15")
    print(clima)
    
    # Teste 2: Buscar atrações
    print("\n2️⃣  BUSCANDO ATRAÇÕES")
    print("-" * 60)
    atracoes = buscar_atracoes(destino)
    for i, atracao in enumerate(atracoes, 1):
        print(f"   {i}. {atracao}")
    
    # Teste 3: Verificar visto
    print("\n3️⃣  VERIFICANDO VISTO")
    print("-" * 60)
    visto = verificar_visto(destino)
    print(visto)
    
    # Teste 4: Calcular orçamento
    print("\n4️⃣  CALCULANDO ORÇAMENTO")
    print("-" * 60)
    dias = 5
    orcamento = calcular_orcamento(destino, dias, "hotel")
    print(f"   Destino: {orcamento['destino']}")
    print(f"   Dias: {orcamento['dias']}")
    print(f"   Hospedagem: R$ {orcamento['hospedagem']:.2f}")
    print(f"   Comida: R$ {orcamento['comida']:.2f}")
    print(f"   Transporte: R$ {orcamento['transporte']:.2f}")
    print(f"   TOTAL: R$ {orcamento['total']:.2f}")
    
    print("\n" + "=" * 60)
    print("✅ Todas as ferramentas funcionando corretamente!")
    print("=" * 60)


if __name__ == "__main__":
    testar_ferramentas()
