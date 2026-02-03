#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar tabelas HTML com dados dos arquivos Excel
Converte arquivos .xlsx para .htm mantendo formatação
"""

import pandas as pd
import os
import re
from pathlib import Path

# Mapeamento de nomes de pastas Excel -> HTML
MAPEAMENTO_REGIOES = {
    "1 Pará": "1-para",
    "2 Araguaia": "2-araguaia",
    "3 Baixo Amazonas": "3-baixo-amazonas",
    "4 Carajás": "4-carajas",
    "5 Guajará": "5-guajara",
    "6 Guamá": "6-guama",
    "7 Lago de Tucuruí": "7-lago-de-tucurui",
    "8 Marajó": "8-marajo",
    "9 Rio Caeté": "9-rio-caete",
    "10 Rio Capim": "10-rio-capim",
    "11 Tapajós": "11-tapajos",
    "12 Tocantins": "12-tocantins",
    "13 Xingu": "13-xingu"
}

def normalizar_nome_arquivo(nome_excel):
    """
    Converte nome do Excel para formato HTML
    Exemplo: "Tabela 1 - População,_Área_Territorial_(km²)_e_Densidade_Demográfica_-_2025_Pará.xlsx"
    Para: "tabela-1-populacao-area-territorial-km2-e-densidade-demografica"
    """
    # Remove extensão
    nome = nome_excel.replace('.xlsx', '')
    
    # Remove ano e região do final (ex: "2025 Pará", "2024 para", etc)
    nome = re.sub(r'[-_\s]+(20\d{2})[\s_-]+.*$', '', nome, flags=re.IGNORECASE)
    
    # Converte para minúsculas
    nome = nome.lower()
    
    # Remove underscores e substitui por espaços
    nome = nome.replace('_', ' ')
    
    # Remove caracteres especiais entre parênteses
    nome = re.sub(r'\([^)]*\)', lambda m: m.group(0).replace('²', '2'), nome)
    
    # Remove parênteses vazios e pontuação extra
    nome = nome.replace('(', '').replace(')', '')
    nome = nome.replace(',', '')
    
    # Substitui múltiplos espaços por hífen
    nome = re.sub(r'\s+', '-', nome.strip())
    
    # Remove hífens múltiplos
    nome = re.sub(r'-+', '-', nome)
    
    # Remove hífen no início/fim
    nome = nome.strip('-')
    
    return nome

def encontrar_arquivo_html(nome_base, pasta_html):
    """
    Encontra arquivo HTML correspondente ao Excel
    """
    # Lista todos os arquivos .htm na pasta
    arquivos = list(Path(pasta_html).glob('*.htm'))
    
    # Procura por correspondência
    for arquivo in arquivos:
        nome_html = arquivo.stem
        # Remove ano do nome HTML para comparação
        nome_html_base = re.sub(r'-20\d{2}-', '-', nome_html)
        nome_html_base = re.sub(r'-para$', '', nome_html_base)
        
        if nome_base in nome_html or nome_html_base.startswith(nome_base[:30]):
            return arquivo
    
    return None

def excel_para_html(arquivo_excel, arquivo_html_saida):
    """
    Converte arquivo Excel para HTML mantendo formatação
    """
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(arquivo_excel, engine='openpyxl')
        
        # Converte para HTML com formatação
        html = df.to_html(
            index=False,
            na_rep='',
            border=1,
            classes='table table-striped table-bordered',
            justify='left',
            float_format=lambda x: '{:,.2f}'.format(x) if pd.notnull(x) else ''
        )
        
        # Lê o arquivo HTML antigo para manter estrutura e estilos
        if arquivo_html_saida.exists():
            with open(arquivo_html_saida, 'r', encoding='utf-8') as f:
                conteudo_antigo = f.read()
            
            # Extrai apenas a tabela do HTML gerado pelo pandas
            nova_tabela = html
            
            # Substitui a tabela no HTML antigo
            # Procura pela tag <table> e substitui
            padrao_tabela = r'<table[^>]*>.*?</table>'
            if re.search(padrao_tabela, conteudo_antigo, re.DOTALL):
                conteudo_novo = re.sub(padrao_tabela, nova_tabela, conteudo_antigo, flags=re.DOTALL)
                
                # Salva o arquivo atualizado
                with open(arquivo_html_saida, 'w', encoding='utf-8') as f:
                    f.write(conteudo_novo)
                
                return True
            else:
                print(f"  ⚠️  Não foi possível encontrar tabela em {arquivo_html_saida.name}")
                return False
        else:
            print(f"  ⚠️  Arquivo HTML não existe: {arquivo_html_saida.name}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro ao processar {arquivo_excel.name}: {str(e)}")
        return False

def processar_regiao(pasta_excel, pasta_html):
    """
    Processa todos os arquivos Excel de uma região
    """
    arquivos_excel = list(Path(pasta_excel).glob('*.xlsx'))
    arquivos_processados = 0
    arquivos_erro = 0
    
    for arquivo_excel in arquivos_excel:
        # Ignora arquivos temporários do Excel
        if arquivo_excel.name.startswith('~'):
            continue
        
        print(f"\n  Processando: {arquivo_excel.name}")
        
        # Normaliza nome do arquivo
        nome_base = normalizar_nome_arquivo(arquivo_excel.name)
        print(f"  Nome base: {nome_base}")
        
        # Encontra arquivo HTML correspondente
        arquivo_html = encontrar_arquivo_html(nome_base, pasta_html)
        
        if arquivo_html:
            print(f"  Encontrado: {arquivo_html.name}")
            if excel_para_html(arquivo_excel, arquivo_html):
                print(f"  ✓ Atualizado com sucesso!")
                arquivos_processados += 1
            else:
                arquivos_erro += 1
        else:
            print(f"  ⚠️  Arquivo HTML não encontrado para: {arquivo_excel.name}")
            arquivos_erro += 1
    
    return arquivos_processados, arquivos_erro

def main():
    """
    Função principal
    """
    # Define caminhos base
    base_dir = Path(__file__).parent
    pasta_excel_base = base_dir / 'tabelas-excel'
    pasta_html_base = base_dir / 'tabelas'
    
    print("=" * 80)
    print("ATUALIZAÇÃO DE TABELAS HTML COM DADOS EXCEL")
    print("=" * 80)
    
    total_processados = 0
    total_erros = 0
    
    # Processa cada região
    for regiao_excel, regiao_html in MAPEAMENTO_REGIOES.items():
        print(f"\n{'=' * 80}")
        print(f"REGIÃO: {regiao_excel}")
        print(f"{'=' * 80}")
        
        pasta_excel = pasta_excel_base / regiao_excel
        pasta_html = pasta_html_base / regiao_html
        
        if not pasta_excel.exists():
            print(f"⚠️  Pasta Excel não encontrada: {pasta_excel}")
            continue
        
        if not pasta_html.exists():
            print(f"⚠️  Pasta HTML não encontrada: {pasta_html}")
            continue
        
        processados, erros = processar_regiao(pasta_excel, pasta_html)
        total_processados += processados
        total_erros += erros
        
        print(f"\n  Resumo da região:")
        print(f"  ✓ Processados: {processados}")
        print(f"  ❌ Erros: {erros}")
    
    # Resumo final
    print(f"\n{'=' * 80}")
    print(f"RESUMO FINAL")
    print(f"{'=' * 80}")
    print(f"Total de arquivos processados: {total_processados}")
    print(f"Total de erros: {total_erros}")
    print(f"Total geral: {total_processados + total_erros}")

if __name__ == "__main__":
    main()
