# Tabela Moderna com Suporte a Download em Excel

## 📋 Descrição

Criada uma nova versão moderna da **Tabela 1 - População, Área Territorial e Densidade Demográfica** com as seguintes melhorias:

### ✨ Recursos Implementados

1. **Design Moderno e Responsivo**
   - Interface limpa com Bootstrap 5
   - Totalmente responsiva para dispositivos móveis
   - Estilo profissional com paleta de cores consistente

2. **Tabela Interativa (DataTables)**
   - Ordenação por qualquer coluna
   - Busca/filtro em tempo real
   - Paginação automática
   - 10 linhas por página (configurável)
   - Hover effects para melhor UX

3. **Exportação em Excel**
   - Botão "Baixar Excel" com ícone
   - Usa biblioteca SheetJS (XLSX)
   - Arquivo formatado com larguras de coluna ajustadas
   - Nome do arquivo: `Tabela_1_Populacao_Densidade_YYYY.xlsx`
   - Feedback visual ao usuário após download

4. **Formatação de Dados**
   - Números com formatação brasileira (separador de milhares e decimal)
   - Alinhamento à direita para valores numéricos
   - Fonte monoespaciada para melhor legibilidade de números

5. **Acessibilidade**
   - Semântica HTML adequada
   - Tabulação correta
   - Labels e descrições clara

## 📁 Arquivo Criado

```
tabelas/1-para/tabela-1-moderna.html
```

## 🛠️ Tecnologias Utilizadas

- **HTML5** - Estrutura semântica
- **CSS3** - Estilos responsivos e modernos
- **JavaScript** - Interatividade
- **Bootstrap 5** - Framework CSS
- **DataTables.js** - Tabela interativa
- **SheetJS (XLSX)** - Exportação em Excel
- **Bootstrap Icons** - Ícones vetoriais

## 🎯 Dados da Tabela

A tabela contém informações para todas as 13 Regiões de Integração do Pará:

1. Pará (estado)
2. Araguaia
3. Baixo Amazonas
4. Carajás
5. Guajará
6. Guamá
7. Lago de Tucuruí
8. Marajó
9. Rio Caeté
10. Rio Capim
11. Tapajós
12. Tocantins
13. Xingu

**Colunas:**
- Estado / Regiões de Integração
- População Estimada Total - 2025
- Área Territorial (km²) - 2024
- Densidade Demográfica (hab./km²)

## 🚀 Como Usar

1. Abrir o arquivo `tabela-1-moderna.html` em um navegador web
2. Usar o campo de busca para filtrar dados
3. Clicar nos cabeçalhos para ordenar
4. Navegar pelas páginas usando a paginação
5. Clicar em "Baixar Excel" para exportar os dados

## ✅ Próximos Passos

Uma vez validada e aprovada esta versão, o template pode ser:

1. **Replicado para as outras tabelas** da região Pará
2. **Adaptado para outras regiões** (Araguaia, Baixo Amazonas, etc.)
3. **Integrado ao site principal** do Radar
4. **Customizado** com cores e estilos do site se necessário

## 📝 Notas Técnicas

- Todas as bibliotecas são carregadas via CDN (sem dependências locais)
- Download compatível com Windows, Mac e Linux
- Funciona em navegadores modernos (Chrome, Firefox, Safari, Edge)
- Otimizado para performance

## 🔄 Manutenção

Para atualizar os dados:

1. Editar o array `tabelaDados` no arquivo HTML
2. Ou usar o script Python `extract_table_data.py` para extrair dados do Excel automaticamente

---

**Data de Criação:** 29/01/2026
**Versão:** 1.0
