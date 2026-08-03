# Nascimento aleatório na Espinha do Mundo

Depois de executar `instalar_espinha.py`, confirme que a entrada de **A Espinha do Mundo** no seu arquivo de regiões usa:

```python
"cena_inicial": "00_despertar_espinha"
```

O instalador tenta fazer isso sozinho e cria um arquivo `.bak_espinha` antes de alterar qualquer código.

Para instalar dentro da pasta `rpg_aetheria`:

```powershell
py caminho\para\espinha-exploracao\instalar_espinha.py
```

Na primeira cena, a opção de exploração livre escolhe aleatoriamente entre Cordilheira Monumental, Vales Profundos e Cavernas Gigantes. Cada deslocamento aceita `norte`, `sul`, `leste` ou `oeste`, avança o tempo e pode revelar recursos, pessoas, rastros, monstros ou transições de bioma.
