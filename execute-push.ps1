cd "c:\Users\marlon.junior\OneDrive - Fapespa\radar2024"

# Redirecionar saída para arquivo
$logFile = "c:\Users\marlon.junior\OneDrive - Fapespa\radar2024\push-output.log"

Write-Host "Iniciando push..." | Tee-Object -FilePath $logFile

git status | Tee-Object -FilePath $logFile -Append

Write-Host "`n=== ENVIANDO PARA GITHUB ===" | Tee-Object -FilePath $logFile -Append

git push -u origin main 2>&1 | Tee-Object -FilePath $logFile -Append

Write-Host "`n=== FIM DO PUSH ===" | Tee-Object -FilePath $logFile -Append

Write-Host "Resultado salvo em: $logFile"
