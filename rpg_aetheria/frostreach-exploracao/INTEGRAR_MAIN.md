# Frostreach — substituição segura

O instalador copia os arquivos antigos conhecidos de Frostreach para:

\`\`\`
data/scenes/backup_frostreach_legacy
\`\`\`

Depois, instala a nova cena inicial e a exploração livre. Confirme que a entrada de Frostreach no arquivo de regiões usa:

\`\`\`python
"cena_inicial": "00_despertar_frostreach"
\`\`\`

Dentro de \`rpg_aetheria\`, execute:

\`\`\`powershell
py .\frostreach-exploracao\instalar_frostreach.py
\`\`\`

