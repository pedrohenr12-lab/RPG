# Frostreach — fase inicial com 100 cenas

Este pacote substitui apenas o despertar de Frostreach e adiciona 99 cenas novas. A cena anterior é copiada para uma pasta de backup antes da substituição.

## Conteúdo

- 100 cenas conectadas;
- exatamente 3 escolhas por cena;
- 300 escolhas;
- três rotas de nascimento: costa, tundra e montanhas;
- cinco comunidades;
- quatro companheiros principais;
- missões principais, secundárias e livres;
- moradia permanente, cabana ou vida nômade;
- profissão e foco de habilidades;
- decisões comunitárias, independentes ou solitárias;
- fauna, flora e elementos próprios de Frostreach;
- mistério da Aurora Quebrada, Aldric e Guerra dos Vorath;
- três saídas ao fim da fase: história continental, vida em Frostreach ou exploração livre.

## Continuidade narrativa revisada

- a frase editorial sobre chegar sem memória foi removida das 99 cenas em que se repetia;
- as quebras de parágrafo não aparecem mais como `\n\n` na tela;
- todas as 300 escolhas possuem transição narrativa própria;
- testes D20 possuem transições diferentes para sucesso e falha, totalizando 399 caminhos de entrada;
- a interface usa `texto_continuacao` para não repetir a abertura da cena depois da transição;
- o arco costeiro de Tovin foi reescrito manualmente para manter causa, pista, perigo, resgate e consequência.

## Ritmo e distância revisados

- escolhas locais consomem minutos, não horas inteiras automáticas;
- as 396 ligações internas possuem distância, terreno e tempo mínimo próprios;
- a próxima cena somente aparece quando a jornada correspondente foi realmente percorrida;
- deslocamentos são intercalados por clima, luz, relevo, vegetação comum e fauna distante;
- uma caminhada comum tem cerca de 6,88% de chance de sofrer uma interrupção contextual;
- há limite de duas interrupções relevantes por dia;
- marcha acima de oito horas exige D20 e vigília acima de vinte horas obriga descanso;
- as rotas mais curtas exigem cerca de 272 horas pela Costa, 261 pelo Planalto e 354 pelas Presas;
- considerando oito horas de viagem por dia, são aproximadamente 34, 33 e 44 dias, antes de desvios, descanso, caça, falhas ou exploração livre.

Veja `PLANO_RITMO_LENTO_FROSTREACH.md` para a trajetória completa.

## Instalação

Feche o software caso esteja aberto. Copie a pasta `frostreach-100-ramificacoes` para dentro de `rpg_aetheria`. Depois execute:

```powershell
cd "C:\Users\Samsung\OneDrive\Área de Trabalho\RPG\rpg_aetheria"
& C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe .\frostreach-100-ramificacoes\instalar_frostreach_100.py
```

O terminal e o software desktop leem os mesmos JSONs em `data/scenes`. Se `aetheria-software` estiver dentro do projeto, o instalador também atualiza a interface para processar testes D20, flags, itens, reputação e passagem do tempo. Os módulos antigos são guardados numa pasta de backup.
