# Script PowerShell para converter arquivos Excel para HTML
# Usa o Excel instalado no Windows para manter formatação idêntica

$ErrorActionPreference = "Continue"

# Mapeamento de pastas
$mapeamento = @{
    "1 Pará" = "1-para"
    "2 Araguaia" = "2-araguaia"
    "3 Baixo Amazonas" = "3-baixo-amazonas"
    "4 Carajás" = "4-carajas"
    "5 Guajará" = "5-guajara"
    "6 Guamá" = "6-guama"
    "7 Lago de Tucuruí" = "7-lago-de-tucurui"
    "8 Marajó" = "8-marajo"
    "9 Rio Caeté" = "9-rio-caete"
    "10 Rio Capim" = "10-rio-capim"
    "11 Tapajós" = "11-tapajos"
    "12 Tocantins" = "12-tocantins"
    "13 Xingu" = "13-xingu"
}

# Função para normalizar nome do arquivo
function Normalizar-Nome {
    param([string]$nomeExcel)
    
    # Remove extensão
    $nome = $nomeExcel -replace '\.xlsx$', ''
    
    # Remove ano e região do final
    $nome = $nome -replace '[-_\s]+(20\d{2})[\s_-]+.*$', ''
    
    # Converte para minúsculas
    $nome = $nome.ToLower()
    
    # Remove underscores e substitui por espaços
    $nome = $nome -replace '_', ' '
    
    # Remove caracteres especiais
    $nome = $nome -replace '\(km²\)', '(km2)'
    $nome = $nome -replace '[(),]', ''
    
    # Substitui múltiplos espaços por hífen
    $nome = $nome -replace '\s+', '-'
    
    # Remove hífens múltiplos
    $nome = $nome -replace '-+', '-'
    
    # Remove hífen no início/fim
    $nome = $nome.Trim('-')
    
    return $nome
}

# Função para encontrar arquivo HTML correspondente
function Encontrar-ArquivoHTML {
    param(
        [string]$nomeBase,
        [string]$pastaHTML
    )
    
    $arquivos = Get-ChildItem -Path $pastaHTML -Filter "*.htm"
    
    foreach ($arquivo in $arquivos) {
        $nomeHTML = $arquivo.BaseName
        $nomeHTMLBase = $nomeHTML -replace '-20\d{2}-', '-'
        $nomeHTMLBase = $nomeHTMLBase -replace '-para$', ''
        
        if ($nomeBase -match [regex]::Escape($nomeHTMLBase.Substring(0, [Math]::Min(30, $nomeHTMLBase.Length))) -or 
            $nomeHTMLBase -match [regex]::Escape($nomeBase.Substring(0, [Math]::Min(30, $nomeBase.Length)))) {
            return $arquivo.FullName
        }
    }
    
    return $null
}

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
        
        Write-Host "    Abrindo Excel: $([System.IO.Path]::GetFileName($arquivoExcel))" -ForegroundColor Cyan
        
        $workbook = $excel.Workbooks.Open($arquivoExcel)
        $worksheet = $workbook.Worksheets.Item(1)
        
        # Cria arquivo HTML temporário
        $tempHTML = [System.IO.Path]::GetTempFileName() + ".htm"
        
        # Exporta para HTML
        $workbook.SaveAs($tempHTML, 44) # 44 = xlHtml
        
        $workbook.Close($false)
        $excel.Quit()
        
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
        [System.GC]::Collect()
        [System.GC]::WaitForPendingFinalizers()
        
        # Copia arquivo HTML gerado para o destino
        if (Test-Path $tempHTML) {
            Copy-Item -Path $tempHTML -Destination $arquivoHTMLSaida -Force
            Remove-Item -Path $tempHTML -Force
            
            # Remove pasta de arquivos auxiliares gerada pelo Excel
            $pastaAuxiliar = $tempHTML -replace '\.htm$', '_arquivos'
            if (Test-Path $pastaAuxiliar) {
                Remove-Item -Path $pastaAuxiliar -Recurse -Force
            }
            
            Write-Host "    ✓ Convertido com sucesso!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "    ❌ Erro: arquivo temporário não foi criado" -ForegroundColor Red
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
        } catch {}
        
        return $false
    }
}

# Função principal para processar uma região
function Processar-Regiao {
    param(
        [string]$pastaExcel,
        [string]$pastaHTML
    )
    
    $processados = 0
    $erros = 0
    
    $arquivosExcel = Get-ChildItem -Path $pastaExcel -Filter "*.xlsx" | Where-Object { -not $_.Name.StartsWith('~') }
    
    foreach ($arquivo in $arquivosExcel) {
        Write-Host "`n  Processando: $($arquivo.Name)" -ForegroundColor Yellow
        
        # Normaliza nome
        $nomeBase = Normalizar-Nome -nomeExcel $arquivo.Name
        Write-Host "  Nome base: $nomeBase" -ForegroundColor Gray
        
        # Encontra arquivo HTML
        $arquivoHTML = Encontrar-ArquivoHTML -nomeBase $nomeBase -pastaHTML $pastaHTML
        
        if ($arquivoHTML) {
            Write-Host "  Encontrado: $([System.IO.Path]::GetFileName($arquivoHTML))" -ForegroundColor Gray
            
            if (Converter-ExcelParaHTML -arquivoExcel $arquivo.FullName -arquivoHTMLSaida $arquivoHTML) {
                $processados++
            } else {
                $erros++
            }
        } else {
            Write-Host "  ⚠️  Arquivo HTML não encontrado" -ForegroundColor Yellow
            $erros++
        }
    }
    
    return @($processados, $erros)
}

# Script principal
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "ATUALIZAÇÃO DE TABELAS HTML COM DADOS EXCEL" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pastaExcelBase = Join-Path $baseDir "tabelas-excel"
$pastaHTMLBase = Join-Path $baseDir "tabelas"

$totalProcessados = 0
$totalErros = 0

foreach ($regiao in $mapeamento.Keys) {
    Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
    Write-Host "REGIÃO: $regiao" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Cyan
    
    $pastaExcel = Join-Path $pastaExcelBase $regiao
    $pastaHTML = Join-Path $pastaHTMLBase $mapeamento[$regiao]
    
    if (-not (Test-Path $pastaExcel)) {
        Write-Host "⚠️  Pasta Excel não encontrada: $pastaExcel" -ForegroundColor Yellow
        continue
    }
    
    if (-not (Test-Path $pastaHTML)) {
        Write-Host "⚠️  Pasta HTML não encontrada: $pastaHTML" -ForegroundColor Yellow
        continue
    }
    
    $resultado = Processar-Regiao -pastaExcel $pastaExcel -pastaHTML $pastaHTML
    $processados = $resultado[0]
    $erros = $resultado[1]
    
    $totalProcessados += $processados
    $totalErros += $erros
    
    Write-Host "`n  Resumo da região:" -ForegroundColor White
    Write-Host "  ✓ Processados: $processados" -ForegroundColor Green
    Write-Host "  ❌ Erros: $erros" -ForegroundColor Red
}

Write-Host "`n" + ("=" * 80) -ForegroundColor Cyan
Write-Host "RESUMO FINAL" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "Total de arquivos processados: $totalProcessados" -ForegroundColor Green
Write-Host "Total de erros: $totalErros" -ForegroundColor Red
Write-Host "Total geral: $($totalProcessados + $totalErros)" -ForegroundColor White

Write-Host "`nPressione qualquer tecla para sair..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
