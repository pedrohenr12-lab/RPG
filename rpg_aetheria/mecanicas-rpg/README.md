# Mecânicas RPG complexas

Copie a pasta `mecanicas-rpg` para dentro de `rpg_aetheria/`. Abra o PowerShell nessa pasta e execute:

```powershell
py mecanicas-rpg/instalar_mecanicas.py
```

Ele cria backup de `engine/game_state.py` e `engine/scene_engine.py`, adiciona `engine/rpg_systems.py` e habilita testes de d20, tempo, energia, fome, sede, temperatura e XP.

Veja `EXEMPLO_CENA_D20.json` para usar testes em cenas. Regra: `d20 + bônus do atributo >= dificuldade` é sucesso; 1 sempre falha e 20 sempre passa.
