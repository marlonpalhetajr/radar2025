#!/bin/bash
cd "c:\Users\marlon.junior\OneDrive - Fapespa\radar2024"

echo "=== Verificando Status ==="
git status

echo ""
echo "=== Verificando Commits ==="
git log --oneline -3

echo ""
echo "=== Fazendo Push ==="
GIT_TRACE=1 git push -u origin main

echo ""
echo "=== Verificando Remotes ==="
git remote -v
