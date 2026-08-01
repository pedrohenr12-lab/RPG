# Aetheria — Motor de RPG de Turnos em Python

## Estrutura de pastas

```
rpg_aetheria/
├── main.py                  # ponto de entrada, roda o laço do jogo
├── engine/                  # o "motor" — código que nunca muda por causa da história
│   ├── game_state.py        # atributos, flags, inventário, reputação
│   ├── scene_loader.py      # lê todos os .json de data/scenes/
│   ├── scene_engine.py      # mostra cena, filtra opções, aplica efeitos
│   ├── combat.py            # sistema de combate por turnos
│   └── race_loader.py       # lê data/characters/races.json
├── data/
│   ├── scenes/               # TODA a história mora aqui, em arquivos .json
│   │   ├── 00_despertar.json
│   │   ├── 00b_vestigio.json
│   │   ├── 00c_encontrado.json
│   │   ├── 01_vila_eldor.json
│   │   ├── 01a_anciao.json
│   │   ├── 01b_taverna.json
│   │   ├── 01c_fazendeiro_lobo.json
│   │   ├── 01c_vitoria.json
│   │   ├── 02_aprendendo_basico.json
│   │   └── 99_finais.json    # cenas finais (podem ficar todas juntas numa lista)
│   ├── characters/
│   │   └── races.json        # atributos e flavor de cada raça jogável
│   └── lore/
│       └── intro_mundo.txt   # texto de contexto do mundo, mostrado antes da criação do personagem
└── saves/                    # reservado para salvar progresso (próximo passo)
```

## Por que essa separação

- **`engine/` nunca deveria precisar mudar** conforme vocês escrevem a história.
  Ele só sabe interpretar o "formato" de uma cena (texto, opções, condições,
  efeitos, destino) — não sabe nada sobre Vael'Tharion, Eldoria ou dragões.
- **`data/scenes/` é onde a história de verdade mora.** Cada arquivo é uma
  cena (ou uma lista de cenas relacionadas, como em `99_finais.json`).
  Adicionar conteúdo novo = criar um arquivo `.json` novo. Não precisa
  tocar em nenhum arquivo `.py`.

## Como rodar

```bash
python3 main.py
```

## Formato de uma cena (JSON)

```json
{
  "id": "01_vila_eldor",
  "texto": "Texto descritivo mostrado ao jogador.",
  "opcoes": [
    {
      "texto": "O que aparece no menu",
      "condicao": { "tem_flag": "algo" },
      "efeitos": [{ "tipo": "flag", "valor": "novo_estado" }],
      "destino": "id_da_proxima_cena"
    }
  ]
}
```

- `condicao` é **opcional**. Se ausente, a opção sempre aparece.
- `efeitos` é **opcional**. Aplicado quando o jogador escolhe essa opção.
- Tipos de condição hoje suportados: `tem_flag`, `nao_tem_flag`, `tem_item`,
  `raca`, `reputacao_minima` (veja `engine/scene_engine.py`).
- Tipos de efeito hoje suportados: `flag`, `remover_flag`, `item`, `dano`,
  `cura`, `reputacao`.
- Uma cena sem `"opcoes"` (ou com lista vazia) é tratada como **fim de jogo**
  — útil para os múltiplos finais.

## Cena de combate

Em vez de `"opcoes"`, uma cena pode ter um bloco `"combate"`:

```json
{
  "id": "01c_fazendeiro_lobo",
  "texto": "...",
  "combate": {
    "inimigo": { "nome": "Lobo Faminto", "vida": 12, "ataque": 3, "defesa": 1 },
    "destino_vitoria": "01c_vitoria",
    "destino_derrota": "fim_derrota"
  }
}
```

## Sistema de raças (já implementado)

- `data/characters/races.json` define, por raça: nome de exibição,
  descrição, atributos iniciais (`vida_max`, `ataque`, `defesa`), uma
  `flag_racial` (adicionada automaticamente ao personagem) e um texto de
  criação exibido só naquela raça.
- `main.py` carrega esse arquivo, mostra as opções e monta o `GameState`
  já com os atributos certos.
- Cenas podem ter opções exclusivas de raça usando
  `"condicao": {"raca": "elfo"}` — exemplos prontos em
  `01_vila_eldor.json` (opções exclusivas de elfo e anão).
