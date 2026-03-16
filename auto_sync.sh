#!/bin/bash
# Auto-sync: detecta mudanças e faz commit+push automaticamente
# Uso: ./auto_sync.sh (rodar em terminal separado)

PROJECT_DIR="/home/jtoledo/projects/projetotoclaudecode"
INTERVAL=30  # segundos entre cada verificação

echo "Auto-sync iniciado. Monitorando $PROJECT_DIR a cada ${INTERVAL}s..."
echo "Pressione Ctrl+C para parar."

while true; do
    cd "$PROJECT_DIR"

    # Verifica se há mudanças não commitadas
    if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$TIMESTAMP] Mudanças detectadas. Fazendo commit e push..."

        git add -A
        git commit -m "Auto-sync: $TIMESTAMP"
        git push origin main

        echo "[$TIMESTAMP] Push concluído."
    fi

    sleep "$INTERVAL"
done
