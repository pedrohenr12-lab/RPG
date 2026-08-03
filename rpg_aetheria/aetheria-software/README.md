# Aetheria — aplicativo desktop com Núcleo Persistente v2

Esta versão instala a primeira fundação completa do mundo persistente. Ela não apaga nem substitui `main.py`, as 100 cenas ou os saves existentes. Personagens anteriores são migrados quando o autosave é carregado.

## Núcleo Persistente v2

O aplicativo agora compartilha cinco serviços entre todas as futuras regiões:

- `WorldState`: fatos tipados com valor, origem, certeza, visibilidade e momento;
- `GameClock`: relógio canônico em dias, horas e minutos;
- `ActionResolver`: ações automáticas ou testes com falha crítica, falha, sucesso e sucesso crítico;
- `EventScheduler`: marés, buscas, clima e consequências que acontecem no futuro;
- `QuestEngine`: rumores, missões ativas, etapas, objetivos, resultados e resolução pelo mundo.

A nova página `Diário` mostra missões, fatos conhecidos, eventos pendentes e o histórico da campanha. A tela `Continuar` restaura o JSON completo, incluindo exploração, necessidades, fatos, missões e acontecimentos ainda não resolvidos.

### Missão-piloto

`O barco que voltou sozinho` é a primeira missão ligada ao núcleo. A partir das cenas de Tovin:

1. o desaparecimento começa como rumor;
2. examinar o barco inicia a investigação e agenda a subida da maré;
3. a maré altera as condições mesmo durante a viagem;
4. organizar uma busca faz a vila agir sem esperar pelo jogador;
5. encontrar Tovin registra método, ferimentos e resultado;
6. ignorar o rumor permite que os moradores resolvam a situação por conta própria.

Isso é o molde técnico para converter as demais cenas de Frostreach antes de criar Eldorwood.

## Atualização procedural de Frostreach

O modo livre deixou de usar oito botões fixos. O fluxo atual é:

1. fora de um encontro, o terreno oferece rotas descritas de acordo com o bioma;
2. caminhar, escutar ou examinar pode revelar fauna, flora, rastros, viajantes, povoados, lugares ou perigos;
3. enquanto existe um encontro, os comandos de caminhada desaparecem e dão lugar às decisões daquela situação;
4. observar ou estudar pode revelar uma segunda camada de escolhas;
5. testes D20 pertencem a ações concretas e aplicam dano, recursos, tempo, necessidades, XP, reputação, descobertas e flags;
6. o histórico recente impede que o mesmo encontro seja escolhido repetidamente;
7. espécies válidas para o bioma vêm de `species_biomes` no MySQL, com catálogo local de segurança quando o banco está desligado.

## Ritmo lento e calendário

- ações locais usam minutos: escutar leva 10, examinar 20, procurar água 30 e forragear 60;
- cada ligação entre cenas virou uma jornada percorrida em blocos de 30 ou 60 minutos;
- escolher um destino não abre a próxima cena imediatamente: distância e tempo mínimo precisam ser cumpridos;
- o relógio distingue madrugada, amanhecer, manhã, tarde, entardecer e noite;
- a maior parte da exploração é silenciosa: em uma simulação de 5.000 caminhadas, 93,12% não produziram interrupção;
- há no máximo duas interrupções relevantes por dia em território selvagem;
- depois de oito horas de viagem, cada trecho exige um teste de marcha forçada; depois de vinte horas acordado, o personagem precisa dormir;
- o sono ocupa no mínimo oito horas e fome, sede, energia, frio e distância continuam acumulados;
- as rotas Costa, Planalto e Presas são origens paralelas, não três capítulos colocados em sequência;
- no ritmo normal de oito horas de viagem por dia, a rota mais curta da fase inicial ocupa aproximadamente 33 a 44 dias, conforme o bioma de nascimento.

O documento `frostreach-100-ramificacoes/PLANO_RITMO_LENTO_FROSTREACH.md` registra o modelo narrativo e as referências de regras usadas na revisão.

Para aplicar tudo de uma vez, dê dois cliques em `ATUALIZAR_AETHERIA.bat`. O atualizador valida as 100 cenas, cria backup recuperável da interface anterior e instala o software em `rpg_aetheria/aetheria-software`.

## O que já funciona

- menu principal e navegação lateral;
- conexão configurável com MySQL, sem gravar a senha;
- contadores das tabelas do mundo;
- criação de personagem usando as 15 raças do banco;
- destino inicial aleatório entre as seis regiões;
- leitura das cenas JSON existentes;
- escolhas narrativas em botões;
- exploração livre para norte, sul, leste e oeste;
- D20, energia, fome, sede, temperatura, dia e hora;
- busca de recursos e tentativa de abrigo;
- Codex de regiões, raças, fauna, flora e 260 itens;
- registro do personagem e salvamento automático no MySQL.

## Instalação

1. Copie a pasta inteira `aetheria-software` para dentro de:

```text
C:\Users\Samsung\OneDrive\Área de Trabalho\RPG\rpg_aetheria
```

2. O software cria as tabelas do núcleo automaticamente depois de conectar ao MySQL. Se quiser prepará-las manualmente no Workbench, execute:

```text
aetheria-software\mysql\core_v2.sql
```

Os scripts são idempotentes e não apagam tabelas ou saves existentes.

3. Dê dois cliques em `INSTALAR_DEPENDENCIAS.bat` e espere terminar.

4. Dê dois cliques em `INICIAR_AETHERIA.bat`.

Também é possível usar o PowerShell:

```powershell
cd "C:\Users\Samsung\OneDrive\Área de Trabalho\RPG\rpg_aetheria\aetheria-software"
& C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
& C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe iniciar_software.py
```

## Conectando ao banco

Na tela `MySQL`, use normalmente:

```text
Servidor: 127.0.0.1
Porta: 3306
Usuário: root
Banco: aetheria_rpg
Senha: a senha criada na instalação do MySQL
```

Clique em `TESTAR E CONECTAR`. A senha fica apenas na memória enquanto o aplicativo está aberto. Host, porta, usuário e nome do banco são salvos em `config/database.json`.

Se preferir iniciar já conectado pelo PowerShell:

```powershell
$env:AETHERIA_DB_PASSWORD="SUA_SENHA"
& C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe iniciar_software.py
```

## Arquitetura

```text
aetheria-software/
├── iniciar_software.py
├── requirements.txt
├── mysql/seed_software.sql
└── aetheria_app/
    ├── config.py       caminhos e configuração pública
    ├── database.py     conexão e consultas MySQL
    ├── content.py      cenas, raças e conteúdo local
    ├── models.py       estado da sessão e sobrevivência
    ├── core/           fatos, tempo, ações, eventos e missões
    ├── theme.py        aparência da interface
    └── ui.py           janelas, páginas e botões
```

O próximo passo técnico é aplicar o núcleo às demais linhas narrativas de Frostreach e então migrar o combate tático, mantendo uma única máquina de regras para todas as regiões.
