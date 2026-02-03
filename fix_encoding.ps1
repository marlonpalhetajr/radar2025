$path = "c:\Users\marlon.junior\OneDrive - Fapespa\radar2024\project.html"
$content = Get-Content $path -Raw -Encoding UTF8

$content = $content.Replace('PopulaÃ§Ã£o','População')
$content = $content.Replace('RegiÃµes','Regiões')  
$content = $content.Replace('IntegraÃ§Ã£o','Integração')
$content = $content.Replace('ParÃ¡','Pará')
$content = $content.Replace('SÃ©ries','Séries')
$content = $content.Replace('AprovaÃ§Ã£o','Aprovação')
$content = $content.Replace('EducaA7A3o','Educacao')
$content = $content.Replace('SaBAde','Saude')
$content = $content.Replace('MA3es','Maes')
$content = $content.Replace('CesA1reo','Cesareo')
$content = $content.Replace('NaInfA2ncia','na_Infancia')

Set-Content $path $content -Encoding UTF8
Write-Host "Encoding corrigido!"
