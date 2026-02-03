@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "c:\Users\marlon.junior\OneDrive - Fapespa\radar2024"

echo.
echo ====================================
echo  ENVIANDO PARA GITHUB
echo ====================================
echo.

echo [1/4] Inicializando repositório...
git init

echo [2/4] Configurando remote origin...
git remote add origin https://github.com/marlonpalhetajr/radar2025.git

echo [3/4] Adicionando arquivos...
git add -A

echo [4/4] Fazendo commit...
git commit -m "Initial commit: Radar 2024 - Mapas de Indicadores com correções de associações"

echo.
echo [5/5] Enviando para GitHub (main branch)...
git branch -M main
git push -u origin main

echo.
if errorlevel 1 (
    echo ❌ ERRO ao fazer push!
    echo Verifique a conexão e permissões de acesso.
) else (
    echo ✅ Push realizado com sucesso!
    echo Repositório: https://github.com/marlonpalhetajr/radar2025
)

echo.
pause
