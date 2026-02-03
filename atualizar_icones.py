#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# Mapeamento de ícones antigos para novos
icon_mapping = {
    # Demografia
    "icons/02_demografia/Demografia_Estimativa_Populacional2024.png": "icons/02_demografia/Demografia_Estimativa_Populacional2025.png",
    
    # Educação
    "icons/03_educacao/EducaA7A3o_TX_ReprovaA7A3o_Fundamental2023.png": "icons/03_educacao/Educação_IDEB_Series_Iniciais2023.png",  # IDEB Iniciais
    # Precisa de dois ícones diferentes - vamos fazer manualmente por contexto
    
    # Saúde
    "icons/04_saude/SaBAde_Taxa_Mortalidade_Materna_2023.png": "icons/04_saude/Saúde_Taxa_Mortalidade_Infantil_2024.png",
    # Necessita substituições contextuais
    
    # Mercado de Trabalho
    "icons/05_mercado_de_trabalho/Mercado_de_Trabalho_Vinculos_Empregaticios_2024.png": "icons/05_mercado_de_trabalho/MercadoDeTrabalho_Vínculos_Empregatícios2024.png",
    "icons/05_mercado_de_trabalho/Mercado_de_Trabalho_Remuneracao_Media_2024.png": "icons/05_mercado_de_trabalho/MercadoDeTrabalho_Remuneração_Média2024.png",
    
    # Assistência e Previdência
    "icons/06_assistencia_e_previdencia_social/AssistAAnciaPrevidAAnciaSocial_FamADlias_Inscritas_Cad9Anico2023.png": "icons/06_assistencia_e_previdencia_social/AssistênciaPrevidênciaSocial_Famílias_Inscritas_CadÚnico2024.png",
    "icons/06_assistencia_e_previdencia_social/AssistAAnciaPrevidAAnciaSocial_FamADlias_Inscritas_BolsaFamADlia2023.png": "icons/06_assistencia_e_previdencia_social/AssistênciaPrevidênciaSocial_Famílias_Inscritas_BolsaFamília2024.png",
    "icons/06_assistencia_e_previdencia_social/AssistAAnciaPrevidAAnciaSocial_Valor_Pago_BolsaFamilia2023.png": "icons/06_assistencia_e_previdencia_social/AssistênciaPrevidênciaSocial_Valor_Pago_BolsaFamilia2024.png",
    "icons/06_assistencia_e_previdencia_social/AssistAAnciaPrevidAAnciaSocial_ValorTotal_Beneficios_Emitidos_PrevidenciaSocial2023.png": "icons/06_assistencia_e_previdencia_social/AssistênciaPrevidênciaSocial_ValorTotal_Beneficios_Emitidos_PrevidenciaSocial2024.png",
    
    # Segurança
    "icons/07_segurança/SeguranA7a_TX_HomicADdios_Total_2023.png": "icons/07_segurança/Segurança_TX_Homicídios_Total_2024.png",
    "icons/07_segurança/SeguranA7a_TX_HomicADdios_Jovens_2023.png": "icons/07_segurança/Segurança_TX_Homicídios_Jovens_2024.png",
    "icons/07_segurança/SeguranA7a_TX_Mortes_TrA2nsito2023.png": "icons/07_segurança/Segurança_TX_Mortes_Trânsito2024.png",
    
    # Meio Ambiente
    "icons/08_meio_ambiente/Social_Leitos2024.png": "icons/08_meio_ambiente/MeioAmbiente_Desflorestamento2024.png",
    "icons/08_meio_ambiente/Meio_Ambiente_Desflorestamento_Acumulado_2023.png": "icons/08_meio_ambiente/MeioAmbiente_Desflorestamento2024.png",
    "icons/08_meio_ambiente/Meio_Ambiente_Desflorestamento_Incremento_Acumulado_2023.png": "icons/08_meio_ambiente/MeioAmbiente_Incremento_Desflorestamento2024.png",
    "icons/08_meio_ambiente/Meio_Ambiente_Focos_de_Calor_2023.png": "icons/08_meio_ambiente/MeioAmbiente_Focos_Calor2024.png",
    
    # Economia
    "icons/09_economia/Economia_VA_Setor_Agropecuaria_2024.png": "icons/09_economia/Economia_PIB2023.png",  # PIB principal
    "icons/09_economia/Economia_VA_Setor_Adm_Pub_2024.png": "icons/09_economia/Economia_ValorAdicionado_Setor_Administração_Pública2021.png",
    "icons/09_economia/Economia_VA_Setor_Servicos_2024.png": "icons/09_economia/Economia_ValorAdicionado_Setor_Serviços2021.png",
    "icons/09_economia/Economia_VA_Setor_Industrial_2024.png": "icons/09_economia/Economia_ValorAdicionado_Setor_Industrial2021.png",
    "icons/09_economia/Economia_PIB_Per_Capita_2024.png": "icons/09_economia/Economia_PIB_PerCapita2023.png",
    "icons/09_economia/Economia_Bal_Com_Exportacao_2024.png": "icons/09_economia/Economia_BalançaComercial_Exportação2024.png",
    "icons/09_economia/Economia_Bal_Com_Importacao_2024.png": "icons/09_economia/Economia_BalançaComercial_Importação2024.png",
    "icons/09_economia/Economia_Bal_Comercial_Saldo_2024.png": "icons/09_economia/Economia_BalançaComercial_Saldo2024.png",
    
    # Finanças Públicas
    "icons/10_financas_publicas/Financas_Publicas_Repasse_de_ICMS_2024.png": "icons/10_financas_publicas/FinançasPúblicas_Repasse_ICMS2024.png",
    
    # Infraestrutura
    "icons/11_infraestrutura/Infraestrutura_Consumo_de_Energia_2024.png": "icons/11_infraestrutura/Infraestrutura_ConsumoEnergia2024.png",
    "icons/11_infraestrutura/Infraestrutura_Consumidores_de_Energia_2024.png": "icons/11_infraestrutura/Infraestrutura_Consumidores2024.png",
    "icons/11_infraestrutura/Infraestrutura_Frota_de_VeADculos_2024.png": "icons/11_infraestrutura/Infraestrutura_Frota_veículos2024.png",
}

