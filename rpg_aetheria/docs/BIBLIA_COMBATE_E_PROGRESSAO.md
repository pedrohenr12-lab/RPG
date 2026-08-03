# Aetheria — Bíblia do núcleo de combate e progressão v1

## Escopo implementado

O combate é uma continuação do mundo persistente. Vida, mana, vigor, equipamento,
condições, companheiros, carga de artefato, experiência e resultado sobrevivem ao
autosave. Encontros hostis de fauna deixam de ser resolvidos por um único teste e
abrem a interface de rodadas.

Cada rodada oferece três pontos de ação. Atacar, mover, preparar guarda, esquivar,
recuperar vigor, conjurar, ativar artefato, usar técnica de classe, exigir rendição,
fugir ou render-se competem pelos mesmos pontos. A distância usa quatro faixas
abstratas para manter decisões táticas legíveis sem fingir um tabuleiro inexistente.

Ataques usam D20 e quatro graus de resultado. Defesa define a dificuldade; armadura
reduz dano; perfuração ignora parte da armadura; resistências alteram dano elemental.
O motor registra rolagem, dificuldade, grau, mitigação e consequência. Isso evita que
o jogador veja apenas “acertou/errou” sem entender por quê.

Condições implementadas: Sangramento, Em chamas, Envenenado, Resfriado, Congelado,
Atordoado, Caído, Guarda, Esquiva preparada, Exposto, Silenciado, Imobilizado,
Amedrontado, Marcado, Regeneração, Barreira e Contrafeitiço preparado.

Chefes lendários possuem fases em 65% e 30% de vida. As fases mudam ataque,
velocidade, proteção e número de ações. Companheiros persistentes entram como aliados
e agem segundo sua função. As saídas incluem vitória, fuga, ameaça afastada, captura
não letal, rendição e derrota.

## Progressão

Existem exatamente 40 caminhos: 24 classes de batalha e 16 profissões. Cada caminho
tem três ramos, cada ramo possui cinco nós encadeados. São 600 habilidades no catálogo.
O terceiro nó de cada ramo libera uma técnica ativa e o quinto é o ápice.

Classes de batalha: Guerreiro, Guardião, Berserker, Duelista, Lanceiro, Cavaleiro,
Patrulheiro, Caçador, Arqueiro, Ladino, Assassino, Monge, Mago, Feiticeiro,
Elementalista, Artífice Arcano, Clérigo, Paladino, Druida, Xamã, Necromante,
Invocador, Bardo de Guerra e Ancião.

Profissões: Ferreiro, Armeiro, Alquimista, Herbalista, Curandeiro, Cozinheiro,
Caçador-Coletor, Pescador, Minerador, Lenhador, Engenheiro, Encantador, Cartógrafo,
Mercador, Diplomata e Escriba.

Qualquer raça pode escolher qualquer caminho. A classe cresce com experiência de
combate. A profissão cresce com estudo, coleta, caça, trabalho, ajuda, cartografia,
investigação e sobrevivência. Os bônus comprados já entram nos testes procedurais e
no motor de combate. A tela **Habilidades** permite consultar todos os 40 caminhos,
mas só comprar nós da classe e profissão escolhidas.

## Equipamentos e MySQL

O adaptador usa as colunas do catálogo existente de 260 itens: dano mínimo/máximo,
tipo, defesa, bloqueio, alcance, poder mágico, efeito e intensidade. Cajados comuns
continuam físicos; cajados arcanos gastam mana. O software funciona offline com
perfis iniciais embutidos e usa todo o catálogo quando o MySQL está conectado.

Ao conectar, o aplicativo cria e sincroniza `career_definitions`, `skill_nodes`,
`character_progression` e `combat_history`. São operações idempotentes. Saves antigos
recebem Guerreiro e Caçador-Coletor como padrões, sem perder cenas, itens, relações,
missões ou posição.

## Princípios de referência

- D&D 2024 Basic Rules: iniciativa, rodadas, ações, reações e várias formas de encerrar confronto.
  https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game
- Pathfinder 2E Demo: economia de três ações, reação e graus de sucesso.
  https://downloads.paizo.com/PZOP2DEMOADVE.pdf
- D&D 2024 Classes: identidade de classe e aquisição de características por nível.
  https://www.dndbeyond.com/sources/dnd/br-2024/character-classes
- World of Warcraft Hero Talents: árvores ligadas à fantasia e especialização da classe.
  https://worldofwarcraft.blizzard.com/en-us/news/24038519
- RuneScape Skills: progressão separada de combate, coleta, ofício e suporte pelo uso.
  https://www.runescape.com/game-guide/skills
- GDC, Ghost of Yōtei: variedade de armas, desarme, inimigos e chefes construídos sobre sistemas centrais.
  https://schedule.gdconf.com/session/honing-the-blade-evolving-combat-for-ghost-of-yotei/913736
- GDC, The Outer Worlds 2: enquadramento explícito e iterativo para vida e dano.
  https://schedule.gdconf.com/session/praise-the-architect-and-pass-the-ammunition-health-damage-in-the-outer-worlds-2/913847
