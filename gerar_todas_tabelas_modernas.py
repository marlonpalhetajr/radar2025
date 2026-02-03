#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter TODAS as tabelas Excel (todas as regiões)
em versões HTML modernas com DataTables e exportação em Excel.
"""

import pandas as pd
import os
import re
import json
from pathlib import Path

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
    """Converte nome do Excel para formato HTML"""
    nome = nome_excel.replace('.xlsx', '')
    nome = re.sub(r'[-_\s]+(20\d{2})[\s_-]+.*$', '', nome, flags=re.IGNORECASE)
    nome = nome.lower()
    nome = nome.replace('_', ' ')
    nome = re.sub(r'\([^)]*\)', lambda m: m.group(0).replace('²', '2'), nome)
    nome = re.sub(r'[^\w\s-]', '', nome)
    nome = re.sub(r'[-\s]+', '-', nome)
    nome = nome.strip('-')
    return nome

def _linha_e_cabecalho(row):
    textos = [str(x).strip() for x in row if pd.notna(x)]
    if not textos:
        return False
    joined = " ".join(textos).lower()
    if "tabela" in joined:
        return False
    if re.match(r"^(fonte|elabora|nota|observa)", joined):
        return False
    if any(k in joined for k in ["estado", "região", "regiao", "município", "municipio", "ris", "ano", "total"]):
        return True
    text_count = sum(1 for x in row if pd.notna(x) and isinstance(x, str))
    num_count = sum(1 for x in row if pd.notna(x) and isinstance(x, (int, float)))
    return text_count >= max(2, num_count + 1)


def extrair_dados_tabela(caminho_excel):
    """Extrai dados de um arquivo Excel e separa notas."""
    try:
        raw = pd.read_excel(caminho_excel, sheet_name=0, header=None, dtype=object)
        raw = raw.dropna(how="all").reset_index(drop=True)
        if raw.empty:
            return None, []

        header_idx = None
        for idx, row in raw.iterrows():
            if _linha_e_cabecalho(row):
                header_idx = idx
                break

        if header_idx is None:
            header_idx = 0

        header_row = raw.iloc[header_idx]
        df = raw.iloc[header_idx + 1:].reset_index(drop=True)

        df = df.loc[:, header_row.notna()]
        header_row = header_row[header_row.notna()]
        df.columns = header_row

        df = df.dropna(how="all").reset_index(drop=True)

        notas = []
        indices_remover = []
        if not df.empty:
            primeira_coluna = df.columns[0]
            for idx, valor in df[primeira_coluna].items():
                if isinstance(valor, str) and re.match(r"^\s*(fonte|elabora|nota|observa)", valor, re.IGNORECASE):
                    notas.append(valor.strip())
                    indices_remover.append(idx)
        if indices_remover:
            df = df.drop(index=indices_remover).reset_index(drop=True)

        return df, notas
    except Exception as e:
        print(f"  ❌ Erro ao extrair dados: {e}")
        return None, []

def criar_html_moderno(nome_tabela, titulo, df, notas, caminho_saida, regiao_atual=None):
    """Cria arquivo HTML moderno com DataTables"""
    
    if df is None or len(df) == 0:
        print(f"  ⚠️ Dados vazios para {nome_tabela}")
        return False
    
    # Prepara dados para JSON
    colunas = [re.sub(r"\s+", " ", str(col).strip()) for col in df.columns]
    dados = []
    
    for _, row in df.iterrows():
        linha = {}
        for i, col in enumerate(colunas):
            valor = row.iloc[i]
            if pd.isna(valor):
                linha[f'col{i}'] = ''
            elif isinstance(valor, (int, float)):
                linha[f'col{i}'] = float(valor)
            else:
                linha[f'col{i}'] = str(valor).strip()
        dados.append(linha)
    
    dados_json = json.dumps(dados, ensure_ascii=False, indent=2)
    colunas_json = json.dumps(colunas, ensure_ascii=False)
    notas_json = json.dumps(notas, ensure_ascii=False, indent=2)
    
    # Define o nome da região para reordenação
    regiao_nome = regiao_atual if regiao_atual else ""
    
    html_content = f'''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} | Radar 2024</title>
    <meta name="description" content="{titulo}">
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/2.0.8/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    
    <style>
        :root {{
            --primary-blue: #1e3a8a;
            --primary-purple: #7c3aed;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --success-green: #10b981;
            --warning-orange: #f59e0b;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container-table {{
            background-color: #ffffff;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 18px;
            margin: 20px auto;
            max-width: 98%;
        }}
        
        .table-header {{
            background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .table-header h1 {{
            color: #ffffff;
            font-size: 22px;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .table-header .subtitle {{
            color: #e0e7ff;
            font-size: 13px;
            margin-top: 8px;
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
            background: linear-gradient(135deg, var(--success-green) 0%, #059669 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
        }}
        
        .btn-export:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
        }}
        
        .btn-back {{
            background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.3s ease;
        }}
        
        .btn-back:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            color: white;
        }}
        
        .table-responsive {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        table.dataTable {{
            width: 100% !important;
            border-collapse: collapse;
        }}
        
        table.dataTable thead {{
            background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        }}
        
        table.dataTable thead th {{
            color: #ffffff !important;
            font-weight: 800 !important;
            padding: 10px 8px !important;
            text-align: center !important;
            font-size: 12px !important;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            border: none !important;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        }}
        
        table.dataTable tbody td {{
            padding: 8px !important;
            border-bottom: 1px solid #e5e7eb;
            color: #111827;
            font-size: 11px;
            font-weight: 500;
            text-align: center !important;
        }}
        
        table.dataTable tbody td:first-child {{
            font-weight: 700;
            color: #1e3a8a;
        }}
        
        table.dataTable tbody tr:first-child {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            font-weight: 700;
        }}
        
        table.dataTable tbody tr:first-child td {{
            color: #1e40af;
            font-weight: 800;
        }}
        
        table.dataTable tbody tr:hover {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            transition: all 0.2s ease;
        }}
        
        table.dataTable tbody tr:nth-child(even) {{
            background-color: #f9fafb;
        }}
        
        #tableNotes {{
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 12px;
            color: #4b5563;
            line-height: 1.6;
        }}
        
        @media (max-width: 768px) {{
            .container-table {{
                padding: 15px;
                max-width: 100%;
            }}
            
            .table-header h1 {{
                font-size: 18px;
            }}
            
            .controls-section {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .btn-export {{
                width: 100%;
                justify-content: center;
            }}
            
            table.dataTable thead th,
            table.dataTable tbody td {{
                font-size: 11px !important;
                padding: 8px !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container-table">
        <div class="table-header">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h1><i class="bi bi-table"></i> {titulo}</h1>
                <a href="../../index.html" class="btn-back">
                    <i class="bi bi-arrow-left"></i> Voltar
                </a>
            </div>
        </div>

        <div class="controls-section">
            <button class="btn-export" onclick="exportToExcel()">
                <i class="bi bi-file-earmark-excel"></i> Baixar Excel
            </button>
            <div style="font-size: 12px; color: #999;">
                <i class="bi bi-info-circle"></i> Use a busca para filtrar dados
            </div>
        </div>

        <div class="table-responsive">
            <table id="tabelaDados" class="table table-striped table-hover table-sm">
                <thead>
                    <tr id="tableHeader"></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        <div id="tableNotes" class="mt-3" style="font-size: 12px; color: #6c757d;"></div>
    </div>

    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.datatables.net/2.0.8/js/dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/2.0.8/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>

    <script>
        const tabelaDados = {dados_json};
        const colunas = {colunas_json};
        const notas = {notas_json};
        const regiaoAtual = "{regiao_nome}";

        document.addEventListener('DOMContentLoaded', function() {{
            // Reordenar dados para colocar a região principal primeiro
            if (regiaoAtual && regiaoAtual.trim() !== "") {{
                const regiaoDados = regiaoAtual.toLowerCase().replace(/\bri\b\s*/, '').trim();
                
                tabelaDados.sort((a, b) => {{
                    const aText = a.col0 ? a.col0.toLowerCase().replace(/\bri\b\s*/, '').trim() : '';
                    const bText = b.col0 ? b.col0.toLowerCase().replace(/\bri\b\s*/, '').trim() : '';
                    
                    // Verifica correspondência exata
                    if (aText === regiaoDados) return -1;
                    if (bText === regiaoDados) return 1;
                    
                    // Verifica correspondência parcial (para casos como "RI Araguaia" vs "Araguaia")
                    if (aText.includes(regiaoDados)) return -1;
                    if (bText.includes(regiaoDados)) return 1;
                    
                    return 0;
                }});
            }}
            const thead = document.querySelector('#tableHeader');
            const tbody = document.querySelector('#tabelaDados tbody');
            const notesEl = document.querySelector('#tableNotes');

            colunas.forEach(col => {{
                const th = document.createElement('th');
                th.textContent = col || '';
                thead.appendChild(th);
            }});
            
            tabelaDados.forEach(row => {{
                const tr = document.createElement('tr');
                for (let i = 0; i < colunas.length; i++) {{
                    const td = document.createElement('td');
                    const valor = row[`col${{i}}`];
                    
                    if (typeof valor === 'number') {{
                        if (Number.isInteger(valor) && valor > 1000) {{
                            td.textContent = new Intl.NumberFormat('pt-BR').format(valor);
                        }} else {{
                            td.textContent = new Intl.NumberFormat('pt-BR', {{
                                minimumFractionDigits: 0,
                                maximumFractionDigits: 4
                            }}).format(valor);
                        }}
                    }} else {{
                        td.textContent = valor || '';
                        if (i === 0) td.style.textAlign = 'left';
                    }}
                    tr.appendChild(td);
                }}
                tbody.appendChild(tr);
            }});

            $('#tabelaDados').DataTable({{
                language: {{
                    emptyTable: "Nenhum dado disponível na tabela",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
                    infoEmpty: "Mostrando 0 a 0 de 0 registros",
                    infoFiltered: "(filtrado de _MAX_ registros)",
                    lengthMenu: "Mostrar _MENU_ registros",
                    loadingRecords: "Carregando...",
                    processing: "Processando...",
                    search: "Buscar:",
                    zeroRecords: "Nenhum registro encontrado",
                    paginate: {{
                        first: "Primeiro",
                        last: "Último",
                        next: "Próximo",
                        previous: "Anterior"
                    }}
                }},
                paging: true,
                pageLength: 25,
                lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "Todos"]],
                searching: true,
                ordering: true,
                info: true,
                responsive: true,
                dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rt<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>'
            }});

            if (notas.length) {{
                notesEl.innerHTML = notas.map(nota => `<div>${{nota}}</div>`).join('');
            }}
        }});

        function exportToExcel() {{
            const ws_data = [colunas];
            
            tabelaDados.forEach(row => {{
                const rowData = [];
                for (let i = 0; i < colunas.length; i++) {{
                    rowData.push(row[`col${{i}}`]);
                }}
                ws_data.push(rowData);
            }});

            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.aoa_to_sheet(ws_data);
            
            const colWidths = colunas.map(() => ({{ wch: 20 }}));
            ws['!cols'] = colWidths;
            
            XLSX.utils.book_append_sheet(wb, ws, 'Dados');
            
            const nomeArquivo = '{nome_tabela}.xlsx';
            XLSX.writeFile(wb, nomeArquivo);
            
            const btn = document.querySelector('.btn-export');
            const textoOriginal = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check-circle"></i> Download Concluído!';
            btn.style.backgroundColor = '#198754';
            setTimeout(() => {{
                btn.innerHTML = textoOriginal;
                btn.style.backgroundColor = '';
            }}, 2000);
        }}
    </script>
</body>
</html>'''
    
    try:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return True
    except Exception as e:
        print(f"  ❌ Erro ao criar HTML: {e}")
        return False

def _encontrar_nome_saida(arquivo_excel, pasta_html):
    match = re.search(r"tabela\s*(\d+)", arquivo_excel.name, re.IGNORECASE)
    if match:
        numero = match.group(1)
        candidatos = list(pasta_html.glob(f"tabela-{numero}-*.htm"))
        if candidatos:
            sem_modern = [c for c in candidatos if "modern" not in c.name.lower()]
            return (sem_modern[0] if sem_modern else candidatos[0]).name
    return f"{normalizar_nome_arquivo(arquivo_excel.name)}.htm"


def processar_todas_tabelas():
    """Processa todas as tabelas de todas as regiões"""
    
    print("=" * 80)
    print("GERAÇÃO AUTOMÁTICA DE TABELAS MODERNAS - TODAS AS REGIÕES")
    print("=" * 80)
    
    base_dir = Path(__file__).parent
    sucesso = 0
    falhas = 0

    for pasta_excel_nome, pasta_html_nome in MAPEAMENTO_REGIOES.items():
        pasta_excel = base_dir / "tabelas-excel" / pasta_excel_nome
        pasta_html = base_dir / "tabelas" / pasta_html_nome
        
        # Extrai o nome da região (remove o número e espaço do início)
        regiao_atual = pasta_excel_nome.split(' ', 1)[1] if ' ' in pasta_excel_nome else pasta_excel_nome

        if not pasta_excel.exists():
            print(f"⚠️ Pasta Excel não encontrada: {pasta_excel}")
            continue

        pasta_html.mkdir(parents=True, exist_ok=True)

        arquivos_excel = list(pasta_excel.glob("Tabela*.xlsx")) + list(pasta_excel.glob("Tabela*.xls"))
        arquivos_excel = [f for f in arquivos_excel if not f.name.startswith('~')]
        arquivos_por_base = {}
        for arquivo in arquivos_excel:
            base = arquivo.stem.lower()
            atual = arquivos_por_base.get(base)
            if atual is None or arquivo.stat().st_mtime > atual.stat().st_mtime:
                arquivos_por_base[base] = arquivo
        arquivos_excel = list(arquivos_por_base.values())

        print(f"\n📊 {pasta_excel_nome}: {len(arquivos_excel)} tabelas para processar\n")

        for idx, arquivo_excel in enumerate(sorted(arquivos_excel), 1):
            print(f"[{idx}/{len(arquivos_excel)}] {arquivo_excel.name}")

            df, notas = extrair_dados_tabela(arquivo_excel)

            if df is None:
                falhas += 1
                continue

            titulo = arquivo_excel.stem
            if 'Tabela' in titulo:
                titulo = re.sub(r'[-_,]+', ' ', titulo)
                titulo = re.sub(r'\s+', ' ', titulo).strip()

            nome_saida = _encontrar_nome_saida(arquivo_excel, pasta_html)
            caminho_html = pasta_html / nome_saida

            if criar_html_moderno(Path(nome_saida).stem, titulo, df, notas, caminho_html, regiao_atual):
                print(f"  ✓ Criado: {caminho_html.name}")
                sucesso += 1
            else:
                falhas += 1
    
    print("\n" + "=" * 80)
    print(f"✅ CONCLUÍDO: {sucesso} tabelas criadas com sucesso")
    if falhas > 0:
        print(f"⚠️ FALHAS: {falhas} tabelas com erro")
    print("=" * 80)

if __name__ == "__main__":
    processar_todas_tabelas()
