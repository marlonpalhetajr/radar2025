# Script para fazer push para GitHub
cd "c:\Users\marlon.junior\OneDrive - Fapespa\radar2024"

Write-Host "Configuração do repositório GitHub..." -ForegroundColor Green
Write-Host "URL: https://github.com/marlonpalhetajr/radar2025.git" -ForegroundColor Cyan
Write-Host ""

Write-Host "Status do repositório:" -ForegroundColor Green
git status

Write-Host ""
Write-Host "Iniciando push para main branch..." -ForegroundColor Green
Write-Host ""

$output = git push -u origin main 2>&1
Write-Host $output

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "Repositório: https://github.com/marlonpalhetajr/radar2025" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️ Erro ao fazer push. Código: $LASTEXITCODE" -ForegroundColor Yellow
}
