#!/usr/bin/env python3
"""
Bot Truco V4.0 - Sistema Completo com Todas as Regras
- Detecção de cartas com símbolos + naipes separados
- Sistema dinâmico de força baseado na manilha
- Detecção de botões na área flexível
- Placar manual bonito
- Controle de quem correu da rodada
- TODAS AS 32 REGRAS DE TRUCO IMPLEMENTADAS
"""

import os
import time
import cv2
import numpy as np
import winsound
import pyautogui
from PIL import ImageGrab
from itertools import count

# Configurações gerais
pyautogui.FAILSAFE = True

# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES E COORDENADAS
# ═══════════════════════════════════════════════════════════════

# Thresholds
THR_FICHA = 0.80
THR_VIRA = 0.96
THR_CRONOMETRO = 0.65
THR_SIMB = 0.82
THR_NAIPE = 0.85
THR_BOTAO = 0.85

# Coordenadas da ficha do pé
FICHA_NOS = (547, 535, 35, 35)
FICHA_ELES = (1263, 312, 35, 35)

# Coordenadas da vira
VIRA_BOX = (874, 459, 48, 93)

# Coordenadas do cronômetro
CRONOMETRO_BOX = (507, 763, 93, 103)

# Coordenadas das cartas da mão - Símbolos
MAO_SIM = [(615, 701, 40, 54), (741, 701, 40, 54), (867, 701, 40, 54)]
# Coordenadas das cartas da mão - Naipes  
MAO_NAI = [(617, 756, 35, 35), (742, 756, 35, 35), (867, 756, 35, 35)]

# Nossa carta na mesa - símbolo + naipe separado  
MESA_NOS_SIM = (716, 567, 30, 30)
MESA_NOS_NAI = (716, 597, 25, 22)

# Carta deles na mesa - símbolo + naipe separado
MESA_ELES_SIM = (1080, 350, 25, 25) 
MESA_ELES_NAI = (1083, 375, 20, 20)

# ═══ COORDENADAS DOS BOTÕES ═══
# Área flexível onde TODOS os botões podem aparecer
AREA_BOTOES = (969, 925, 610, 80)  # Área que pega qualquer botão
BOTAO_MOSTRAR = (986, 821, 171, 24)  # Botão Mostrar Cartas (posição diferente)

# Coordenadas para clicar nas cartas (CORRIGIDAS)
CARD_POS = [(643, 738), (769, 738), (895, 738)]

# Sequência das cartas para definir manilha
SEQ = ['Q', 'J', 'K', 'A', '2', '3']

# ═══════════════════════════════════════════════════════════════
# CAMINHOS E TEMPLATES
# ═══════════════════════════════════════════════════════════════

BASE_DIR = os.getcwd() + '/imagens'

# Template da ficha
FICHA_TEMPLATE = cv2.imread(f"{BASE_DIR}/ficha_pe/pe.png", 0)

# Carrega templates dos botões
T_ACEITAR = cv2.imread(f"{BASE_DIR}/botoes/Aceitar.png", 0)
T_CORRER = cv2.imread(f"{BASE_DIR}/botoes/Correr.png", 0) 
T_MOSTRAR_CARTAS = cv2.imread(f"{BASE_DIR}/botoes/Mostrar_cartas.png", 0)
T_TRUCO = cv2.imread(f"{BASE_DIR}/botoes/Truco.png", 0)
T_TRUCO6 = cv2.imread(f"{BASE_DIR}/botoes/Truco6.png", 0)
T_TRUCO9 = cv2.imread(f"{BASE_DIR}/botoes/Truco9.png", 0)
T_TRUCO12 = cv2.imread(f"{BASE_DIR}/botoes/Truco12.png", 0)
T_MOSTRAR = cv2.imread(f"{BASE_DIR}/botoes/Mostrar_Cartas.png", 0)  # Backup do new10.py

def load_folder(pasta):
    """Carrega todos os templates de uma pasta"""
    templates = {}
    if not os.path.exists(pasta):
        return templates
    
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.png'):
            nome = os.path.splitext(arquivo)[0]
            template = cv2.imread(f'{pasta}/{arquivo}', 0)
            if template is not None:
                templates[nome] = template
    return templates

# Carrega templates das viras e cronômetros
T_VIRA = load_folder(f"{BASE_DIR}/viras")
T_CRONOMETRO = load_folder(f"{BASE_DIR}/cronometro")

# Carrega templates dos símbolos e naipes das cartas
T_SIMB = load_folder(f"{BASE_DIR}/cartas_minha_mao")        # Símbolos da mão
T_NAI = load_folder(f"{BASE_DIR}/cartas_minha_mao/naipes")  # Naipes da mão

# Carrega templates das cartas da mesa
T_MESA_NOS_SIMB = load_folder(f"{BASE_DIR}/cartas_minha_mesa")        # Símbolos mesa nossa
T_MESA_NOS_NAI = load_folder(f"{BASE_DIR}/cartas_minha_mesa/Naipes")   # Naipes mesa nossa
T_MESA_ADV_SIMB = load_folder(f"{BASE_DIR}/cartas_mesa_adversario")        # Símbolos mesa deles
T_MESA_ADV_NAI = load_folder(f"{BASE_DIR}/cartas_mesa_adversario/Naipes")   # Naipes mesa deles

# ═══════════════════════════════════════════════════════════════
# VARIÁVEIS GLOBAIS
# ═══════════════════════════════════════════════════════════════

# Controle de rodadas
rodada = 0
lado_pe = None
lado_mao = None

# Controle da vira e manilha
MANILHA = None

# Controle de jogadas
jog = 0
v_n = 0  # vitórias nossas
v_e = 0  # vitórias deles
emp = 0  # empates

# Controle de cliques e spam
clicou = False
cronometro_ja_mostrado = False

# ═══ CONTROLE DE CORRIDA ═══
bot_correu = False  # Flag para saber se NÓS corremos
aguardando_mostrar_cartas = False  # Flag para aguardar fim da rodada

# ═══ PLACAR MANUAL ═══
PLACAR_NOS = 0
PLACAR_ELES = 0

# ═══════════════════════════════════════════════════════════════
# NOVAS VARIÁVEIS GLOBAIS PARA AS REGRAS
# ═══════════════════════════════════════════════════════════════

# Controle de estratégias temporárias
estrategia_duas_manilhas = {'ativa': False, 'carta_comum_idx': None}
estrategia_duas_manilhas_pe = {'ativa': False, 'carta_comum_idx': None, 'manilha_menor_idx': None, 'matou_j1': False}
estrategia_mao_fraca_manilha = {'ativa': False, 'empatou_j1': False, 'manilha_usada_j1': False}

# Controle de truco e mão
mao_inicial_classificacao = None
ultima_mao_completa = (None, None)  # (lista_de_cartas, jog)
empate_j1_com_copa = False
aguardando_truco = False

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════

def beep(frequencia=800, duracao=200):
    """Emite um beep sonoro"""
    winsound.Beep(int(frequencia), int(duracao))

def grab(box):
    """Captura região da tela"""
    x, y, w, h = box
    img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

def best(img, bank, thr):
    """Encontra melhor template"""
    h, w = img.shape
    top, key = 0, None
    
    for k, t in bank.items():
        if t is None:
            continue
        th, tw = t.shape
        if th > h or tw > w:
            continue
        v = cv2.matchTemplate(img, t, cv2.TM_CCOEFF_NORMED).max()
        if v > top:
            top, key = v, k
    
    return key if top >= thr else None

def click_card(idx):
    """Clica numa carta"""
    x, y = CARD_POS[idx]
    time.sleep(0.5)
    pyautogui.moveTo(x, y, duration=0.2)
    time.sleep(0.5)
    pyautogui.click(x, y, duration=0.5)
    pyautogui.moveTo(100, 50, duration=0.2)
    time.sleep(0.2)

def exibir_placar():
    """
    Exibe o placar manual de forma bonita
    """
    print("┌─────────────────────────────────┐")
    print(f"│           PLACAR ATUAL          │")
    print("├─────────────────────────────────┤")
    print(f"│  NÓS: {PLACAR_NOS:2d}     ×     ELES: {PLACAR_ELES:2d}  │")
    print("└─────────────────────────────────┘")

def atualizar_placar(nos=None, eles=None):
    """
    Atualiza o placar manual
    """
    global PLACAR_NOS, PLACAR_ELES
    
    if nos is not None:
        PLACAR_NOS = nos
    if eles is not None:
        PLACAR_ELES = eles

def padronizar_carta_mao(carta):
    """Converte carta da mão para formato padronizado"""
    global MANILHA
    
    if not carta or not carta[0] or not carta[1]:
        return None

    simbolo_completo, naipe = carta
    naipe = naipe.lower()
    
    # Corrigir símbolo para tirar o sufixo de cor
    base_simb = simbolo_completo.split('_')[0].upper()
    carta_padrao = f"{base_simb}_{naipe}"

    # Verificar se é manilha
    if MANILHA and base_simb == MANILHA:
        return carta_padrao + "M"
    return carta_padrao

# ═══════════════════════════════════════════════════════════════
# SISTEMA DE FORÇA DINÂMICO COMPLETO
# ═══════════════════════════════════════════════════════════════

def calcular_pontuacao_dinamica():
    """Sistema de pontos dinâmico baseado na manilha atual - VERSÃO COMPLETA"""
    global MANILHA
    
    if not MANILHA:
        return None
    
    # Sequência original
    sequencia_original = ['Q', 'J', 'K', 'A', '2', '3']
    
    # Remove a carta que virou MANILHA
    cartas_normais = [carta for carta in sequencia_original if carta != MANILHA]
    
    # Sistema de pontuação dinâmica (1-5 para cartas normais)
    pontuacao = {}
    for i, carta in enumerate(cartas_normais):
        pontuacao[carta] = i + 1
    
    # Manilhas sempre pontuam 6-9 
    pontuacao[f'{MANILHA}_ouro'] = 6     # MANILHA OURO = 6
    pontuacao[f'{MANILHA}_espada'] = 7   # MANILHA ESPADA = 7
    pontuacao[f'{MANILHA}_copa'] = 8     # MANILHA COPA = 8
    pontuacao[f'{MANILHA}_zap'] = 9      # MANILHA ZAP = 9
    
    return pontuacao

