# Script PowerShell para converter arquivos Excel para HTML - TESTE (apenas Pará)
# Usa o Excel instalado no Windows para manter formatação idêntica

$ErrorActionPreference = "Continue"

# Função para converter Excel para HTML usando Excel COM
function Converter-ExcelParaHTML {
    param(
        [string]$arquivoExcel,
        [string]$arquivoHTMLSaida
    )
    
    try {
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false
        
        Write-Host "    Abrindo Excel..." -ForegroundColor Cyan
        
        $workbook = $excel.Workbooks.Open($arquivoExcel)
        $worksheet = $workbook.Worksheets.Item(1)
        
        # Exporta para HTML direto no destino
        $workbook.SaveAs($arquivoHTMLSaida, 44) # 44 = xlHtml
        
        Write-Host "    Fechando Excel..." -ForegroundColor Cyan
        
        $workbook.Close($false)
        $excel.Quit()
        
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        [System.GC]::Collect()
        [System.GC]::WaitForPendingFinalizers()
        
        if (Test-Path $arquivoHTMLSaida) {
            Write-Host "    ✓ Convertido com sucesso!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "    ❌ Erro: arquivo não foi criado" -ForegroundColor Red
            return $false
        }
        
    } catch {
        Write-Host "    ❌ Erro ao converter: $($_.Exception.Message)" -ForegroundColor Red
        
        # Cleanup em caso de erro
        try {
            if ($workbook) { $workbook.Close($false) }
            if ($excel) { 
                $excel.Quit()
                [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
            }
        } catch { }
        
        return $false
    }
}

# Script principal - APENAS PARÁ
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "TESTE DE ATUALIZAÇÃO - REGIÃO PARÁ" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pastaExcel = Join-Path $baseDir "tabelas-excel\1 Pará"
$pastaHTML = Join-Path $baseDir "tabelas\1-para"

if (-not (Test-Path $pastaExcel)) {
    Write-Host "❌ Pasta Excel não encontrada: $pastaExcel" -ForegroundColor Red
    exit
}

if (-not (Test-Path $pastaHTML)) {
    Write-Host "❌ Pasta HTML não encontrada: $pastaHTML" -ForegroundColor Red
    exit
}

# Pega apenas a Tabela 1 para teste
$arquivoExcel = Get-ChildItem -Path $pastaExcel -Filter "Tabela 1 - *.xlsx" | Select-Object -First 1

if (-not $arquivoExcel) {
    Write-Host "❌ Arquivo Excel 'Tabela 1' não encontrado" -ForegroundColor Red
    exit
}

Write-Host "`nArquivo Excel encontrado:" -ForegroundColor Yellow
Write-Host "  $($arquivoExcel.Name)" -ForegroundColor White

# Encontra arquivo HTML correspondente
$arquivoHTML = Get-ChildItem -Path $pastaHTML -Filter "tabela-1-*.htm" | Select-Object -First 1

if (-not $arquivoHTML) {
    Write-Host "`n❌ Arquivo HTML correspondente não encontrado" -ForegroundColor Red
    exit
}

Write-Host "`nArquivo HTML correspondente:" -ForegroundColor Yellow
Write-Host "  $($arquivoHTML.Name)" -ForegroundColor White

Write-Host "`n" + ("-" * 80) -ForegroundColor Gray
Write-Host "Iniciando conversão..." -ForegroundColor Yellow
Write-Host ("-" * 80) -ForegroundColor Gray

if (Converter-ExcelParaHTML -arquivoExcel $arquivoExcel.FullName -arquivoHTMLSaida $arquivoHTML.FullName) {
    Write-Host "`n" + ("=" * 80) -ForegroundColor Green
    Write-Host "✓ CONVERSÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
    Write-Host ("=" * 80) -ForegroundColor Green
    Write-Host "`nArquivo atualizado:" -ForegroundColor White
    Write-Host "  $($arquivoHTML.FullName)" -ForegroundColor Cyan
    
    # Verifica se criou pasta de arquivos auxiliares
    $pastaAuxiliar = $arquivoHTML.FullName -replace '\.htm$', '_arquivos'
    if (Test-Path $pastaAuxiliar) {
        Write-Host "`nPasta auxiliar criada:" -ForegroundColor White
        Write-Host "  $pastaAuxiliar" -ForegroundColor Gray
    }
} else {
    Write-Host "`n" + ("=" * 80) -ForegroundColor Red
    Write-Host "❌ FALHA NA CONVERSÃO" -ForegroundColor Red
    Write-Host ("=" * 80) -ForegroundColor Red
}

Write-Host "`nPressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
