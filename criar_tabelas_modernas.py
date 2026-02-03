#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar a Tabela 1 de cada região automaticamente
Cria versão moderna com DataTables e export em Excel
"""

import os
import json
from pathlib import Path
from datetime import datetime

def criar_tabela_moderna(regiao_nome, dados_tabela, caminho_saida):
    """
    Cria um arquivo HTML moderno com a tabela
    
    Args:
        regiao_nome: Nome da região (ex: "Pará", "Araguaia", etc)
        dados_tabela: Lista de dicts com os dados
        caminho_saida: Caminho para salvar o arquivo HTML
    """
    
    # Converte dados para JSON
    dados_json = json.dumps(dados_tabela, ensure_ascii=False, indent=2)
    
    html_content = f'''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabela 1 - {{regiao_nome}} | Radar 2024</title>
    <meta name="description" content="Tabela 1 - População, Área Territorial e Densidade Demográfica">
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- DataTables CSS -->
    <link href="https://cdn.datatables.net/2.0.8/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    
    <style>
        :root {{
            --primary-color: #0d6efd;
            --success-color: #198754;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #fff;
            padding: 20px 0;
        }}

        .container-table {{
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin: 20px auto;
        }}

        .table-header {{
            border-bottom: 3px solid var(--primary-color);
            margin-bottom: 25px;
            padding-bottom: 15px;
        }}

        .table-header h1 {{
            color: #1a1a1a;
            font-size: 28px;
            font-weight: 700;
            margin: 0;
        }}

        .controls-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .btn-export {{
            background-color: var(--success-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: background-color 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-export:hover {{
            background-color: #157347;
            color: white;
            text-decoration: none;
        }}

        table.dataTable tbody tr:hover {{
            background-color: #f8f9fa;
        }}

        table.dataTable tbody td:nth-child(n+2) {{
            text-align: right;
            font-family: 'Courier New', monospace;
        }}

        @media (max-width: 768px) {{
            .container-table {{
                padding: 15px;
            }}
            .controls-section {{
                flex-direction: column;
                align-items: stretch;
            }}
            .btn-export {{
                width: 100%;
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container-table" style="max-width: 1200px;">
        <div class="table-header">
            <h1><i class="bi bi-table"></i> Tabela 1</h1>
            <p style="color: #6c757d; margin-top: 5px;">População, Área Territorial e Densidade Demográfica - {regiao_nome}</p>
        </div>

        <div class="controls-section">
            <button class="btn-export" id="btnExportExcel" onclick="exportToExcel()">
                <i class="bi bi-file-earmark-excel"></i> Baixar Excel
            </button>
        </div>

        <div class="table-responsive">
            <table id="tabelaDados" class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Região</th>
                        <th>População</th>
                        <th>Área (km²)</th>
                        <th>Densidade (hab./km²)</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.datatables.net/2.0.8/js/dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/2.0.8/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>

    <script>
        const tabelaDados = {dados_json};

        document.addEventListener('DOMContentLoaded', function() {{
            const tbody = document.querySelector('#tabelaDados tbody');
            tabelaDados.forEach(row => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${{row.regiao || row.municipio || Object.values(row)[0]}}</td>
                    <td>${{formatarNumero(row.populacao || 0)}}</td>
                    <td>${{formatarNumeroDecimal(row.areaTerritorial || 0, 2)}}</td>
                    <td>${{formatarNumeroDecimal(row.densidadeDemografica || 0, 4)}}</td>
                `;
                tbody.appendChild(tr);
            }});

            $('#tabelaDados').DataTable({{
                language: {{
                    url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/pt-BR.json'
                }},
                paging: true,
                pageLength: 10,
                searching: true,
                ordering: true,
                responsive: true
            }});
        }});

        function formatarNumero(num) {{
            return new Intl.NumberFormat('pt-BR').format(Math.round(num));
        }}

        function formatarNumeroDecimal(num, casas = 2) {{
            return new Intl.NumberFormat('pt-BR', {{
                minimumFractionDigits: casas,
                maximumFractionDigits: casas
            }}).format(num);
        }}

        function exportToExcel() {{
            const ws_data = [
                ['Região', 'População', 'Área (km²)', 'Densidade (hab./km²)']
            ];

            tabelaDados.forEach(row => {{
                ws_data.push([
                    row.regiao || row.municipio || Object.values(row)[0],
                    row.populacao || 0,
                    row.areaTerritorial || 0,
                    row.densidadeDemografica || 0
                ]);
            }});

            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.aoa_to_sheet(ws_data);
            ws['!cols'] = [{{ wch: 30 }}, {{ wch: 20 }}, {{ wch: 20 }}, {{ wch: 25 }}];
            XLSX.utils.book_append_sheet(wb, ws, 'Tabela 1');

            const nomeArquivo = `Tabela_1_{{new Date().getFullYear()}}.xlsx`;
            XLSX.writeFile(wb, nomeArquivo);
        }}
    </script>
</body>
</html>'''
    
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Tabela moderna criada: {caminho_saida}")

# Exemplo de uso
if __name__ == "__main__":
    print("=" * 80)
    print("SCRIPT PARA CRIAR TABELAS MODERNAS - PREPARADO PARA PRÓXIMAS REGIÕES")
    print("=" * 80)
    print("\nEste script pode ser usado para atualizar as outras regiões com tabelas modernas")
    print("Quando pronto, execute para cada região:")
    print("\nExemplo:")
    print("  criar_tabela_moderna('Araguaia', dados_araguaia, 'tabelas/2-araguaia/tabela-1-moderna.html')")