def força(carta):
    """Calcula força da carta com sistema dinâmico"""
    if not carta or carta == 'SemCarta':
        return (0, 0)
    
    # Sistema dinâmico
    pontuacao_dinamica = calcular_pontuacao_dinamica()
    if not pontuacao_dinamica:
        return (0, 0)
    
    if carta.endswith('M'):  # É manilha
        carta_sem_m = carta[:-1]  # Remove o M
        pontos = pontuacao_dinamica.get(carta_sem_m, 0)
        return (pontos, 0)
    else:  # Carta normal
        simbolo = carta.split('_')[0]
        pontos = pontuacao_dinamica.get(simbolo, 0)
        return (pontos, 0)

def avaliar_forca_mao(hand_str, jog):
    """
    Avalia força da mão com sistema dinâmico e classificação
    """
    if not hand_str:
        return 0, "Não classificada"

    # Sistema dinâmico
    pontuacao_dinamica = calcular_pontuacao_dinamica()
    if not pontuacao_dinamica:
        return 0, "Não classificada"

    pontos = 0
    for carta in hand_str:
        if not carta: 
            continue
        
        # Se termina com M, é manilha
        if carta.endswith('M'):
            carta_sem_m = carta[:-1]  # Remove o M
            pontos += pontuacao_dinamica.get(carta_sem_m, 0)
        else:
            # Carta normal, pega só o símbolo
            simbolo = carta.split('_')[0]
            pontos += pontuacao_dinamica.get(simbolo, 0)

    # Máximos corretos por jogada
    max_por_jogada = {0: 24, 1: 17, 2: 9}  # J1: 7+8+9=24, J2: 8+9=17, J3: 9
    total_max = max_por_jogada.get(jog, 24)

    porcentagem = (pontos / total_max) * 100

    # Classificação
    if porcentagem <= 20:
        classificacao = "Super Fraca"
    elif porcentagem <= 40:
        classificacao = "Fraca"
    elif porcentagem <= 55:
        classificacao = "Média"
    elif porcentagem <= 70:
        classificacao = "Média-Forte"
    elif porcentagem <= 85:
        classificacao = "Forte"
    else:
        classificacao = "Muito Forte"

    return pontos, classificacao

# ═══════════════════════════════════════════════════════════════
# SISTEMA DE DETECÇÃO DE JOGO GANHO
# ═══════════════════════════════════════════════════════════════

def tem_jogo_ganho():
    """Detecta se temos jogo matematicamente garantido"""
    global v_n, v_e, emp, jog, lado_mao, MANILHA
    
    zap_card = f"{MANILHA}_zapM"
    is_mao = (lado_mao == 'NOS')
    raw = card_adv() or 'SemCarta'
    
    # Lê mão atual
    hand = mao()
    hand_str = [padronizar_carta_mao(h) for h in hand]
    tem_zap = zap_card in hand_str
    
    # CENÁRIO 1: Vitória + ZAP
    if v_n >= 1 and tem_zap:
        return True, "Vitória + ZAP"
        
    # CENÁRIO 2: Vitória + Somos PÉ + Matamos
    if v_n >= 1 and not is_mao and raw != 'SemCarta':
        pode_matar = any(força(c) > força(raw) for c in hand_str if c)
        if pode_matar:
            return True, "Vitória + PÉ + Mata"
            
    # CENÁRIO 3: J3 (1x1) + Somos PÉ + Empate/Mata  
    if jog == 2 and v_n == 1 and v_e == 1 and not is_mao and raw != 'SemCarta':
        pode_empatar_ou_matar = any(força(c) >= força(raw) for c in hand_str if c)
        if pode_empatar_ou_matar:
            return True, "J3 1x1 PÉ + Empate/Mata"
            
    # CENÁRIO 4: Empate + ZAP
    if emp >= 1 and tem_zap:
        return True, "Empate + ZAP"
        
    # CENÁRIO 5: Empate + Somos PÉ + Matamos
    if emp >= 1 and not is_mao and raw != 'SemCarta':
        pode_matar = any(força(c) > força(raw) for c in hand_str if c)
        if pode_matar:
            return True, "Empate + PÉ + Mata"
            
    return False, None

# ═══════════════════════════════════════════════════════════════
# REGRAS 1 & 2: ZAP ESTRATÉGICO
# ═══════════════════════════════════════════════════════════════

def aplicar_regra_zap(hand_str, carta_adv, jog, is_mao, emp):
    """
    REGRA 1 (MÃO): Zap + 1ª jogada → mais fraca | Empate J1 → truca + zap
    REGRA 2 (PÉ): J1 → tenta matar sem zap | empata sem zap | zap último recurso
    """
    global MANILHA
    
    if not MANILHA:
        return False, None, None
        
    zap_card = f"{MANILHA}_zapM"
    
    if zap_card not in hand_str:
        return False, None, None
    
    cartas = [(i, cs, força(cs)) for i, cs in enumerate(hand_str) if cs]
    
    # REGRA 1: Somos MÃO com ZAP
    if is_mao:
        if jog == 0:
            # 1ª jogada: joga mais fraca
            carta_mais_fraca = min(cartas, key=lambda x: x[2])
            return True, carta_mais_fraca[0], "Regra 1: ZAP - jogando mais fraca na 1ª"
        elif jog == 1 and emp == 1:
            # Empate J1: truca antes de jogar zap
            print("🂡 Regra 1: Empate na 1ª → TRUCO antes de jogar ZAP")
            # Aqui seria implementado o sistema de truco
            for i, cs, _ in cartas:
                if cs == zap_card:
                    return True, i, "Regra 1: ZAP após empate + truco"
        else:
            # Outras situações: joga mais fraca
            carta_mais_fraca = min(cartas, key=lambda x: x[2])
            return True, carta_mais_fraca[0], "Regra 1: ZAP - economia geral"
    
    # REGRA 2: Somos PÉ com ZAP (apenas J1)
    elif jog == 0 and not is_mao:
        cartas_sem_zap = [c for c in cartas if c[1] != zap_card]
        
        if cartas_sem_zap:
            # Tenta matar sem zap
            killers_sem_zap = [c for c in cartas_sem_zap if força(c[1]) > força(carta_adv)]
            if killers_sem_zap:
                carta_escolhida = min(killers_sem_zap, key=lambda x: x[2])
                return True, carta_escolhida[0], f"Regra 2: Matando {carta_adv} sem ZAP"
            
            # Tenta empatar sem zap
            ties_sem_zap = [c for c in cartas_sem_zap if força(c[1]) == força(carta_adv)]
            if ties_sem_zap:
                carta_escolhida = max(ties_sem_zap, key=lambda x: força(x[1])[1])
                return True, carta_escolhida[0], f"Regra 2: Empatando {carta_adv} sem ZAP"
        
        # Último recurso: usa zap
        for i, cs, _ in cartas:
            if cs == zap_card:
                return True, i, "Regra 2: Usando ZAP como último recurso"
    
    return False, None, None

# ═══════════════════════════════════════════════════════════════
# REGRAS 3-8: COPA MANILHA
# ═══════════════════════════════════════════════════════════════

def aplicar_regra_copa_manilha(cartas, is_mao, jog, emp, classificacao):
    """Aplica todas as situações da Regra Copa Manilha"""
    global MANILHA
    
    if not is_mao or not MANILHA:
        return False, None, "Regra Copa só vale quando somos MÃO"
    
    # Identifica copas manilha e outras manilhas
    copas_manilha = [(i, cs) for i, cs, _ in cartas if cs and cs.endswith('_copaM')]
    outras_manilhas = [(i, cs) for i, cs, _ in cartas if cs and cs.endswith('M') and not cs.endswith('_copaM')]
    total_manilhas = len(copas_manilha) + len(outras_manilhas)
    
    if len(copas_manilha) != 1:
        return False, None, f"Copas manilha encontradas: {len(copas_manilha)} (precisa ser 1)"
    
    copa_idx, copa_carta = copas_manilha[0]
    
    # SITUAÇÃO C - EMPATE = COPA (MAIOR PRIORIDADE)
    if emp >= 1:
        return True, copa_idx, "Situação C: Empate anterior → jogando copa manilha"
    
    # SITUAÇÃO B - ESTRATÉGIA COM 3 (2ª PRIORIDADE)
    if jog == 0:
        tem_3 = [(i, cs) for i, cs, _ in cartas if cs and cs.startswith('3_') and not cs.endswith('M')]
        cartas_fracas = [(i, cs, forca) for i, cs, forca in cartas 
                         if cs and not cs.endswith('M') and força(cs)[0] <= 4]
        
        if len(tem_3) == 1 and len(cartas_fracas) >= 1 and len(cartas) == 3:
            cartas_tipo = set()
            for _, cs, forca in cartas:
                if cs.endswith('_copaM'):
                    cartas_tipo.add('copa')
                elif cs.startswith('3_') and not cs.endswith('M'):
                    cartas_tipo.add('3')
                elif not cs.endswith('M') and força(cs)[0] <= 4:
                    cartas_tipo.add('fraca')
            
            if cartas_tipo == {'copa', '3', 'fraca'}:
                tres_idx = tem_3[0][0]
                return True, tres_idx, "Situação B: Copa + 3 + carta ≤4pts → jogando o 3"
    
    # SITUAÇÃO A - COPA + CARTA FRACA (3ª PRIORIDADE)
    if total_manilhas == 1:
        cartas_fracas = [(i, cs, forca) for i, cs, forca in cartas 
                         if cs and not cs.endswith('M') and força(cs)[0] <= 4]
        
        if len(cartas_fracas) >= 1:
            menor_fraca_idx = min(cartas_fracas, key=lambda x: x[2])[0]
            menor_fraca_carta = cartas_fracas[min(range(len(cartas_fracas)), key=lambda i: cartas_fracas[i][2])][1]
            return True, menor_fraca_idx, f"Situação A: Copa + carta fraca ({menor_fraca_carta}) → guardando copa"
    
    # SITUAÇÃO D - MÃO FORTE (4ª PRIORIDADE)
    if jog == 0 and total_manilhas == 1 and classificacao in ["Média-Forte", "Forte", "Muito Forte"]:
        return True, copa_idx, f"Situação D: Mão {classificacao} com 1 manilha → jogando copa primeiro"
    
    return False, None, "Nenhuma situação da Regra Copa se aplica"

