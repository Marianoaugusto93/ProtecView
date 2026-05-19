# Contratos de integração — Estudos ↔ Relé ↔ Campo

Este documento define os **tipos de dados** que atravessam a suíte Estudos
e suas interfaces com Relé e Campo. A regra-de-ouro: **um estudo nunca é
um silo**. Se um cálculo produz um ajuste, ele expõe esse ajuste num
formato consumível pelas demais suítes.

## 1. `BayContext` — o contexto compartilhado

Estrutura única que descreve o **sistema elétrico em análise**. Persistida
em Zustand global, acessível por todas as ferramentas de Estudos, Relé e
Painel.

```ts
/** Tudo que um estudo precisa saber sobre o sistema antes de calcular. */
export interface BayContext {
  id: string;                        // 'BAY-01'
  name: string;                      // 'Subestação Industrial — BAY-01'

  // ───── Sistema ─────
  nominalVoltage_kV: number;         // 13.8
  frequency_Hz: 50 | 60;             // 60
  systemConnection:                  // tipo de aterramento da fonte
    | 'YN_solid'                     // estrela aterrada
    | 'YN_resistor'                  // estrela com resistor
    | 'YN_reactor'                   // estrela com reator
    | 'D'                            // delta (não aterrada)
    | 'Z';                           // zigzag

  // ───── Fonte ─────
  shortCircuitPower_MVA: number;     // Sₛc = 350
  xOverR: number;                    // 14.5

  // ───── Equipamentos do bay ─────
  ct: {
    ratio: { primary: number; secondary: 1 | 5 };  // 600 / 5
    class: string;                                  // '5P20'
    burden_VA?: number;
    rct_ohms?: number;
  };
  vt?: {
    ratio: { primary: number; secondary: number }; // 13800 / 115
    class: string;                                  // '0.3'
  };

  // ───── Impedâncias da rede (opcional, refinamento) ─────
  z1_ohms?: Complex;                  // sequência positiva
  z2_ohms?: Complex;
  z0_ohms?: Complex;

  // ───── Metadados ─────
  updatedAt: string;                  // ISO 8601
  source: 'manual' | 'rele-import' | 'painel-link' | 'template';
}

export type Complex = { r: number; x: number };   // r + jx em ohms
```

### Onde vive
- **Store:** Zustand slice `useBayStore` (singleton de aplicação).
- **Persistência:** `localStorage` chave `relaylab.bay.current`. Sessão.
- **Multi-bay:** futuro — agora 1 bay ativo por vez.

### Quem lê / quem escreve

| Suíte | Lê | Escreve |
|---|---|---|
| Estudos | sempre | Hub: trocar; Bay editor (lateral): ajustar |
| Relé | sempre | Import de relé real: sobrescreve |
| Campo | sempre (não-editável) | nunca |
| Painel | metadados (nome, Vn) | nunca |

## 2. `StudyArtifact` — o resultado de qualquer ferramenta

Toda ferramenta em Estudos produz **zero ou mais StudyArtifacts**. Um
artifact é a unidade transferível entre ferramentas e entre suítes.

```ts
export type StudyArtifactKind =
  | 'fault-result'
  | 'tcc-curve'
  | 'distance-zones'
  | 'differential-curve'
  | 'inrush-spectrum'
  | 'cable-ampacity'
  | 'ct-saturation'
  | 'symmetrical-components'
  | 'protection-preset';

export interface StudyArtifact<T = unknown> {
  id: string;                        // uuid
  kind: StudyArtifactKind;
  producedBy: string;                // 'estudos/faltas'
  producedAt: string;                // ISO 8601
  bayId: string;                     // ref. a BayContext.id
  label: string;                     // 'Falta 3φ · BAY-01 · 13.8 kV'
  data: T;                           // payload tipado por `kind`
}
```

### Payloads tipados por `kind`

```ts
/** kind: 'fault-result' */
export interface FaultResultPayload {
  faultType: '3ph' | '2ph' | '2ph-T' | '1ph-T';
  faultResistance_ohms: number;
  symmetricCurrent_A: { primary: number; secondary: number };
  peakAsymmetric_kA: number;
  dcDecayTime_ms: { to50: number; to90: number };
  sequenceCurrents: { I1: Complex; I2: Complex; I0: Complex };
  perPhaseCurrent: { a: Complex; b: Complex; c: Complex };
  residualVoltage: { a: Complex; b: Complex; c: Complex };
}

/** kind: 'protection-preset' — o output universal de "Enviar para Relé" */
export interface ProtectionPresetPayload {
  ansiCode: string;                  // '50-1', '51-1', '87T', '21-Z1', ...
  enabled: boolean;
  settings: Record<string, number | string | boolean>;
  // Exemplos por código ANSI:
  //   '50-1':  { pickup_A: 6000, delay_s: 0.05, base: 'primary' }
  //   '51-1':  { pickup_A: 600, timeDial: 0.10, curve: 'IEC-VI', reset: 'instant' }
  //   '21-Z1': { reach_ohms: 4.2, angle_deg: 75, characteristic: 'Mho', delay_s: 0 }
  //   '87T':   { slope1_pct: 30, slope2_pct: 50, breakpoint_pu: 2.0, minPickup_pu: 0.3 }
}

/** kind: 'tcc-curve' */
export interface TccCurvePayload {
  curveFamily: 'IEC' | 'IEEE' | 'ANSI' | 'DefiniteTime' | 'UserDefined';
  curveType: string;                 // 'SI', 'VI', 'EI', 'MI', ...
  pickup_A_primary: number;
  timeDial: number;
  instantaneous?: { pickup_A_primary: number; delay_s: number };
  reset: 'instant' | 'disk';
  userPoints?: Array<{ I: number; t: number }>;
}

// (demais payloads em DATA_MODEL_DETAILS.md — fora do escopo deste hand-off)
```

