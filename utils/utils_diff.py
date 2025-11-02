# Ficheiro: utils/utils_diff.py
import numpy as np

def generate_differential_curve(pickup, bp1, slope1, bp2, slope2, unrestrained):
    """
    Calcula os pontos (x, y) para a curva de restrição diferencial
    baseada no modelo de múltiplos breakpoints.

    :param pickup: Corrente de pickup (Idif >)
    :param bp1: Breakpoint 1 (Ir >)
    :param slope1: Inclinação 1 (em %)
    :param bp2: Breakpoint 2 (Ir >)
    :param slope2: Inclinação 2 (em %)
    :param unrestrained: Pickup Não Restrito (Idiff >>)
    :return: Duas listas: (lista_ir, lista_iop)
    """

    try:
        # --- 1. Converter inputs ---
        p = float(pickup)
        b1 = float(bp1)
        s1 = float(slope1) / 100.0  # Converte % para decimal
        b2 = float(bp2)
        s2 = float(slope2) / 100.0  # Converte % para decimal
        unres = float(unrestrained)

        # --- 2. Listas de pontos para o gráfico ---
        list_ir = []  # Eixo X (Restrição)
        list_iop = []  # Eixo Y (Operação)

        # Validação de inputs
        if b1 > b2:
            # Garante que breakpoint 1 é menor que breakpoint 2
            b1, b2 = b2, b1

            # --- Ponto 1: Início (Origem) ---
        list_ir.append(0)
        list_iop.append(p)

        # --- Ponto 2: Fim do Pickup / Início Slope1 ---
        list_ir.append(b1)
        list_iop.append(p)

        # --- Ponto 3: Fim do Slope 1 / Início Slope2 ---
        # Iop no breakpoint 2 = Pickup + (Slope1 * (Ir_bp2 - Ir_bp1))
        iop_at_bp2 = p + (s1 * (b2 - b1))

        # Verifica se o Ponto 3 já atingiu o limite "unrestrained"
        if iop_at_bp2 >= unres:
            # A curva atingiu o limite "unrestrained" durante o Slope 1
            # Precisamos encontrar o 'Ir' onde a linha do Slope 1 cruza 'unres'
            # unres = p + s1 * (Ir_cruzamento - b1)
            # (unres - p) / s1 = Ir_cruzamento - b1
            ir_cross = b1 + (unres - p) / (s1 + 1e-9)  # 1e-9 para evitar divisão por zero

            list_ir.append(ir_cross)
            list_iop.append(unres)
            # Adiciona um ponto final horizontal
            list_ir.append(max(ir_cross, b2) * 1.2)  # Ponto final para plotagem
            list_iop.append(unres)
            return list_ir, list_iop  # A curva termina aqui

        # Se não atingiu, adiciona o Ponto 3 normalmente
        list_ir.append(b2)
        list_iop.append(iop_at_bp2)

        # --- Ponto 4: Interseção do Slope 2 com Unrestrained ---
        # Encontra 'Ir' onde a linha do Slope 2 cruza 'unres'
        # unres = iop_at_bp2 + s2 * (Ir_cruzamento - b2)
        # (unres - iop_at_bp2) / s2 = Ir_cruzamento - b2
        ir_cross_2 = b2 + (unres - iop_at_bp2) / (s2 + 1e-9)

        list_ir.append(ir_cross_2)
        list_iop.append(unres)

        # --- Ponto 5: Linha Horizontal Final ---
        list_ir.append(ir_cross_2 * 1.2)  # Ponto final 20% além
        list_iop.append(unres)

        return list_ir, list_iop

    except Exception as e:
        print(f"Erro ao gerar curva diferencial: {e}")
        return [], []