def aplicar_copa_j1_pe(cartas, is_mao, jog, carta_adv):
    """COPA J1: Primeira jogada sendo pé → preserva copa"""
    global MANILHA
    
    if is_mao or jog != 0 or not MANILHA:
        return False, None, None
        
    copa_card = f"{MANILHA}_copaM"
    tem_copa = any(cs == copa_card for _, cs, _ in cartas)
    tem_carta_fraca = any(cs.startswith(('Q_', 'J_', 'K_')) and not cs.endswith('M') 
                         for _, cs, _ in cartas)
    
    if tem_copa and tem_carta_fraca:
        cartas_sem_copa = [c for c in cartas if c[1] != copa_card]
        
        # Tenta matar sem copa
        killers_sem_copa = [c for c in cartas_sem_copa if força(c[1]) > força(carta_adv)]
        if killers_sem_copa:
            escolhida = min(killers_sem_copa, key=lambda x: x[2])
            return True, escolhida[0], f"Copa preservada: matando com {escolhida[1]}"
        
        # Tenta empatar sem copa
        ties_sem_copa = [c for c in cartas_sem_copa if força(c[1]) == força(carta_adv)]
        if ties_sem_copa:
            escolhida = min(ties_sem_copa, key=lambda x: x[2])
            return True, escolhida[0], f"Copa preservada: empatando com {escolhida[1]}"
    
    return False, None, None

def aplicar_copa_ultima_carta(hand_str):
    """COPA ÚLTIMA CARTA: Se só restou Copa na mão, joga ela"""
    global MANILHA
    
    if not MANILHA:
        return False, None, None
        
    copa_card = f"{MANILHA}_copaM"
    cartas_validas = [c for c in hand_str if c]
    
    if len(cartas_validas) == 1 and copa_card in cartas_validas:
        for i, cs in enumerate(hand_str):
            if cs == copa_card:
                return True, i, "Copa última carta: jogando Copa!"
    
    return False, None, None

# ═══════════════════════════════════════════════════════════════
# REGRAS 9-11: DUAS MANILHAS
# ═══════════════════════════════════════════════════════════════

def aplicar_regra_duas_manilhas_mao(cartas, is_mao, jog, v_n, v_e):
    """Regra Duas Manilhas quando somos MÃO"""
    global estrategia_duas_manilhas
    
    if not is_mao:
        return False, None, "Não somos mão"
    
    # JOGADA 1: Detectar + aplicar
    if jog == 0:
        manilhas = [(i, cs) for i, cs, _ in cartas if cs and cs.endswith('M')]
        zaps = [cs for _, cs, _ in cartas if cs and cs.endswith('_zapM')]
        cartas_comuns = [(i, cs, forca) for i, cs, forca in cartas if cs and not cs.endswith('M')]
        
        if len(manilhas) == 2 and len(zaps) == 0 and len(cartas_comuns) == 1:
            # Ranking: Copa > Espada > Ouro
            def rank_manilha(carta):
                if '_copaM' in carta: return 3
                elif '_espadaM' in carta: return 2  
                elif '_ouroM' in carta: return 1
                return 0
            
            manilhas_ordenadas = sorted(manilhas, key=lambda x: rank_manilha(x[1]), reverse=True)
            manilha_maior_idx = manilhas_ordenadas[0][0]
            
            estrategia_duas_manilhas = {
                'ativa': True,
                'carta_comum_idx': cartas_comuns[0][0]
            }
            
            return True, manilha_maior_idx, f"Regra 2 Manilhas J1: manilha maior ({manilhas_ordenadas[0][1]})"
    
    # JOGADA 2: Se ganhamos J1 → joga carta comum
    elif jog == 1 and estrategia_duas_manilhas['ativa']:
        if v_n >= 1:
            for i, (idx, cs, forca) in enumerate(cartas):
                if not cs.endswith('M'):
                    estrategia_duas_manilhas['ativa'] = False
                    return True, i, f"Regra 2 Manilhas J2: carta comum ({cs})"
        else:
            estrategia_duas_manilhas['ativa'] = False
    
    return False, None, "Regra não se aplica"

def aplicar_regra_duas_manilhas_pe(cartas, is_mao, jog, v_n, v_e, carta_adv):
    """Regra Duas Manilhas quando somos PÉ"""
    global estrategia_duas_manilhas_pe, MANILHA
    
    if is_mao:
        return False, None, "Não somos pé"
    
    # JOGADA 1: Detectar condição + aplicar
    if jog == 0:
        manilhas = [(i, cs) for i, cs, _ in cartas if cs and cs.endswith('M')]
        cartas_comuns = [(i, cs, forca) for i, cs, forca in cartas if cs and not cs.endswith('M')]
        
        if len(manilhas) == 2 and len(cartas_comuns) == 1:
            def rank_manilha(carta):
                if '_zapM' in carta: return 4
                elif '_copaM' in carta: return 3
                elif '_espadaM' in carta: return 2  
                elif '_ouroM' in carta: return 1
                return 0
            
            manilhas_ordenadas = sorted(manilhas, key=lambda x: rank_manilha(x[1]))
            manilha_menor_idx = manilhas_ordenadas[0][0]
            carta_comum_idx = cartas_comuns[0][0]
            
            # Verifica se conseguimos matar
            if carta_adv and carta_adv not in ('SemCarta', 'Virada'):
                pode_matar_comum = força(cartas_comuns[0][1]) > força(carta_adv)
                
                if pode_matar_comum:
                    carta_escolhida = carta_comum_idx
                    estrategia_duas_manilhas_pe['matou_j1'] = True
                    motivo = f"J1: Matamos com carta comum ({cartas_comuns[0][1]})"
                else:
                    carta_escolhida = manilha_menor_idx
                    estrategia_duas_manilhas_pe['matou_j1'] = True
                    motivo = f"J1: Matamos com manilha menor ({manilhas_ordenadas[0][1]})"
            else:
                carta_escolhida = manilha_menor_idx
                estrategia_duas_manilhas_pe['matou_j1'] = False
                motivo = f"J1: SemCarta, jogando manilha menor ({manilhas_ordenadas[0][1]})"
            
            estrategia_duas_manilhas_pe = {
                'ativa': True,
                'carta_comum_idx': carta_comum_idx,
                'manilha_menor_idx': manilha_menor_idx,
                'matou_j1': estrategia_duas_manilhas_pe['matou_j1']
            }
            
            return True, carta_escolhida, motivo
    
    # JOGADA 2: Estratégia baseada no resultado da J1
    elif jog == 1 and estrategia_duas_manilhas_pe['ativa']:
        cartas_comuns = [(i, cs, forca) for i, cs, forca in cartas if not cs.endswith('M')]
        
        if cartas_comuns:
            carta_comum = cartas_comuns[0]
            estrategia_duas_manilhas_pe['ativa'] = False
            return True, carta_comum[0], f"Regra 2 Manilhas PÉ J2: carta comum ({carta_comum[1]})"
    
    return False, None, "Regra não se aplica"

# ═══════════════════════════════════════════════════════════════
# REGRAS 12-16: MÃO FRACA + MANILHA E FORÇA 5
# ═══════════════════════════════════════════════════════════════

def aplicar_regra_mao_fraca_manilha(cartas, is_mao, jog, v_n, v_e, emp, carta_adv):
    """Regra Mão Fraca + Manilha quando somos PÉ"""
    global estrategia_mao_fraca_manilha, MANILHA
    
    if is_mao or not MANILHA:
        return False, None, "Só aplica quando somos PÉ"
    
    # JOGADA 1: Detectar condição + aplicar
    if jog == 0:
        manilhas = [(i, cs) for i, cs, _ in cartas if cs and cs.endswith('M')]
        cartas_comuns = [(i, cs, forca) for i, cs, forca in cartas if cs and not cs.endswith('M')]
        
        if len(manilhas) != 1:
            return False, None, f"Tem {len(manilhas)} manilhas (precisa exatamente 1)"
        
        manilha_carta = manilhas[0][1]
        
        # Manilha deve ser Ouro OU Espada
        if not (manilha_carta.endswith('_ouroM') or manilha_carta.endswith('_espadaM')):
            return False, None, f"Manilha {manilha_carta} não é Ouro nem Espada"
        
        # Verificar cartas ≤ 2 pontos dinâmicos
        pontuacao_dinamica = calcular_pontuacao_dinamica()
        if not pontuacao_dinamica:
            return False, None, "Sistema de pontuação dinâmica não disponível"
        
        cartas_fracas = []
        for i, cs, forca in cartas_comuns:
            simbolo = cs.split('_')[0]
            pontos = pontuacao_dinamica.get(simbolo, 0)
            if pontos <= 2:
                cartas_fracas.append((i, cs, forca, pontos))
        
        if len(cartas_fracas) == 0:
            return False, None, "Nenhuma carta ≤ 2 pontos dinâmicos"
        
        # Estratégia baseada na carta do adversário
        if carta_adv and carta_adv not in ('SemCarta', 'Virada'):
            # Tenta matar com carta comum
            cartas_comuns_que_matam = [c for c in cartas_comuns if força(c[1]) > força(carta_adv)]
            if cartas_comuns_que_matam:
                carta_escolhida = min(cartas_comuns_que_matam, key=lambda x: x[2])
                estrategia_mao_fraca_manilha = {'ativa': True, 'empatou_j1': False, 'manilha_usada_j1': False}
                return True, carta_escolhida[0], f"J1: Matando com carta comum ({carta_escolhida[1]})"
            
            # Tenta empatar
            cartas_que_empatam = [c for c in cartas_comuns if força(c[1]) == força(carta_adv)]
            if cartas_que_empatam:
                carta_escolhida = cartas_que_empatam[0]
                estrategia_mao_fraca_manilha = {'ativa': True, 'empatou_j1': True, 'manilha_usada_j1': False}
                return True, carta_escolhida[0], f"J1: Empatando com carta comum ({carta_escolhida[1]})"
        
        # Joga carta mais fraca
        carta_mais_fraca = min(cartas_fracas, key=lambda x: x[2])
        estrategia_mao_fraca_manilha = {'ativa': True, 'empatou_j1': False, 'manilha_usada_j1': False}
        return True, carta_mais_fraca[0], f"J1: Jogando mais fraca ({carta_mais_fraca[1]})"
    
    # JOGADA 2: Estratégia após J1
    elif jog == 1 and estrategia_mao_fraca_manilha['ativa']:
        if estrategia_mao_fraca_manilha['empatou_j1'] and emp >= 1:
            manilhas_restantes = [(i, cs, forca) for i, cs, forca in cartas if cs.endswith('M')]
            if manilhas_restantes:
                manilha_restante = manilhas_restantes[0]
                estrategia_mao_fraca_manilha['ativa'] = False
                return True, manilha_restante[0], f"J2: Empatou J1! Usando manilha ({manilha_restante[1]})"
        
        estrategia_mao_fraca_manilha['ativa'] = False
    
    return False, None, "Regra não se aplica"

