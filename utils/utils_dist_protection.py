# Ficheiro: utils/utils_dist_protection.py
# (Com a correção de tipo int() para fuse_rating)

import numpy as np

# --- MÓDULO 11: LÓGICA DE PROTEÇÃO DE DISTRIBUIÇÃO ---

# Constantes para as curvas de fusíveis (baseado em polinómios IEEE C37.42)
FUSE_CURVE_CONSTANTS = {
    'K': {
        'melt': {
            6: [0.3396, -0.045, -2.148, 1.254, -0.252, 0.019],
            10: [0.461, -0.045, -2.148, 1.254, -0.252, 0.019],
            15: [0.606, -0.045, -2.148, 1.254, -0.252, 0.019],
            25: [0.814, -0.045, -2.148, 1.254, -0.252, 0.019],
            40: [1.026, -0.045, -2.148, 1.254, -0.252, 0.019],
            65: [1.328, -0.045, -2.148, 1.254, -0.252, 0.019],
            100: [1.606, -0.045, -2.148, 1.254, -0.252, 0.019],
            140: [1.814, -0.045, -2.148, 1.254, -0.252, 0.019],
            200: [2.126, -0.045, -2.148, 1.254, -0.252, 0.019]
        },
        'clear_adder': {
            6: 0.015, 10: 0.018, 15: 0.022, 25: 0.025, 40: 0.03,
            65: 0.035, 100: 0.04, 140: 0.05, 200: 0.06
        }
    },
    'T': {
        'melt': {
            6: [0.62, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            10: [0.76, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            15: [0.89, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            25: [1.13, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            40: [1.38, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            65: [1.63, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            100: [1.94, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            140: [2.16, -0.0038, -1.75, 0.776, -0.156, 0.0116],
            200: [2.44, -0.0038, -1.75, 0.776, -0.156, 0.0116]
        },
        'clear_adder': {
            6: 0.02, 10: 0.02, 15: 0.025, 25: 0.03, 40: 0.04,
            65: 0.04, 100: 0.05, 140: 0.06, 200: 0.08
        }
    }
}


def calculate_fuse_time(current, fuse_type, fuse_rating):
    """
    Calcula o tempo de fusão (t_melt) e o tempo de eliminação (t_clear) para um fusível.
    Retorna (t_melt, t_clear)
    """
    try:
        # --- [CORREÇÃO AQUI] ---
        # Converte o 'fuse_rating' (que vem como string "40") para um inteiro (40)
        # para que possamos usá-lo como chave na tabela FUSE_CURVE_CONSTANTS
        rating_int = int(fuse_rating)

        # Tenta encontrar as constantes para o tipo e ampacidade
        consts = FUSE_CURVE_CONSTANTS[fuse_type]['melt'][rating_int]
        adder = FUSE_CURVE_CONSTANTS[fuse_type]['clear_adder'][rating_int]
        # --- [FIM DA CORREÇÃO] ---

        # Converte a corrente para log(I)
        log_i = np.log10(current)

        # Calcula log(t_melt) usando o polinómio
        log_t_melt = (consts[0] +
                      consts[1] * log_i +
                      consts[2] * (log_i ** 2) +
                      consts[3] * (log_i ** 3) +
                      consts[4] * (log_i ** 4) +
                      consts[5] * (log_i ** 5))

        # Converte log(t) de volta para t (em segundos)
        t_melt = 10 ** log_t_melt

        # t_clear = t_melt + C
        t_clear = t_melt + adder

        if t_melt < 0:
            return np.inf, np.inf

        return t_melt, t_clear

    except Exception:
        return np.inf, np.inf

# (Iremos adicionar as funções do religador aqui no futuro)