## 3. Eventos / mensageria entre suítes

A integração Estudos → Relé não é via prop drilling — é via store + evento.

```ts
/** dispara quando o usuário aciona "Enviar para Relé" */
useArtifactBus.publish({
  type: 'artifact.sendToRele',
  artifact: presetArtifact,
});

/** Relé inscreve-se: */
useArtifactBus.subscribe('artifact.sendToRele', (a) => {
  releStore.applyPreset(a.data);
  toast.success(`Preset ${a.data.ansiCode} aplicado em ${a.bayId}`);
  // não navega; usuário decide se vai checar
});
```

Implementação sugerida: **mitt** ou um Zustand store próprio para o bus.

## 4. Fluxos de continuidade (cenários canônicos)

### 4.1. Fluxo "do estudo ao ajuste" (caso de uso primário)
```
1.  Usuário define BayContext em /estudos
2.  Abre /estudos/faltas → roda falta 3φ → obtém Iₛc = 14.64 kA
3.  Clica "Enviar como preset para Relé"
    → StudyArtifact<ProtectionPresetPayload> ('50-1', pickup=Iₛc*1.25)
    → bus publica 'artifact.sendToRele'
4.  Toast aparece; usuário pode navegar para Relé pela topbar
5.  Em Relé, função 50-1 já está pré-preenchida com a sugestão
6.  Usuário ajusta TD, aprova, envia para o equipamento real
```

### 4.2. Fluxo "verificar TC após calcular falta"
```
1.  /estudos/faltas → resultado com Iₛc e X/R
2.  Clica "Abrir em Saturação de TC"
    → navega para /estudos/tc?from=faltas&iSc=14640&xr=14.5
3.  /estudos/tc importa BayContext + Iₛc e X/R como inputs
4.  Resultado: TC OK / alerta
```

### 4.3. Fluxo "do Relé para Estudos"
```
1.  Usuário está em /rele e quer ver curva TCC do ajuste atual
2.  Clica "Abrir em Curvas TCC"
    → /estudos/tcc?from=rele&curve=51-1
3.  Curva chega já plotada; usuário ajusta TD e re-envia para Relé
```

## 5. Versionamento

Esses contratos devem ser **versionados**. Sugestão:

```ts
// no header de cada artifact
schemaVersion: '1.0';
```

Mudança incompatível bump major; compatível bump minor. Relé/Campo lêem
schema e adaptam ou rejeitam com mensagem clara.

## 6. Validação (Zod recomendado)

```ts
import { z } from 'zod';

export const ComplexSchema = z.object({ r: z.number(), x: z.number() });

export const BayContextSchema = z.object({
  id: z.string().min(1),
  name: z.string(),
  nominalVoltage_kV: z.number().positive(),
  frequency_Hz: z.union([z.literal(50), z.literal(60)]),
  systemConnection: z.enum([
    'YN_solid','YN_resistor','YN_reactor','D','Z'
  ]),
  shortCircuitPower_MVA: z.number().positive(),
  xOverR: z.number().positive(),
  // ...
});
```

Validar **na fronteira** — todo artifact que entra no store passa pelo
schema. Erros vão para `console.warn` + toast em dev; em prod, falham silencioso.

## 7. Persistência

| O quê | Onde | TTL |
|---|---|---|
| `BayContext` ativo | localStorage `relaylab.bay.current` | sessão (sem expiração) |
| `BayContext` salvos (templates) | localStorage `relaylab.bay.templates[]` | indefinido |
| Histórico de artifacts | memória + indexedDB `relaylab.artifacts` | 30 dias |
| Recentes do hub | localStorage `relaylab.estudos.recent[]` | 30 dias |

## 8. Privacidade

Nenhum dos dados acima sai do cliente sem ação explícita do usuário
("Exportar JSON"). Não há telemetria de **valores** — apenas eventos de uso
(qual ferramenta foi aberta, quantos artifacts foram criados).