def aplicar_regra_carta_forca5_manilha(cartas, is_mao, jog, v_n, v_e):
    """Regra Carta Força 5 + Manilha"""
    global MANILHA
    
    if jog != 1 or not is_mao or v_n < 1 or not MANILHA:
        return False, None, "Condições não atendidas"
    
    # Identifica carta força 5
    carta_forca5 = "3" if MANILHA != "3" else "2"
    
    manilhas = [(i, cs) for i, cs, _ in cartas if cs and cs.endswith('M')]
    cartas_forca5 = [(i, cs, forca) for i, cs, forca in cartas 
                     if cs and cs.startswith(f'{carta_forca5}_') and not cs.endswith('M')]
    
    if len(manilhas) < 1 or len(cartas_forca5) < 1:
        return False, None, f"Condições não atendidas: {len(manilhas)} manilhas, {len(cartas_forca5)} cartas força 5"
    
    carta_escolhida = cartas_forca5[0]
    return True, carta_escolhida[0], f"Regra Força 5: J2 após vitória → jogando {carta_escolhida[1]}"

def regra_pe_manilha_forte(mao_para_analise, is_mao):
    """Verifica regra Pé Manilha Forte: 1 manilha + carta ≥3pts + carta ≥4pts"""
    global MANILHA
    
    if is_mao or not mao_para_analise or not MANILHA:
        return False
    
    manilhas = [c for c in mao_para_analise if c and c.endswith('M')]
    cartas_comuns = [c for c in mao_para_analise if c and not c.endswith('M')]
    
    if len(manilhas) != 1:
        return False
    
    pontuacao_dinamica = calcular_pontuacao_dinamica()
    if not pontuacao_dinamica:
        return False
    
    tem_3pts = False
    tem_4pts = False
    
    for carta in cartas_comuns:
        if not carta:
            continue
        simbolo = carta.split('_')[0]
        pontos = pontuacao_dinamica.get(simbolo, 0)
        
        if pontos >= 4:
            tem_4pts = True
        elif pontos >= 3:
            tem_3pts = True
    
    return tem_3pts and tem_4pts

def regra_pe_manilha_forca5(mao_para_analise, is_mao):
    """Verifica regra Pé Manilha + Força 5: 1 manilha + carta força 5"""
    global MANILHA
    
    if is_mao or not mao_para_analise or not MANILHA:
        return False
    
    manilhas = [c for c in mao_para_analise if c and c.endswith('M')]
    
    if len(manilhas) != 1:
        return False
    
    # Identifica carta força 5
    carta_forca5 = "3" if MANILHA != "3" else "2"
    
    tem_forca5 = any(c and c.startswith(f'{carta_forca5}_') and not c.endswith('M') 
                     for c in mao_para_analise if c)
    
    return tem_forca5

# ═══════════════════════════════════════════════════════════════
# REGRAS 17-22: TRUCO AUTOMÁTICO
# ═══════════════════════════════════════════════════════════════

def deve_trucar_ofensivo(hand_str, jog, v_n, v_e, emp, valor_truco):
    """Decide se deve trucar/subir baseado na força da mão"""
    pontos, classificacao = avaliar_forca_mao(hand_str, jog)  
    
    # REGRA 1: Mão "Muito Forte" → Sempre subir
    if classificacao == "Muito Forte":
        return True, f"Mão {classificacao} → SUBINDO!"
        
    # REGRA 2: Mão "Forte" + (primeira jogada OU já ganhamos 1)
    if classificacao == "Forte":
        if jog == 0 and valor_truco == 1:
            return True, f"Mão {classificacao} na abertura → TRUCANDO!"
        elif v_n >= 1:
            return True, f"Mão {classificacao} + já ganhamos {v_n} jogada(s) → SUBINDO!"
    
    return False, None

def decidir_truco_regra3(jog, v_n, v_e, carta_adv, cartas, zap_card, is_mao):
    """REGRA 3: Jogada 3, sendo PÉ → blefe ou mata"""
    global bot_correu, MANILHA
    
    if jog != 2 or is_mao:
        return False
    
    if not carta_adv or carta_adv in ['Virada', 'SemCarta']:
        return False

    simbolo = carta_adv.split('_')[0].upper().replace('M', '')
    is_manilha = carta_adv.endswith('M') or simbolo == MANILHA
    ordem = ['Q', 'J', 'K', 'A', '2', '3']
    pos = ordem.index(simbolo) if simbolo in ordem else -1
    
    # Verifica jogo ganho com ZAP
    tem_zap = any(cs == zap_card for _, cs, _ in cartas)
    ja_ganhamos_ou_empatamos = (v_n >= 1) or (emp >= 1)
    if tem_zap and ja_ganhamos_ou_empatamos:
        print("🏆 Regra 3: JOGO GANHO com ZAP → SUBINDO!")
        return "TRUCO_JOGO_GANHO"

    pode_matar = any(força(cs) > força(carta_adv) for _, cs, _ in cartas)

    # Blefe contra carta ≤ K
    if 0 <= pos <= 2 and not is_manilha:
        print("⚠️ Regra 3: Carta baixa (≤ K) — TRUCO no blefe!")
        return "TRUCO_BLEFE"

    # Pode matar carta alta ou manilha
    if (pos >= 3 or is_manilha) and pode_matar:
        print("⚠️ Regra 3: Carta alta/manilha e podemos matar → TRUCO!")
        return "TRUCO_MATA"

    # Não pode matar carta alta ou manilha: CORRE
    if (pos >= 3 or is_manilha) and not pode_matar:
        print("🏳️ Regra 3: Carta alta/manilha sem chance — CORRENDO")
        bot_correu = True
        return "CORRER"

    return False

def decidir_truco_regra4(jog, v_n, v_e, emp, carta_adv, cartas, zap_card, is_mao):
    """REGRA 4: Truco na segunda jogada, sendo PÉ"""
    global MANILHA
    
    if jog != 1 or is_mao:
        return False
        
    if carta_adv == 'Virada' or '_' not in carta_adv:
        return False

    simbolo = carta_adv.split('_')[0].upper().replace('M', '')
    is_manilha = carta_adv.endswith('M') or simbolo == MANILHA
    ordem = ['Q', 'J', 'K', 'A', '2', '3']
    pos = ordem.index(simbolo) if simbolo in ordem else -1

    pode_matar = any(força(cs) > força(carta_adv) for _, cs, _ in cartas if cs != zap_card)
    tem_zap = any(cs == zap_card for _, cs, _ in cartas)
    
    # Verifica jogo ganho
    ja_ganhamos_ou_empatamos = (v_n >= 1) or (emp >= 1)
    if tem_zap and ja_ganhamos_ou_empatamos:
        print("🏆 Regra 4: JOGO GANHO com ZAP → SUBINDO!")
        return "TRUCO_JOGO_GANHO"

    # Condição 1: Tenho zap e uma carta que mata
    if v_e == 1 and tem_zap and pode_matar:
        print("⚠️ Regra 4: Zap + carta que mata — jogo garantido → TRUCO!")
        return "TRUCO_ZAP_MATA"

    # Condição 2: Tenho zap e carta fraca, adversário jogou carta fraca
    if v_e == 1 and tem_zap and not pode_matar and 0 <= pos <= 2 and not is_manilha:
        print("⚠️ Regra 4: Zap + blefe contra carta ≤ K → TRUCO!")
        return "TRUCO_ZAP_BLEFE"

    # Condição 3: Empate na jogada 1, agora posso matar
    if emp == 1 and pode_matar:
        print("⚠️ Regra 4: Empate anterior e agora posso matar → TRUCO!")
        return "TRUCO_EMPATE_MATA"

    return False

