# 🦋 Sistema de Efeito Borboleta

## Filosofia

Cada escolha importante altera o mundo. A mesma **cena** pode ter **múltiplas interpretações** dependendo das decisões passadas do jogador.

Não é necessário criar novas cenas pra cada combinação de flags — a mesma cena **muda seu conteúdo** baseada nas flags do jogador.

## Exemplo Prático

### Uma Cena Normal (SEM Efeito Borboleta)
```json
{
  "id": "encontro_garrick",
  "texto": "Você encontra Garrick",
  "opcoes": [...]
}
```
Garrick é sempre o mesmo. Não importa suas ações anteriores.

### Com Efeito Borboleta
```json
{
  "id": "encontro_garrick",
  "variações": [
    {
      "condicao": {
        "tipo": "AND",
        "items": [
          {"tipo": "tem_flag", "valor": "ajudou_garrick"},
          {"tipo": "nao_tem_flag", "valor": "roubou_caravana"}
        ]
      },
      "texto": "Garrick sorri e te cumprimenta como aliado",
      "opcoes": [...]
    },
    {
      "condicao": {
        "tipo": "AND",
        "items": [
          {"tipo": "tem_flag", "valor": "roubou_caravana"},
          {"tipo": "nao_tem_flag", "valor": "ajudou_garrick"}
        ]
      },
      "texto": "Garrick te reconhece com raiva e te cerca",
      "opcoes": [...]
    },
    {
      "condicao": null,  // padrão - sempre válida
      "texto": "Você caminha sozinho, sem ver Garrick",
      "opcoes": [...]
    }
  ]
}
```

### Como Funciona
1. Quando você entra na cena `encontro_garrick`
2. O engine **verifica suas flags** (ajudou_garrick? roubou_caravana?)
3. **Seleciona a variação correta**
4. Mostra o texto e opções **daquela variação**

**Resultado**: A mesma cena ID, conteúdo completamente diferente.

## Formatos de Condição

### Simples
```json
{"tem_flag": "ajudou_garrick"}
{"nao_tem_flag": "roubou_caravana"}
{"tem_item": "Amuleto"}
{"npc_vivo": "garrick"}
{"npc_morto": "mercador"}
{"raca": "elfo"}
{"reputacao_minima": {"faccao": "caravana", "valor": 50}}
```

### Compostas (AND, OR, NOT)
```json
{
  "tipo": "AND",
  "items": [
    {"tipo": "tem_flag", "valor": "ajudou"},
    {"tipo": "tem_item", "valor": "Artefato"}
  ]
}
```

```json
{
  "tipo": "OR",
  "items": [
    {"tipo": "tem_flag", "valor": "traidor"},
    {"tipo": "npc_morto", "valor": "anciaoeldor"}
  ]
}
```

```json
{
  "tipo": "NOT",
  "items": [
    {"tipo": "tem_flag", "valor": "descobriu_verdade"}
  ]
}
```

## Padrão de Uso Recomendado

1. **Adicione variações quando a história diverge**
   - Se uma escolha importante muda o tom de uma cena futura, use variações
   
2. **Ordem das variações importa**
   - O engine retorna a **primeira** variação que o jogador atende
   - Coloque condições mais específicas ANTES das genéricas
   
3. **Use flags pra marcar decisões**
   - `ajudou_garrick` — o jogador ajudou
   - `roubou_caravana` — o jogador roubou
   - `nao_se_envolveu` — o jogador ignorou

4. **Sempre tenha uma variação padrão**
   - `"condicao": null` ao final — catchall pra quem não se encaixa em nada

## Exemplo de Desenvolvimento

### Passo 1: Cena de Decisão (Stonevale Hub)
```
Garrick oferece trabalho.
- Aceitar → flag "ajudou_garrick"
- Roubar → flag "roubou_caravana"
- Ignorar → (sem flag)
```

### Passo 2: Cenas Posteriores
Qualquer cena que Garrick possa aparecer tem variações:
- Se ajudou: Garrick é aliado
- Se roubou: Garrick é inimigo
- Se ignorou: Garrick não existe pra você

### Passo 3: Finais
O final reflete toda a cascata de escolhas:
- Ajudou muita gente → herói
- Roubou muito → vilão
- Ignorou → neutro

## Combinações Complexas

Uma cena pode ter lógica muito mais elaborada:

```json
{
  "condicao": {
    "tipo": "AND",
    "items": [
      {
        "tipo": "OR",
        "items": [
          {"tipo": "tem_flag", "valor": "traidor"},
          {"tipo": "npc_morto", "valor": "garrick"}
        ]
      },
      {"tipo": "nao_tem_flag", "valor": "se_arrependeu"}
    ]
  },
  "texto": "Você é considerado um inimigo do reino..."
}
```

Tradução: "Se você traiu OU matou Garrick, E não se arrependeu → essa cena aparece"

## Boas Práticas

✅ **Faça**:
- Use flags descritivas: `ajudou_garrick`, não `flag_1`
- Agrupe variações por tema
- Deixe comentários explicando a lógica

❌ **Evite**:
- Não crie 100 cenas que poderiam ser 1 cena com variações
- Não esqueça a variação padrão
- Não anide demais (máximo 2-3 níveis de AND/OR)

## No Código

`engine/condition_system.py` - sistema de condições
`engine/scene_engine.py` - renderização de cenas com variações
