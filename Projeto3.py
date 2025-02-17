import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Patch

# -------------------------------------------------------------------------------------------------------------------------
# Implementação do Projeto 3 da matéria de Teoria e Aplicação de Grafos - UnB
# 
# Implementação baseada no algoritmo clássico de Algoritmo Guloso para Coloração de Arestas
# Referências: https://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/
# -------------------------------------------------------------------------------------------------------------------------


# Todos os times do campeonato em siglas, respectivamente: Dragões FC., Tubarões FC., Águias FC., Leões FC., Falcões FC., Orcas FC., Crocodilos FC.
times = ["DFC", "TFC", "AFC", "LFC", "FFC", "OFC", "CFC"]

# Restrições de rodadas
# Legenda: Mandante A vs Visitante B não podem em X e Y rodada
restricoesRodadas = {
    ("DFC", "CFC"): [1, 14],  
    ("LFC", "FFC"): [7, 13],   
    ("OFC", "LFC"): [10, 11],  
    ("AFC", "FFC"): [12, 13],  
    ("CFC", "TFC"): [2, 3],    
}

# Restrições de Mandante: O time A Mandante não pode estar na mesma rodada que o time B mandante, e vice versa
restricaoMandante = {
    "TFC": ["OFC"],  
    "OFC": ["TFC"],  
    "AFC": ["FFC"],  
    "FFC": ["AFC"],  
}

# Função que plota o gráfico com a coloração do grafo
def plotaGrafo(rodadas):
    
    # Define o grafo e 14 cores diferentes
    G = nx.DiGraph()
    cores = plt.cm.nipy_spectral(np.linspace(0, 1, 14))

    # Adiciona todas as arestas no grafo
    for r in rodadas:
        for jogo in rodadas[r]["jogos"]: 
            G.add_edge(jogo[0], jogo[1], color=cores[r-1], rodada=r)

    # Usa a função de spring layout de nx para evitar sobreposição das arestas, deixando as arestas mais curvas.
    mola = nx.spring_layout(G, seed=42, k=0.5)
    
    # Configuração base para o plot do grafo
    plt.figure(figsize=(22, 15))
    corVertices = [G[u][v]['color'] for u, v in G.edges()]
    nomeVertice = {(u, v): G[u][v]['rodada'] for u, v in G.edges()}

    # Desenha o grafo
    nx.draw(G, mola, with_labels=True, node_size = 3000, node_color = 'lightblue', edge_color = corVertices, arrows = True, arrowsize = 25, connectionstyle = 'arc3,rad=0.1', width = 1.5)
    
    # Desenha o número nas arestas
    nx.draw_networkx_edge_labels(G, mola, edge_labels = nomeVertice, font_size = 10, label_pos = 0.75, font_color = 'darkred')

    #Adiciona legenda de cores, para facilitar a visualização
    legenda = [Patch(facecolor = cores[i], label= f'Rodada {i+1}') for i in range(14)]
    plt.legend(handles = legenda, loc = 'upper right', title = "Rodadas")

    # Chama função de plotar
    plt.tight_layout()
    plt.show()
    

# Função para gerar todas as possíveis 42 combinações de jogos (tanto de ida quanto de volta)
def gerarCombinacaoJogos():
    
    # Adiciona nessa lista vazia as combinações
    jogos = []

    for mandante in times:
        for visitante in times:
            if mandante != visitante:
                jogos.append((mandante, visitante))
    
    return jogos


# FUnção que ordena os jogos mais restritos primeiro, para otimizar o algoritmo
def ordenarJogosPorRestricao(jogos):
    
    prioridadeJogos = []
    
    for jogo in jogos:
        rodadasProibidas = restricoesRodadas.get(jogo, [])
        rodadasDisponiveis = 14 - len(rodadasProibidas)
        prioridadeJogos.append((rodadasDisponiveis, jogo))
    
    prioridadeJogos.sort()

    return [jogo for (_, jogo) in prioridadeJogos]

# Função que verifica se o mandante tem restrição contra algum outro mandante, retornando True ou False
def verificaRestricaoMandante(rodada, novoMandante, rodadas):

    for mandante in rodadas["mandantes"]:
        if novoMandante in restricaoMandante.get(mandante, []):
            return True
    
    return False

# Função que implementa um algoritmo guloso para coloração em grafos
def algoritmoGuloso(jogosOrdenados, maxTentativas):
    
    # Foi necessário estipular um máximo de tentativas, para garantir que se o algoritmo não ache uma solução que tenha os 42 jogos por 14 rodadas, ele pare
    for tentativa in range(maxTentativas):
       
        rodadas = {i: {"mandantes": set(), "visitantes": set(), "jogos": []} for i in range(1, 15)}
        
        # Randomiza a ordem de percorrimento dos vértices
        random.shuffle(jogosOrdenados) 
        
        for jogo in jogosOrdenados:
            mandante, visitante = jogo
            rodadasValidas = [r for r in range(1, 15) if r not in restricoesRodadas.get(jogo, [])]
            alocado = False
            
            for i in rodadasValidas:
               
                # Verifica se os times já estão na rodada
                if (mandante in rodadas[i]["mandantes"] or
                    mandante in rodadas[i]["visitantes"] or
                    visitante in rodadas[i]["mandantes"] or
                    visitante in rodadas[i]["visitantes"]):
                    continue
                
                # Verifica restricao de mandantes
                if verificaRestricaoMandante(i, mandante, rodadas[i]):
                    continue
                
                # Se jogo é permitido, aloca e dá break
                rodadas[i]["mandantes"].add(mandante)
                rodadas[i]["visitantes"].add(visitante)
                rodadas[i]["jogos"].append(jogo)
                alocado = True
                break
            
            # Se não, reinicia a tentativa
            if not alocado:
                break
        
        # Verifica se todas as rodadas têm 3 jogos (Para garantir que todos os times joguem contra todos os times nas 14 rodadas)
        sucesso = True
        for i in rodadas:
            if len(rodadas[i]["jogos"]) != 3:
                sucesso = False
                break
        
        if sucesso:
            # Retorna a solução e o número de tentativas
            return rodadas, tentativa + 1 
    
    # Caso contrário, retorna None
    return None, maxTentativas


# Função para printar as rodadas
def printRodadas(rodadas):

    for i in rodadas:
        
        jogos = rodadas[i]["jogos"]
        print(f"Rodada {i}:")
        
        for jogo in jogos:
            print(f"  {jogo[0]} (Mandante) vs {jogo[1]} (Visitante)")
        print()

# Main
def main():
    
    jogos = gerarCombinacaoJogos()
    jogosOrdenados = ordenarJogosPorRestricao(jogos)
    resposta, tentativas = algoritmoGuloso(jogosOrdenados, maxTentativas = 500)
    
    if resposta:
        print(f"Resposta encontrada após {tentativas} tentativas")
        printRodadas(resposta)
        plotaGrafo(resposta)

    else:
        print(f"Nenhuma resposta válida encontrada após {tentativas} tentativas.")


if __name__ == "__main__":
    main()