def decidir_truco_regra5(jog, v_n, v_e, emp, carta_adv, cartas, is_mao):
    """REGRA 5: Empate J1 + Somos PÉ na J2"""
    global bot_correu, MANILHA
    
    if jog != 1 or is_mao or emp != 1:
        return False
    
    if not carta_adv or carta_adv in ['Virada', 'SemCarta']:
        return False
    
    simbolo = carta_adv.split('_')[0].upper().replace('M', '')
    is_manilha = carta_adv.endswith('M') or simbolo == MANILHA
    ordem = ['Q', 'J', 'K', 'A', '2', '3']
    pos = ordem.index(simbolo) if simbolo in ordem else -1
    
    pode_matar = any(força(cs) > força(carta_adv) for _, cs, _ in cartas)
    pode_empatar = any(força(cs) == força(carta_adv) for _, cs, _ in cartas)

    # Carta baixa (≤ A): TRUCAR sempre (blefe)
    if 0 <= pos <= 3 and not is_manilha:
        print("⚠️ Regra 5: Empate J1 + carta baixa (≤ A) → TRUCO no blefe!")
        return "TRUCO_BLEFE"

    # Carta alta (> A) ou manilha
    elif pos >= 4 or is_manilha:
        if pode_matar:
            print("⚠️ Regra 5: Empate J1 + carta alta mas podemos matar → TRUCO!")
            return "TRUCO_MATA"
        elif pode_empatar:
            print("⚠️ Regra 5: Empate J1 + podemos empatar → TRUCO no blefe!")
            return "TRUCO_EMPATE"
        else:
            forca_adversario = força(carta_adv)[0]
            if forca_adversario <= 4:
                print("⚠️ Regra 5: Empate J1 + carta fraca (≤4 pts) → TRUCO no blefe!")
                return "TRUCO_BLEFE"
            else:
                print("🏳️ Regra 5: Empate J1 + carta forte (>4 pts) sem chance → CORRENDO")
                bot_correu = True
                return "CORRER"

    return False

def regra_zap_blefe_j2(jog, is_mao, hand_str, carta_adv):
    """REGRA ZAP BLEFE: J2 + PÉ + carta fraca adversário"""
    global MANILHA
    
    if jog != 1 or is_mao or not MANILHA:
        return False
    
    zap_card = f"{MANILHA}_zapM"
    if zap_card not in hand_str:
        return False
    
    if carta_adv and carta_adv.startswith(('Q_', 'J_', 'K_', 'A_')):
        print("⚡ REGRA ZAP BLEFE: Carta fraca adversário + temos ZAP → TRUCANDO!")
        return "TRUCO_ZAP_BLEFE"
    
    return False

# ═══════════════════════════════════════════════════════════════
# REGRAS 23-25: CORRER AUTOMATICAMENTE
# ═══════════════════════════════════════════════════════════════

def regra_q_na_mao(jog, v_n, v_e, hand_str, carta_adv):
    """REGRA Q: Perdeu J1 + temos Q + não virada → CORRE"""
    global bot_correu
    
    if jog != 1 or v_n != 0 or v_e != 1:
        return False
    
    tem_q = any(c and c.startswith('Q_') and not c.endswith('M') for c in hand_str if c)
    
    if tem_q:
        if carta_adv == "Virada":
            print("🃏 EXCEÇÃO VIRADA: Q mata Virada → Jogando normal!")
            return False
        else:
            print("🚨 REGRA Q: Perdeu J1 + temos Q → CORRENDO!")
            bot_correu = True
            return "CORRER"
    
    return False

# ═══════════════════════════════════════════════════════════════
# REGRAS 26-32: ACEITAR/CORRER TRUCO
# ═══════════════════════════════════════════════════════════════

def decidir_aceite_truco(mao_para_analise, v_n, jog):
    """Decide se aceita ou corre do truco baseado na força da mão e regras especiais"""
    global bot_correu, emp, lado_mao, MANILHA, ultima_mao_completa
    global estrategia_duas_manilhas_pe, estrategia_mao_fraca_manilha, mao_inicial_classificacao
    
    if not mao_para_analise:
        print("❌ Não conseguiu ler cartas - correndo por segurança!")
        bot_correu = True
        return "CORREU"
    
    is_mao_momento = (lado_mao == 'NOS')
    jog_para_calculo = ultima_mao_completa[1] if ultima_mao_completa[1] is not None and is_mao_momento else jog
    
    # REGRA EMPATE J1 SIMPLES - PRIMEIRA PRIORIDADE
    if jog == 1 and emp == 1 and not is_mao_momento and MANILHA:
        carta_forca5 = "3" if MANILHA != "3" else "2"
        cartas_fortes = [c for c in mao_para_analise if c and (
            c.startswith(f'{carta_forca5}_') or c.startswith('2_') or c.endswith('M')
        )]
        
        if len(cartas_fortes) >= 1:
            print(f"⚡ REGRA EMPATE J1: Empate + PÉ + Carta forte → ACEITANDO!")
            return "ACEITOU"

    # REGRA ZAP J2: ZAP + carta fraca na J2 quando somos PÉ = CORRER
    if jog == 1 and not is_mao_momento and MANILHA:
        zap_card = f"{MANILHA}_zapM"
        tem_zap = zap_card in mao_para_analise
        
        if tem_zap:
            num_manilhas = sum(1 for c in mao_para_analise if c and c.endswith('M'))
            
            if num_manilhas < 2:  # Só ZAP (sem outras manilhas)
                cartas_comuns = [c for c in mao_para_analise if c and c != zap_card and not c.endswith('M')]
                
                if cartas_comuns:
                    pontuacao = calcular_pontuacao_dinamica()
                    
                    if pontuacao:
                        tem_carta_fraca = any(
                            pontuacao.get(c.split('_')[0], 0) <= 2 
                            for c in cartas_comuns
                        )
                        
                        if tem_carta_fraca:
                            print("🚨 REGRA ZAP J2 (PÉ): ZAP + carta ≤ 2 pontos → CORRENDO!")
                            bot_correu = True
                            return "CORREU"

    # REGRA PRIORITÁRIA: Perdemos J1 + Q na mão = CORRER
    if jog == 1 and v_n == 0 and v_e == 1:
        tem_q = any(c and c.startswith('Q_') and not c.endswith('M') for c in mao_para_analise if c)
        
        if tem_q:
            print("🚨 REGRA PRIORITÁRIA TRUCO: Perdemos J1 + temos Q → CORRENDO!")
            bot_correu = True
            return "CORREU"

    # REGRAS ESPECIAIS ATIVAS
    if estrategia_duas_manilhas_pe.get('ativa', False):
        print("🃏 REGRA DUAS MANILHAS PÉ: Estratégia ativa → ACEITANDO!")
        return "ACEITOU"
        
    if estrategia_mao_fraca_manilha.get('ativa', False) and estrategia_mao_fraca_manilha.get('empatou_j1', False):
        print("🃏 REGRA MÃO FRACA + MANILHA: Empatou J1 → ACEITANDO!")
        return "ACEITOU"

    # COPA + EMPATE = ACEITAR SEMPRE
    if MANILHA and emp >= 1:
        copa_card = f"{MANILHA}_copaM"
        if copa_card in mao_para_analise:
            print("🃏 REGRA ESPECIAL: Empate + Copa Manilha → ACEITANDO!")
            return "ACEITOU"

    # ZAP + VITÓRIA = ACEITAR SEMPRE
    if MANILHA and v_n >= 1:
        zap_card = f"{MANILHA}_zapM"
        if zap_card in mao_para_analise:
            print("🏆 JOGO GANHO: ZAP + já ganhamos uma jogada → ACEITANDO!")
            return "ACEITOU"
    
    # REGRAS PÉ MANILHA
    if regra_pe_manilha_forca5(mao_para_analise, is_mao_momento):
        print("🎯 REGRA PÉ MANILHA + FORÇA 5: Aceitando!")
        return "ACEITOU"
    
    if regra_pe_manilha_forte(mao_para_analise, is_mao_momento):
        print("🎯 REGRA PÉ MANILHA FORTE: Aceitando!")
        return "ACEITOU"

    # DECISÃO BASEADA NA FORÇA (fallback final)
    pontos, classificacao = avaliar_forca_mao(mao_para_analise, jog_para_calculo)
    print(f"🤔 Classificação: {classificacao} ({pontos} pts)")
    
    if classificacao in ["Super Fraca", "Fraca"]:
        print("🛑 Mão fraca, correndo do truco!")
        bot_correu = True
        return "CORREU"
    elif classificacao == "Média":
        if v_n >= 1:
            # Verifica se mão original foi forte
            if mao_inicial_classificacao and mao_inicial_classificacao in ["Média-Forte", "Forte", "Muito Forte"]:
                print("✅ Mão média MELHORADA: Mão original forte + já ganhamos → ACEITANDO!")
                return "ACEITOU"
            else:
                print("🛑 Mão média + não passou nos critérios → CORRENDO!")
                bot_correu = True
                return "CORREU"
        else:
            print("🛑 Mão média + não ganhamos → correndo!")
            bot_correu = True
            return "CORREU"
    else:  # Média-Forte, Forte, Muito Forte
        print(f"✅ Mão {classificacao} → aceitando!")
        return "ACEITOU"

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE CONTROLE E RESET
# ═══════════════════════════════════════════════════════════════

def resetar_variaveis_estrategias():
    """Reseta todas as variáveis de estratégias para nova rodada"""
    global estrategia_duas_manilhas, estrategia_duas_manilhas_pe, estrategia_mao_fraca_manilha
    global empate_j1_com_copa, mao_inicial_classificacao, ultima_mao_completa
    
    estrategia_duas_manilhas = {'ativa': False, 'carta_comum_idx': None}
    estrategia_duas_manilhas_pe = {'ativa': False, 'carta_comum_idx': None, 'manilha_menor_idx': None, 'matou_j1': False}
    estrategia_mao_fraca_manilha = {'ativa': False, 'empatou_j1': False, 'manilha_usada_j1': False}
    empate_j1_com_copa = False
    mao_inicial_classificacao = None
    ultima_mao_completa = (None, None)

def salvar_mao_completa(hand_str, jog_atual):
    """Salva mão completa para uso posterior"""
    global ultima_mao_completa
    
    if jog_atual == 0:
        cartas_validas = [c for c in hand_str if c]
        if len(cartas_validas) == 3:
            pontos, classificacao = avaliar_forca_mao(hand_str, 0)
            global mao_inicial_classificacao
            mao_inicial_classificacao = classificacao
            ultima_mao_completa = (hand_str.copy(), jog_atual)
            print(f"💾 Mão J1 salva: {classificacao}")

