# Pacote de cenas — Frostreach

Copie estes quatro arquivos para `rpg_aetheria/data/scenes/` do projeto:

- `00_despertar_frostreach.json` — substitui o despertar atual.
- `00b_frostreach_abrigo.json` — substitui a cena de abrigo atual.
- `01_stonhelm_hub.json` — substitui o hub atual de Stonhelm.
- `frostreach_expedicao.json` — adiciona 20 cenas novas.

O carregador atual já aceita um arquivo JSON com uma lista de cenas, portanto não é preciso alterar `scene_loader.py`.

O pacote usa somente recursos já suportados pelo motor atual: `texto`, `opcoes`, `destino`, `condicao`, `flag`, `item`, `dano`, `cura`, `reputacao` e `combate`.

## Instalação em um comando

1. Copie a pasta inteira `frostreach-scenes` para dentro de `rpg_aetheria/`.
2. Abra o terminal dentro da pasta `rpg_aetheria/`.
3. Para conferir sem alterar nada, execute:

   ```powershell
   python frostreach-scenes/instalar_cenas_frostreach.py --dry-run
   ```

4. Para instalar tudo de uma vez, execute:

   ```powershell
   python frostreach-scenes/instalar_cenas_frostreach.py
   ```

O instalador valida todos os JSONs, cria um backup dos arquivos que serão substituídos e instala os quatro arquivos na pasta correta.

Após copiar, rode `python main.py` na pasta `rpg_aetheria`. O spawn de Frostreach seguirá para `00_despertar_frostreach` como já acontece em `main.py`.
