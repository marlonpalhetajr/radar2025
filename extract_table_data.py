#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair dados de uma tabela Excel e converter para JSON
"""

import pandas as pd
import json
import os
from pathlib import Path

# Arquivo Excel de entrada
excel_file = r"c:\Users\marlon.junior\OneDrive - Fapespa\radar2024\tabelas-excel\1 Pará\Tabela 1 - População,_Área_Territorial_(km²)_e_Densidade_Demográfica_-_2025_Pará.xlsx"

try:
    # Lê o Excel
    df = pd.read_excel(excel_file, sheet_name=0)
    
    # Remove linhas completamente vazias
    df = df.dropna(how='all')
    
    # Exibe as primeiras linhas
    print("Primeiras linhas da tabela:")
    print(df.head(10))
    print(f"\nTotal de linhas: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")
    print("\nNomes das colunas:")
    print(df.columns.tolist())
    
    # Converte para JSON
    json_data = df.to_json(orient='records', indent=2, force_ascii=False)
    
    # Salva em arquivo JSON
    output_file = r"c:\Users\marlon.junior\OneDrive - Fapespa\radar2024\tabela1_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_data)
    
    print(f"\n✓ Dados extraídos e salvos em: {output_file}")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