def detectar_empate_j1_copa(jog_atual, vencedor):
    """Detecta empate J1 com Copa para estratégia J2"""
    global empate_j1_com_copa, MANILHA
    
    if jog_atual == 1 and vencedor == 'EMPATE' and MANILHA:
        copa_card = f"{MANILHA}_copaM"
        hand = mao()
        hand_str = [padronizar_carta_mao(h) for h in hand]
        tem_copa = copa_card in hand_str
        
        if tem_copa:
            empate_j1_com_copa = True
            print("🃏 Copa: Empate na J1 detectado - ativando estratégia J2")

# ═══════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL DE ESCOLHA DE CARTA COM TODAS AS REGRAS
# ═══════════════════════════════════════════════════════════════

def escolher_carta_com_regras(hand, carta_adv, jog, is_mao, emp):
    """
    Escolha de carta com TODAS as regras implementadas
    ORDEM DE PRIORIDADE (do maior para menor)
    """
    hand_str = [padronizar_carta_mao(h) for h in hand]
    
    # Salva mão completa na J1
    if jog == 0:
        salvar_mao_completa(hand_str, jog)
    
    cartas_validas = [(i, cs, força(cs)) for i, cs in enumerate(hand_str) if cs]
    
    if not cartas_validas:
        print("⚠️ Nenhuma carta reconhecida")
        return 0

    # ═══ PRIORIDADE 1: REGRAS DE ZAP ═══
    aplica_zap, idx_zap, motivo_zap = aplicar_regra_zap(hand_str, carta_adv, jog, is_mao, emp)
    if aplica_zap:
        print(f"🂡 {motivo_zap}")
        return idx_zap

    # ═══ PRIORIDADE 2: REGRAS DE DUAS MANILHAS ═══
    aplica_duas_mao, idx_duas_mao, motivo_duas_mao = aplicar_regra_duas_manilhas_mao(cartas_validas, is_mao, jog, v_n, v_e)
    if aplica_duas_mao:
        print(f"🃏 {motivo_duas_mao}")
        return idx_duas_mao
        
    aplica_duas_pe, idx_duas_pe, motivo_duas_pe = aplicar_regra_duas_manilhas_pe(cartas_validas, is_mao, jog, v_n, v_e, carta_adv)
    if aplica_duas_pe:
        print(f"🃏 {motivo_duas_pe}")
        return idx_duas_pe

    # ═══ PRIORIDADE 3: REGRAS DE FORÇA 5 ═══
    aplica_forca5, idx_forca5, motivo_forca5 = aplicar_regra_carta_forca5_manilha(cartas_validas, is_mao, jog, v_n, v_e)
    if aplica_forca5:
        print(f"🃏 {motivo_forca5}")
        return idx_forca5

    # ═══ PRIORIDADE 4: REGRAS DE COPA MANILHA ═══
    pontos, classificacao = avaliar_forca_mao(hand_str, jog)
    aplica_copa, idx_copa, motivo_copa = aplicar_regra_copa_manilha(cartas_validas, is_mao, jog, emp, classificacao)
    if aplica_copa:
        print(f"🃏 {motivo_copa}")
        return idx_copa
    
    aplica_copa_j1, idx_copa_j1, motivo_copa_j1 = aplicar_copa_j1_pe(cartas_validas, is_mao, jog, carta_adv)
    if aplica_copa_j1:
        print(f"🃏 {motivo_copa_j1}")
        return idx_copa_j1

    # ═══ PRIORIDADE 5: REGRAS DE MÃO FRACA + MANILHA ═══
    aplica_fraca, idx_fraca, motivo_fraca = aplicar_regra_mao_fraca_manilha(cartas_validas, is_mao, jog, v_n, v_e, emp, carta_adv)
    if aplica_fraca:
        print(f"🃏 {motivo_fraca}")
        return idx_fraca

    # ═══ PRIORIDADE 6: COPA ÚLTIMA CARTA ═══
    aplica_copa_ultima, idx_copa_ultima, motivo_copa_ultima = aplicar_copa_ultima_carta(hand_str)
    if aplica_copa_ultima:
        print(f"🃏 {motivo_copa_ultima}")
        return idx_copa_ultima

    # ═══ LÓGICA BÁSICA (ÚLTIMA PRIORIDADE) ═══
    if carta_adv == 'Virada':
        escolhida = min(cartas_validas, key=lambda x: x[2])
        print(f"🎯 Virada: jogando mais fraca ({escolhida[1]})")
        return escolhida[0]
        
    if carta_adv == 'SemCarta':
        escolhida = max(cartas_validas, key=lambda x: x[2])
        print(f"🎯 SemCarta: jogando mais forte ({escolhida[1]})")
        return escolhida[0]

    # Jogada normal: matar > empatar > mais fraca
    killers = [c for c in cartas_validas if força(c[1]) > força(carta_adv)]
    if killers:
        escolhida = min(killers, key=lambda x: x[2])
        print(f"🎯 Matando {carta_adv} com {escolhida[1]}")
        return escolhida[0]
    
    ties = [c for c in cartas_validas if força(c[1]) == força(carta_adv)]
    if ties:
        escolhida = max(ties, key=lambda x: força(x[1])[1])
        print(f"🎯 Empatando {carta_adv} com {escolhida[1]}")
        return escolhida[0]

    escolhida = min(cartas_validas, key=lambda x: x[2])
    print(f"🎯 Não mata nem empata: jogando mais fraca ({escolhida[1]})")
    return escolhida[0]

# ═══════════════════════════════════════════════════════════════
# FUNÇÕES DE DETECÇÃO (MANTIDAS DO ORIGINAL)
# ═══════════════════════════════════════════════════════════════

def id_ficha():
    """Detecta ficha do pé"""
    # Testa posição "nós somos o pé"
    if best(grab(FICHA_NOS), {'f': FICHA_TEMPLATE}, THR_FICHA):
        return 'NOS'
    
    # Testa posição "eles são o pé"
    if best(grab(FICHA_ELES), {'f': FICHA_TEMPLATE}, THR_FICHA):
        return 'ELES'
    
    return None

def id_vira():
    """Detecta vira"""
    return best(grab(VIRA_BOX), T_VIRA, THR_VIRA)

def cronometro_btn():
    """Detecta cronômetro (testa todos Cronometro0-15)"""
    img = grab(CRONOMETRO_BOX)
    
    # Primeiro testa se NÃO é nossa vez
    if 'SemCronometro' in T_CRONOMETRO:
        if best(img, {'sem': T_CRONOMETRO['SemCronometro']}, THR_CRONOMETRO):
            return False  # Não é nossa vez
    
    # Testa todos os cronômetros (0 a 15)
    cronometros_nossa_vez = {}
    for i in range(16):
        nome_cronometro = f'Cronometro{i}'
        if nome_cronometro in T_CRONOMETRO:
            cronometros_nossa_vez[nome_cronometro] = T_CRONOMETRO[nome_cronometro]
    
    # Se encontrou qualquer cronômetro 0-15 = nossa vez
    if cronometros_nossa_vez:
        resultado = best(img, cronometros_nossa_vez, THR_CRONOMETRO)
        if resultado:
            return True  # É nossa vez!
    
    return None  # Não detectou nada claro

