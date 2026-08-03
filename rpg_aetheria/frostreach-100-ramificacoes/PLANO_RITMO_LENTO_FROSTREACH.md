# Frostreach — trajetória lenta, livre e espacial

## Diagnóstico da versão anterior

- Uma escolha consumia em média 1,25 hora.
- O fim da fase podia ser alcançado em 21 transições e cerca de 39 horas.
- Todo deslocamento procedural criava obrigatoriamente um encontro.
- Costa, Planalto e Montanha estavam ligados em série, embora devessem ser três nascimentos paralelos.
- A quantidade de acontecimentos por dia fazia Frostreach parecer um corredor temático, não uma região de 38 milhões de km².

## Princípio central

O jogo não deve perguntar apenas “qual evento vem agora?”. Ele precisa simular o intervalo entre eventos: deslocamento, frio, orientação, silêncio, alimentação, escolha de rota, luz disponível, montagem de acampamento e descanso.

Uma cena importante é uma recompensa por explorar, alcançar um lugar, seguir uma pista ou sobreviver tempo suficiente. Ela não aparece automaticamente depois de cada botão.

## Escalas de tempo

| Escala | Unidade | Exemplos |
|---|---:|---|
| Ação local | 5–20 minutos | escutar, examinar pegadas, comer, tratar corte |
| Exploração cuidadosa | 30 minutos | avançar procurando sinais, mapear trecho, seguir pista |
| Viagem normal | 1 hora | deslocamento orientado entre pontos conhecidos |
| Subsistência | 45–120 minutos | procurar água, caçar, colher, construir abrigo |
| Acampamento | 1–3 horas | escolher ponto, montar proteção, acender fogo, cozinhar |
| Sono | 8–11 horas | depende do horário, abrigo, vigia, ferimentos e clima |
| Travessia regional | dias ou semanas | costa, tundra, montanha e rotas entre comunidades |

Após oito horas de marcha no mesmo dia, continuar exige marcha forçada e aumenta exaustão. O relógio nunca salta vários dias sem que o jogador escolha viagem longa, sono ou espera.

## Períodos do dia

- Madrugada: 00:00–05:00 — escuridão, maior frio, fauna noturna.
- Amanhecer: 05:00–08:00 — luz baixa, rastros recentes, preparação do dia.
- Manhã: 08:00–12:00 — melhor visibilidade e deslocamento.
- Tarde: 12:00–17:00 — neve amolece em alguns trechos; vento pode aumentar.
- Entardecer: 17:00–19:00 — decisão entre insistir e acampar.
- Noite: 19:00–00:00 — visão limitada, orientação difícil, fogueiras visíveis à distância.

O jogador pode agir em qualquer período. O sistema altera dificuldade, descrição, fauna possível, temperatura e visibilidade; não bloqueia artificialmente a liberdade.

## Densidade do mundo

Para cada bloco de 30 minutos em território selvagem:

- 70–82%: deslocamento silencioso, clima, relevo ou vegetação comum;
- 10–18%: sinais ambientais — fezes, penas, líquen, pegadas antigas, canto distante;
- 4–8%: situação que interrompe a marcha — risco, criatura próxima, recurso raro ou pista;
- menos de 2%: pessoa em território remoto;
- povoado: somente quando a posição do personagem realmente alcança sua área.

Há limite normal de dois acontecimentos relevantes por dia. Tempestades, perseguições e locais especiais podem quebrar esse limite porque são consequências, não sorteios soltos.

Fauna não significa combate. A maior parte será vista longe, ouvida, rastreada ou evitada. Predadores atacam conforme fome, território, surpresa, vento e comportamento do jogador.

## Três trajetórias iniciais paralelas

### Orla Costeira do Gelo

Sobrevivência em gelo de maré, pesca, cavernas, Aquari, Northarianos e o desaparecimento de Tovin. A rota termina em Brumafiorde ou numa estrada para Stonhelm; não obriga atravessar todo o Planalto.

### Planalto Central

Orientação, manadas, matilhas, tempestades, Renaquieta e rotas de trenó. A rota termina em comunidade, caravana ou chegada solitária a Stonhelm; não obriga subir as Presas.

### Presas de Gelo

Altitude, cavernas, mineração, Glacari, Aureli, Ferrari e Pedravela. A rota termina numa descida para a civilização; não depende de o personagem ter vivido as outras duas origens.

As rotas podem ser visitadas depois, por viagem real de dias ou semanas. Elas não são capítulos automáticos colocados em fila.

## Trajetória narrativa sem calendário obrigatório

Os dias abaixo são referências mínimas, não prazos impostos:

1. Dias 1–3: acordar, proteger-se, descobrir água, alimento e direção.
2. Dias 3–10: aprender o bioma; fauna e flora dominam a experiência.
3. Dias 7–20: encontrar sinais inteligentes; contato com pessoa ou comunidade não é garantido.
4. Dias 12–30: escolher companhia, trabalho, moradia, nomadismo ou isolamento.
5. Dias 20–45: reunir pistas da Aurora Quebrada, caso o jogador queira investigá-la.
6. Dia 35 em diante: história continental disponível, sem encerrar exploração, vida local ou construção pessoal.

Gatilhos dependem de tempo mínimo + distância + pistas + escolhas. Dormir vários dias no mesmo abrigo não substitui investigação; explorar depressa não elimina distâncias.

Na implementação validada, os menores percursos contínuos até o início continental somam aproximadamente 272 horas pela Costa, 261 pelo Planalto e 354 pelas Presas. Em jornadas de oito horas, isso representa cerca de 34, 33 e 44 dias, sem contar desvios, encontros, busca de recursos, sono e falhas.

## Inspiração de regras

- Pathfinder usa intervalos mínimos de dez minutos para exploração e horas ou dias para deslocamentos maiores; também recomenda variar a passagem do tempo e usar detalhes sensoriais.
- A exploração por hexágonos mede travessias em dias, separa viajar de reconhecer uma área e considera terreno ártico difícil ou muito difícil.
- A tabela ártica de encontros faz uma verificação diária rara e metade dos resultados é inofensiva.
- D&D diferencia ritmo rápido, normal e lento; viagem além de oito horas por dia causa risco de exaustão.
- Descanso completo ocupa aproximadamente oito horas.

Fontes:

- https://paizo.com/blog/experience-the-world-in-exploration-mode
- https://2e.aonprd.com/Rules.aspx?ID=3103
- https://2e.aonprd.com/Rules.aspx?ID=2442
- https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game/
- https://www.dndbeyond.com/sources/dnd/br-2024/dms-toolbox