- **Para adicionar uma raça nova**: basta acrescentar uma entrada no
  `races.json`. Não precisa mexer em nenhum `.py`.

## Introdução do mundo (já implementada)

- `data/lore/intro_mundo.txt` é um texto puro (não JSON), mostrado antes da
  criação do personagem, com o contexto geral de Aetheria — sem revelar
  nada sobre o vilão ou a ameaça atual. Isso fica só pra ser descoberto
  jogando.
- Pra editar, basta abrir esse `.txt` e reescrever — não precisa mexer no
  código.

## Spawn aleatório por região (já implementado)

- No início de cada partida, `sortear_regiao_inicial()` (em `main.py`)
  sorteia uma das 6 regiões de Eldoria — o jogador não escolhe onde cai
  nesse mundo, só a raça e o nome.
- Cada região tem sua própria cena de despertar (`00_despertar_*.json`) e
  um "hub" inicial equivalente à Vila de Eldor. Frostreach, Blackmarsh e a
  Espinha do Mundo (regiões de dificuldade mais alta) aplicam um pouco de
  dano logo na cena de despertar, dependendo da escolha do jogador —
  refletindo a dificuldade descrita no documento de geografia.
- **Eldorwood é hoje a única região totalmente desenvolvida** (a árvore
  completa da Vila de Eldor). As outras 5 têm só uma cena de despertar +
  um hub curto, convergindo para `fim_demo` — servem de esqueleto pronto
  pra expandir, seguindo exatamente o mesmo padrão de arquivos.
- **Liberdade do jogador**: cada hub inclui uma opção de "seguir sozinho /
  evitar contato com todo mundo" (flag `isolado_no_inicio`), além das
  opções de se envolver com a comunidade local. A ideia é que nem toda
  cena precise empurrar o jogador pro caminho social — vale manter esse
  padrão ao escrever novas cenas.

- **Nova camada de profundidade**: cada opção "social" dos hubs agora leva
  a uma cena própria (puxando o "gancho de magia" daquela região, definido
  no documento de geografia) antes de convergir em `03_sinais_do_mundo` —
  onde os primeiros sinais da ameaça maior (sonhos, fenômenos estranhos)
  aparecem, não importa a região. Dali, `04_decisao_de_caminho` deixa o
  jogador escolher que tipo de postura vai adotar (comunitário,
  investigador, ou ignorar os sinais) — flags que devem influenciar os
  6 finais mais pra frente.

## Sistema de Efeito Borboleta (🦋 Implementado)

**Mudança paradigmática**: em vez de criar novas cenas pra cada combinação de flags, 
**a mesma cena tem múltiplas interpretações** baseadas nas decisões do jogador.

- **Cenas têm "variações"**: cada variação tem condições de entrada, texto próprio e opções próprias.
- **Sem convergência forçada**: escolhas nunca se encontram; caminhos divergem e ficam divergentes.
- Exemplo funcional: `04_encuentro_garrick.json` tem 3 variações:
  - Ajudou Garrick? → Garrick é aliado, propõe missão
  - Roubou de Garrick? → Garrick é inimigo, quer se vingar
  - Ignorou? → Garrick não existe pra você, encontro normal

**Condições compostas suportadas**: AND, OR, NOT
- `{"tipo": "AND", "items": [...]}` — todos devem ser verdadeiros
- `{"tipo": "OR", "items": [...]}` — pelo menos um deve ser verdadeiro  
- `{"tipo": "NOT", "items": [...]}` — deve ser falso

Detalhes completos em `data/lore/EFEITO_BORBOLETA.md`.

## Próximos passos sugeridos (nessa ordem)

1. **Expandir as outras 5 regiões** (Frostreach, Arkanor, Stonevale,
   Blackmarsh, Espinha do Mundo) até o mesmo nível de profundidade que
   Eldorwood já tem — puxando a lore de Aetheria (Nós de Poder, sinais de
   Vael'Tharion, rumores) a partir de onde cada uma parou.
2. **Sistema de save/load** — salvar `estado.to_dict()` como JSON em
   `saves/` e recarregar com `GameState.from_dict()`.
3. **Expandir o combate** — IA de inimigo menos previsível, itens variados,
   habilidades específicas de raça/classe (aproveitando a `flag_racial`
   que já existe em cada personagem).