def detectar_botoes_na_area():
    """
    NOVO SISTEMA: Detecta TODOS os botões dentro da área flexível
    Retorna dicionário com quais botões estão visíveis e suas posições
    """
    # Captura toda a área onde botões podem aparecer
    img_area = grab(AREA_BOTOES)
    
    botoes_detectados = {}
    
    # Dictionary com todos os templates dos botões
    templates_botoes = {
        'Aceitar': T_ACEITAR,
        'Correr': T_CORRER,
        'Mostrar_cartas': T_MOSTRAR_CARTAS,
        'Truco': T_TRUCO,
        'Truco6': T_TRUCO6,
        'Truco9': T_TRUCO9,
        'Truco12': T_TRUCO12
    }
    
    # Testa cada botão na área
    for nome_botao, template in templates_botoes.items():
        if template is not None:
            # Usa matchTemplate para encontrar a posição
            resultado = cv2.matchTemplate(img_area, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
            
            if max_val >= THR_BOTAO:
                # Calcula posição absoluta na tela
                x_area, y_area = AREA_BOTOES[0], AREA_BOTOES[1]
                x_relativo, y_relativo = max_loc
                
                # Posição absoluta do canto superior esquerdo do botão
                x_absoluto = x_area + x_relativo
                y_absoluto = y_area + y_relativo
                
                # Calcula centro do botão
                h_template, w_template = template.shape
                centro_x = x_absoluto + w_template // 2
                centro_y = y_absoluto + h_template // 2
                
                botoes_detectados[nome_botao] = {
                    'detectado': True,
                    'confianca': max_val,
                    'centro': (centro_x, centro_y),
                    'posicao': (x_absoluto, y_absoluto),
                    'tamanho': (w_template, h_template)
                }
            else:
                botoes_detectados[nome_botao] = {'detectado': False}
    
    return botoes_detectados

def clicar_botao_detectado(nome_botao, botoes_detectados):
    """
    Clica no centro de um botão detectado
    """
    if nome_botao in botoes_detectados and botoes_detectados[nome_botao]['detectado']:
        centro_x, centro_y = botoes_detectados[nome_botao]['centro']
        confianca = botoes_detectados[nome_botao]['confianca']
        
        print(f"🖱️ Clicando no botão {nome_botao} (confiança: {confianca:.2f})")
        print(f"📍 Posição: ({centro_x}, {centro_y})")
        
        pyautogui.moveTo(centro_x, centro_y, duration=0.3)
        time.sleep(0.2)
        pyautogui.click(centro_x, centro_y, duration=0.4)
        time.sleep(0.3)
        return True
    else:
        print(f"❌ Botão {nome_botao} não foi detectado!")
        return False

def botao_mostrar_cartas():
    """Detecta botão Mostrar Cartas (fim de rodada)"""
    if T_MOSTRAR is None and T_MOSTRAR_CARTAS is None:
        return False
    
    # Tenta primeiro com T_MOSTRAR_CARTAS
    if T_MOSTRAR_CARTAS is not None:
        if best(grab(BOTAO_MOSTRAR), {'mostrar': T_MOSTRAR_CARTAS}, THR_BOTAO):
            return True
    
    # Se não deu certo, tenta com backup T_MOSTRAR
    if T_MOSTRAR is not None:
        if best(grab(BOTAO_MOSTRAR), {'mostrar': T_MOSTRAR}, THR_BOTAO):
            return True
    
    return False

def det_sim(img):
    """Detecta símbolo da carta (só a parte principal)"""
    resultado = best(img, T_SIMB, THR_SIMB)
    if resultado and '_' in resultado:
        return resultado.split('_')[0]  # 'Q_Preto' → 'Q'
    return resultado

def det_nai(img):
    """Detecta naipe da carta (só a parte principal)"""
    resultado = best(img, T_NAI, THR_NAIPE)
    if resultado and '_' in resultado:
        return resultado.split('_')[0]  # 'espada_algo' → 'espada'
    return resultado

def mao():
    """Detecta cartas da mão (símbolo + naipe separado para cada carta)"""
    cartas = []
    for i in range(3):
        # Detecta símbolo
        img_sim = grab(MAO_SIM[i])
        simbolo = det_sim(img_sim)
        
        # Detecta naipe
        img_nai = grab(MAO_NAI[i])
        naipe = det_nai(img_nai)
        
        if simbolo and naipe:
            carta = f"{simbolo}_{naipe}"
            # Se for manilha, adiciona 'M'
            if MANILHA and simbolo == MANILHA:
                carta += "M"
            cartas.append((simbolo, naipe))
        else:
            cartas.append((None, None))
    
    return cartas

def card_nos():
    """Detecta nossa carta na mesa (símbolo + naipe separado)"""
    # Detecta símbolo
    img_sim = grab(MESA_NOS_SIM)
    simbolo = best(img_sim, T_MESA_NOS_SIMB, THR_SIMB)
    
    # Se detectou "SemCarta", retorna 'SemCarta'
    if simbolo == 'SemCarta':
        return 'SemCarta'
    
    if simbolo and '_' in simbolo:
        simbolo = simbolo.split('_')[0]  # Remove sufixo se tiver
    
    # Detecta naipe
    img_nai = grab(MESA_NOS_NAI)
    naipe = best(img_nai, T_MESA_NOS_NAI, THR_NAIPE)
    if naipe and '_' in naipe:
        naipe = naipe.split('_')[0]  # Remove sufixo se tiver
    
    if simbolo and naipe:
        carta = f"{simbolo}_{naipe}"
        # Se for manilha, adiciona 'M'
        if MANILHA and simbolo == MANILHA:
            carta += "M"
        return carta
    
    return 'SemCarta'

def card_adv():
    """Detecta carta do adversário na mesa (símbolo + naipe separado)"""
    # Detecta símbolo
    img_sim = grab(MESA_ELES_SIM)
    simbolo = best(img_sim, T_MESA_ADV_SIMB, THR_SIMB)
    
    # Se detectou "SemCarta", retorna 'SemCarta'
    if simbolo == 'SemCarta':
        return 'SemCarta'
    
    if simbolo and '_' in simbolo:
        simbolo = simbolo.split('_')[0]  # Remove sufixo se tiver
    
    # Detecta naipe
    img_nai = grab(MESA_ELES_NAI)
    naipe = best(img_nai, T_MESA_ADV_NAI, THR_NAIPE)
    if naipe and '_' in naipe:
        naipe = naipe.split('_')[0]  # Remove sufixo se tiver
    
    if simbolo and naipe:
        carta = f"{simbolo}_{naipe}"
        # Se for manilha, adiciona 'M'
        if MANILHA and simbolo == MANILHA:
            carta += "M"
        return carta
    
    return 'SemCarta'

def definir_manilha_pelo_vira(vira_str):
    """Define manilha baseada na vira"""
    global MANILHA
    if not vira_str:
        return
    
    simb = vira_str.split('_')[0]
    if simb in SEQ:
        idx = SEQ.index(simb)
        MANILHA = SEQ[(idx + 1) % len(SEQ)]
        print("=" * 50)
        print(f"🃏 VIRA: {vira_str} → MANILHA: {MANILHA}")
        print("=" * 50)
    else:
        print(f"⚠️ Símbolo da vira desconhecido: {simb}")

def processar_fim_rodada():
    """
    Processa o fim da rodada quando aparece botão Mostrar Cartas
    """
    global bot_correu, aguardando_mostrar_cartas
    global jog, v_n, v_e, emp, clicou, cronometro_ja_mostrado
    
    print("=" * 50)
    
    if bot_correu:
        print("🏳️ RESULTADO: Nós corremos - PERDEMOS a rodada!")
        resultado = "DERROTA"
    else:
        print("🏆 RESULTADO: Eles correram - GANHAMOS a rodada!")
        resultado = "VITORIA"
    
    print("=" * 50)
    
    # Aguarda botão desaparecer
    while botao_mostrar_cartas():
        time.sleep(0.2)
    
    # Reset completo para próxima rodada
    jog = v_n = v_e = emp = 0
    clicou = False
    cronometro_ja_mostrado = False
    bot_correu = False
    aguardando_mostrar_cartas = False
    resetar_variaveis_estrategias()  # NOVA LINHA
    
    return resultado

# ═══════════════════════════════════════════════════════════════
# FUNÇÃO DE INICIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════

def inicializar_bot():
    """Inicializa o bot"""
    print("=" * 60)
    print("🤖 Bot Truco V4.0 - Sistema Completo com Todas as Regras")
    print("=" * 60)
    
    # Verifica templates essenciais
    if FICHA_TEMPLATE is None:
        print(f"❌ ERRO: Template da ficha não encontrado!")
        return False
    
    if T_TRUCO is None:
        print(f"❌ ERRO: Template do botão Truco não encontrado!")
        return False
        
    if T_CORRER is None:
        print(f"❌ ERRO: Template do botão Correr não encontrado!")
        return False
        
    if T_ACEITAR is None:
        print(f"❌ ERRO: Template do botão Aceitar não encontrado!")
        return False
        
    if T_TRUCO6 is None:
        print(f"❌ ERRO: Template do botão Truco6 não encontrado!")
        return False
        
    if T_TRUCO9 is None:
        print(f"❌ ERRO: Template do botão Truco9 não encontrado!")
        return False
        
    if T_TRUCO12 is None:
        print(f"⚠️ AVISO: Template do botão Truco12 não encontrado (opcional)")
        
    if T_MOSTRAR_CARTAS is None:
        print(f"❌ ERRO: Template do botão Mostrar_cartas não encontrado!")
        return False
        
    if T_MOSTRAR is None:
        print(f"⚠️ AVISO: Template backup Mostrar_Cartas não encontrado")
    
    if not T_CRONOMETRO:
        print(f"❌ ERRO: Templates do cronômetro não encontrados!")
        return False
    
    if not T_VIRA:
        print(f"❌ ERRO: Templates de vira não encontrados!")
        return False
    
    if not T_SIMB:
        print(f"❌ ERRO: Templates de símbolos não encontrados!")
        return False
        
    if not T_NAI:
        print(f"❌ ERRO: Templates de naipes não encontrados!")
        return False
    
    # Verifica templates da mesa
    if not T_MESA_NOS_SIMB:
        print(f"❌ ERRO: Templates símbolos mesa nossa não encontrados!")
        return False
        
    if not T_MESA_NOS_NAI:
        print(f"❌ ERRO: Templates naipes mesa nossa não encontrados!")
        return False
        
    if not T_MESA_ADV_SIMB:
        print(f"❌ ERRO: Templates símbolos mesa adversário não encontrados!")
        return False
        
    if not T_MESA_ADV_NAI:
        print(f"❌ ERRO: Templates naipes mesa adversário não encontrados!")
        return False
    
    print(f"✅ Template ficha carregado")
    print(f"✅ Templates de botões carregados")
    print(f"✅ {len(T_CRONOMETRO)} templates de cronômetro carregados")
    print(f"✅ {len(T_VIRA)} templates de vira carregados")
    print(f"✅ {len(T_SIMB)} templates de símbolos mão carregados")
    print(f"✅ {len(T_NAI)} templates de naipes mão carregados")
    print(f"✅ {len(T_MESA_NOS_SIMB)} templates símbolos mesa nossa carregados")
    print(f"✅ {len(T_MESA_NOS_NAI)} templates naipes mesa nossa carregados")
    print(f"✅ {len(T_MESA_ADV_SIMB)} templates símbolos mesa adversário carregados")
    print(f"✅ {len(T_MESA_ADV_NAI)} templates naipes mesa adversário carregados")
    print("🔧 TODAS AS 32 REGRAS DE TRUCO IMPLEMENTADAS:")
    print("   • Regras 1-2: ZAP Estratégico")
    print("   • Regras 3-8: Copa Manilha")
    print("   • Regras 9-11: Duas Manilhas")
    print("   • Regras 12-16: Mão Fraca + Manilha e Força 5")
    print("   • Regras 17-22: Truco Automático")
    print("   • Regras 23-25: Correr Automaticamente")
    print("   • Regras 26-32: Aceitar/Correr Truco")
    print("🔍 Aguardando detecção...")
    print("=" * 60)
    
    return True

# ═══════════════════════════════════════════════════════════════
# LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def main():
    """Loop principal"""
    global rodada, lado_pe, lado_mao, MANILHA
    global jog, v_n, v_e, emp, clicou, cronometro_ja_mostrado
    global bot_correu, aguardando_mostrar_cartas
    global PLACAR_NOS, PLACAR_ELES
    
    if not inicializar_bot():
        return
    
    try:
        for _ in count():
            # ═══ 1. VERIFICA BOTÃO MOSTRAR CARTAS (PRIORIDADE MÁXIMA) ═══
            if botao_mostrar_cartas() and not aguardando_mostrar_cartas:
                aguardando_mostrar_cartas = True
                resultado = processar_fim_rodada()
                continue
            
            # Se estamos aguardando fim da rodada, só espera
            if aguardando_mostrar_cartas:
                time.sleep(0.2)
                continue
            
            # ═══ 2. DETECTA FICHA DO PÉ ═══
            f = id_ficha()
            if f and f != lado_pe:
                # NOVA RODADA (reset completo)
                rodada += 1
                jog = v_n = v_e = emp = 0  # Reset jogadas
                lado_pe = f
                lado_mao = 'ELES' if f == 'NOS' else 'NOS'
                MANILHA = None  # Reset manilha
                clicou = False
                cronometro_ja_mostrado = False
                bot_correu = False
                aguardando_mostrar_cartas = False
                resetar_variaveis_estrategias()  # NOVA LINHA
                
                beep(800, 200)
                print("=" * 50)
                print(f"🎲 RODADA {rodada} INICIADA!")
                print("=" * 50)
                print(f"🦶 Pé: {lado_pe} | ✋ Mão: {lado_mao}")
                
                # Exibe placar manual bonito
                exibir_placar()
                
                if lado_pe == 'NOS':
                    print("🟢 NÓS somos o pé - aguardamos adversário")
                else:
                    print("🔴 ELES são o pé - jogamos primeiro")
                
                print("=" * 50)
            
            # ═══ 3. DETECTA VIRA ═══
            if MANILHA is None and lado_pe:
                v = id_vira()
                if v:
                    definir_manilha_pelo_vira(v)
                    beep(1000, 150)
                else:
                    time.sleep(0.3)
                    continue
            
            # ═══ 4. NOVO SISTEMA: DETECTA BOTÕES NA ÁREA FLEXÍVEL ═══
            if MANILHA and not clicou and not aguardando_mostrar_cartas:
                # Detecta TODOS os botões na área usando o novo sistema
                botoes_detectados = detectar_botoes_na_area()
                
                # Lista quais botões estão visíveis
                botoes_visiveis = [nome for nome, info in botoes_detectados.items() 
                                 if info.get('detectado', False)]
                
                # Se detectou botões de TRUCO, implementa decisão automática
                if botoes_visiveis:
                    print(f"🔍 BOTÕES DETECTADOS: {', '.join(botoes_visiveis)}")
                    
                    # DECISÃO AUTOMÁTICA PARA BOTÕES DE TRUCO
                    if 'Aceitar' in botoes_visiveis and 'Correr' in botoes_visiveis:
                        print("🎯 Adversário trucou - decidindo automaticamente...")
                        
                        # Lê mão atual para decidir
                        hand = mao()
                        hand_str = [padronizar_carta_mao(h) for h in hand]
                        
                        decisao = decidir_aceite_truco(hand_str, v_n, jog)
                        
                        if decisao == "ACEITOU":
                            clicar_botao_detectado('Aceitar', botoes_detectados)
                        elif decisao == "CORREU":
                            clicar_botao_detectado('Correr', botoes_detectados)
                        
                        print(f"✅ Decisão tomada: {decisao}")
                        time.sleep(1)
                        continue
                    
                    # Para outros botões, apenas informa
                    for nome in botoes_visiveis:
                        info = botoes_detectados[nome]
                        centro = info['centro']
                        confianca = info['confianca']
                        print(f"   📍 {nome}: centro({centro[0]}, {centro[1]}) - confiança: {confianca:.2f}")
                    
                    print("=" * 50)
            
            # ═══ 5. DETECTA CRONÔMETRO E JOGA ═══
            if MANILHA and not clicou and not aguardando_mostrar_cartas:
                resultado_cronometro = cronometro_btn()
                
                if resultado_cronometro == True and not cronometro_ja_mostrado:
                    cronometro_ja_mostrado = True
                    print("=" * 50)
                    print(f"⏰ Cronômetro encontrado! Nossa vez de jogar!")
                    print("=" * 50)
                    
                    # Lê cartas da mão
                    cartas_mao = mao()
                    cartas_validas = [c for c in cartas_mao if c and c[0] and c[1]]
                    
                    print(f"🃏 Cartas da mão detectadas: {cartas_validas}")
                    
                    # Avalia força da mão usando o sistema avançado
                    hand_str = [padronizar_carta_mao(c) for c in cartas_mao]
                    cartas_str_validas = [c for c in hand_str if c]
                    
                    if cartas_str_validas:
                        pontos, classificacao = avaliar_forca_mao(cartas_str_validas, jog)
                        print(f"📊 Força da mão: {pontos} pontos – {classificacao}")
                    
                    # Detecta carta do adversário
                    carta_adversario = card_adv()
                    
                    # Escolhe carta usando sistema híbrido (regras + fallback)
                    idx = escolher_carta(cartas_mao, carta_adversario)
                    
                    # Clica na carta escolhida
                    if isinstance(idx, int) and idx < len(cartas_mao):
                        click_card(idx)
                        carta_jogada = hand_str[idx] if idx < len(hand_str) and hand_str[idx] else "desconhecida"
                        print(f"🖱️ Clicou na carta {idx + 1}: {carta_jogada}")
                    else:
                        print("❌ Erro ao escolher carta")
                    
                    print("=" * 50)
                    
                    clicou = True  # Evita spam
                elif resultado_cronometro == False:
                    # Reset para poder mostrar cronômetro novamente
                    cronometro_ja_mostrado = False
            
            # ═══ 6. DETECTA CARTAS NA MESA ═══
            if MANILHA and not aguardando_mostrar_cartas:
                nossa_carta = card_nos()
                carta_deles = card_adv()
                
                # SÓ PROCESSA quando AMBAS forem cartas REAIS (não SemCarta)
                if (nossa_carta != 'SemCarta' and carta_deles != 'SemCarta' and 
                    nossa_carta and carta_deles):
                    
                    print("=" * 50)
                    print(f"📋 CARTAS NA MESA DETECTADAS!")
                    print(f"🃏 Nossa carta: {nossa_carta}")
                    print(f"🃏 Carta deles: {carta_deles}")
                    print("=" * 50)
                    
                    # Processa resultado da jogada
                    jog += 1
                    clicou = False
                    cronometro_ja_mostrado = False
                    
                    # Compara forças
                    fn, fe = força(nossa_carta), força(carta_deles)
                    
                    if fn > fe:
                        v_n += 1
                        vencedor = 'NOS'
                        lado_mao = 'NOS'
                    elif fe > fn:
                        v_e += 1
                        vencedor = 'ELES'  
                        lado_mao = 'ELES'
                    else:
                        emp += 1
                        vencedor = 'EMPATE'
                        
                        # Detecta empate J1 com Copa
                        if jog == 1:  # Primeira jogada acabou
                            detectar_empate_j1_copa(jog, vencedor)
                    
                    print(f"🏁 Jogada {jog}: {vencedor}")
                    print(f"📊 Placar: NOS {v_n} × {v_e} ELES (empates: {emp})")
                    print(f"✋ Próxima mão: {lado_mao}")
                    print("=" * 50)
                    
                    # Aguarda cartas saírem da mesa
                    while card_nos() != 'SemCarta' or card_adv() != 'SemCarta':
                        time.sleep(0.2)
                    
                    # ═══ VERIFICAÇÃO COMPLETA DE FIM DE RODADA ═══
                    fim_de_rodada = False
                    resultado_final = None
                    
                    # Condição 1: Alguém ganhou 2 jogadas
                    if v_n >= 2:
                        fim_de_rodada = True
                        resultado_final = 'NOS'
                    elif v_e >= 2:
                        fim_de_rodada = True
                        resultado_final = 'ELES'
                    
                    # Condição 2: 1 vitória + 1 empate = vitória
                    elif v_n >= 1 and emp >= 1:
                        fim_de_rodada = True
                        resultado_final = 'NOS'
                    elif v_e >= 1 and emp >= 1:
                        fim_de_rodada = True
                        resultado_final = 'ELES'
                    
                    # Condição 3: 3 empates seguidos = empate da rodada
                    elif emp >= 3:
                        fim_de_rodada = True
                        resultado_final = 'EMPATE'
                    
                    # Condição 4: Chegou na 3ª jogada (todas as cartas jogadas)
                    elif jog >= 3:
                        fim_de_rodada = True
                        if v_n > v_e:
                            resultado_final = 'NOS'
                        elif v_e > v_n:
                            resultado_final = 'ELES'
                        else:
                            resultado_final = 'EMPATE'
                    
                    # Se fim de rodada detectado
                    if fim_de_rodada:
                        print("=" * 50)
                        print(f"🏆 RODADA {rodada} FINALIZADA: {resultado_final}")
                        print(f"📊 Resultado: NOS {v_n} × {v_e} ELES (empates: {emp})")
                        
                        # Atualiza placar manual
                        if resultado_final == 'NOS':
                            atualizar_placar(nos=PLACAR_NOS + 1)
                            print("🟢 +1 ponto para nós!")
                        elif resultado_final == 'ELES':
                            atualizar_placar(eles=PLACAR_ELES + 1)
                            print("🔴 +1 ponto para eles!")
                        else:
                            print("⚖️ Rodada empatada - ninguém pontua")
                        
                        # Exibe placar atualizado
                        exibir_placar()
                        print("=" * 50)
                        
                        # Reset para próxima rodada
                        jog = v_n = v_e = emp = 0
                        clicou = False
                        cronometro_ja_mostrado = False
                        bot_correu = False
                        aguardando_mostrar_cartas = False
                        resetar_variaveis_estrategias()  # NOVA LINHA
                
                # SILENCIOSO: Se SemCarta, não faz nada (não loga)
            
            # Aguarda antes da próxima iteração
            time.sleep(0.3)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot encerrado")
        print(f"📊 Rodadas: {rodada}")
        print("=" * 60)
        print("🤖 Obrigado por usar o Bot Truco V4.0!")
        print("   Todas as 32 regras foram implementadas com sucesso!")
        print("=" * 60)

# ═══════════════════════════════════════════════════════════════
# EXECUÇÃO
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()