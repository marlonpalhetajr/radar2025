$ErrorActionPreference = "Continue"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "TESTE DE CONVERSAO - TABELA 1 DO PARA" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$baseDir = $PSScriptRoot
$pastaExcel = Join-Path $baseDir "tabelas-excel"
$pastaHTML = Join-Path $baseDir "tabelas"

$arquivoExcel = Get-ChildItem -Path "$pastaExcel\1 Pará" -Filter "Tabela 1 -*.xlsx" | Select-Object -First 1
$arquivoHTML = Get-ChildItem -Path "$pastaHTML\1-para" -Filter "tabela-1-*.htm" | Select-Object -First 1

if (-not $arquivoExcel) {
    Write-Host "ERRO: Arquivo Excel nao encontrado" -ForegroundColor Red
    exit
}

if (-not $arquivoHTML) {
    Write-Host "ERRO: Arquivo HTML nao encontrado" -ForegroundColor Red
    exit
}

Write-Host "`nArquivo Excel:" -ForegroundColor Yellow
Write-Host "  $($arquivoExcel.Name)" -ForegroundColor White

Write-Host "`nArquivo HTML (sera atualizado):" -ForegroundColor Yellow
Write-Host "  $($arquivoHTML.Name)" -ForegroundColor White

Write-Host "`n--------------------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "Iniciando conversao com Microsoft Excel..." -ForegroundColor Yellow
Write-Host "--------------------------------------------------------------------------------" -ForegroundColor Gray

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    Write-Host "`nAbrindo Excel..." -ForegroundColor Cyan
    $workbook = $excel.Workbooks.Open($arquivoExcel.FullName)
    
    Write-Host "Exportando para HTML..." -ForegroundColor Cyan
    $workbook.SaveAs($arquivoHTML.FullName, 44)
    
    Write-Host "Fechando Excel..." -ForegroundColor Cyan
    $workbook.Close($false)
    $excel.Quit()
    
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
    Write-Host "`n================================================================================" -ForegroundColor Green
    Write-Host "CONVERSAO CONCLUIDA COM SUCESSO!" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "`nArquivo atualizado:" -ForegroundColor White
    Write-Host "  $($arquivoHTML.FullName)" -ForegroundColor Cyan
    
} catch {
    Write-Host "`n================================================================================" -ForegroundColor Red
    Write-Host "ERRO NA CONVERSAO" -ForegroundColor Red
    Write-Host "================================================================================" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    
    try {
        if ($excel) { 
            $excel.Quit()
            [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        }
    } catch { }
}

Write-Host "`nPressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")