# Ler o arquivo
with open("project.html", "r", encoding="utf-8") as f:
    content = f.read()

# Substituições simples
for old, new in icon_mapping.items():
    content = content.replace(f'src="{old}"', f'src="{new}"')

# Substituições contextuais para educação (precisa de 3 ícones diferentes do mesmo arquivo)
# IDEB Iniciais
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4 text-center">IDEB S[ée]ries Iniciais</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_IDEB_Series_Iniciais2023.png"',
    content,
    flags=re.DOTALL
)

# IDEB Finais
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4">IDEB S[ée]ries Finais</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_IDEB_Series_finais2023.png"',
    content,
    flags=re.DOTALL
)

# Taxa de Aprovação Fundamental
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4">Taxa de Aprova[çc][ãa]o Ens\. Fundamental</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_TX_Aprovação_Fundamental2024.png"',
    content,
    flags=re.DOTALL
)

# Taxa de Aprovação Médio
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class=" text-white mb-4">Taxa de Aprova[çc][ãa]o Ens\. M[ée]dio</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_TX_Aprovação_Medio2024.png"',
    content,
    flags=re.DOTALL
)

# Taxa de Reprovação Fundamental  
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4">Taxa de Reprova[çc][ãa]o Ens\. Fundamental</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_TX_Reprovação_Fundamental2024.png"',
    content,
    flags=re.DOTALL
)

# Taxa de Reprovação Médio
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4">Taxa de Reprova[çc][ãa]o Ens\. M[ée]dio</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_TX_Reprovação_Medio2024.png"',
    content,
    flags=re.DOTALL
)

# Taxa de Abandono Fundamental
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4">Taxa de Abandono Ens\. Fundamental</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_TX_Abandono_Fundamental2024.png"',
    content,
    flags=re.DOTALL
)

# Taxa de Abandono Médio
content = re.sub(
    r'(<div class="col-lg-4 col-md-6 portfolio-item educacao ">.*?<h4 class="text-white mb-4">Taxa de Abandono Ens\. M[ée]dio</h4>.*?<img class="img-fluid" src=")icons/03_educacao/[^"]*"',
    r'\1icons/03_educacao/Educação_TX_Abandono_Medio2024.png"',
    content,
    flags=re.DOTALL
)

# Substituições contextuais para Saúde (múltiplos cards)
health_replacements = {
    "Taxa de Mortalidade Infantil": "icons/04_saude/Saúde_Taxa_Mortalidade_Infantil_2024.png",
    "Taxa de Mortalidade na Inf[âa]ncia": "icons/04_saude/Saúde_Taxa_Mortalidade_NaInfância_2024.png",
    "Taxa de Mortalidade Materna": "icons/04_saude/Saúde_Taxa_Mortalidade_Materna_2024.png",
    "Taxa de Mortalidade Geral": "icons/04_saude/Saúde_TX_Mortalidade_Geral2024.png",
    "Taxa de Natalidade": "icons/04_saude/Saúde_Taxa_Natalidade_2024.png",
    "Percentual de Nascidos Vivos de Parto Normal": "icons/04_saude/Saúde_PercentualNascidosVivos_Parto_Normal2024.png",
    "Percentual de Nascidos Vivos Por Ces[áa]ria": "icons/04_saude/Saúde_PercentualNascidosVivos_Parto_Cesáreo2024.png",
    "Percentual de Nascidos Vivos de M[ãa]es Faixa Et[áa]ria": "icons/04_saude/Saúde_PercentualNascidosVivos_Mães10A19anos_2024.png",
    "Percentual de Nascidos Vivos com 7 ou Mais": "icons/04_saude/Saúde_PercentualNascidosVivos_Com7ouMaisConsultas2024.png",
}

for title_pattern, icon_path in health_replacements.items():
    content = re.sub(
        rf'(<div class="col-lg-4 col-md-6 portfolio-item saude ">.*?<h4 class="text-white mb-4">[^<]*{title_pattern}[^<]*</h4>.*?<img class="img-fluid" src=")icons/04_saude/[^"]*"',
        rf'\1{icon_path}"',
        content,
        flags=re.DOTALL
    )

# Salvar o arquivo
with open("project.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✓ Ícones atualizados com sucesso!")
