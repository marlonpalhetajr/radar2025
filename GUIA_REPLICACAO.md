# 📋 Guia de Replicação - Tabelas Modernas

## 🎯 Objetivo

Replicar o modelo da **Tabela 1 Moderna** para as outras tabelas do Radar 2024.

---

## 📊 Estrutura Atual da Tabela 1

```html
<!-- Arquivo: tabelas/1-para/tabela-1-moderna.html -->
- Interface moderna com Bootstrap 5
- DataTables.js para interatividade
- Exportação em Excel com SheetJS
- Dados hardcoded no JavaScript (13 regiões)
```

---

## 🔄 Processo de Replicação

### Passo 1: Identificar a Tabela
Exemplo: Tabela 2 - População por Sexo

**Arquivos de entrada:**
- Excel: `tabelas-excel/1 Pará/Tabela 2 - População_Por_Sexo_e_Razão_de_Sexo_-_2025_Pará.xlsx`
- Saída esperada: `tabelas/1-para/tabela-2-moderna.html`

### Passo 2: Extrair Dados
Usar o script `extract_table_data.py` para obter os dados em JSON

```bash
# Editar o arquivo e apontar para a Tabela 2
python extract_table_data.py
```

### Passo 3: Adaptar o Template
Modificar `tabela-1-moderna.html` para a Tabela 2:

1. **Mudar o título**
   ```html
   <h1>Tabela 2</h1>
   <p>População por Sexo e Razão de Sexo - 2025</p>
   ```

2. **Adaptar as colunas**
   ```html
   <thead>
       <tr>
           <th>Região</th>
           <th>População Masculina</th>
           <th>População Feminina</th>
           <th>Razão de Sexo</th>
       </tr>
   </thead>
   ```

3. **Atualizar os dados**
   ```javascript
   const tabelaDados = [
       // Dados da Tabela 2
       {
           "regiao": "Pará",
           "populacaoMasculina": 4355598,
           "populacaoFeminina": 4355598,
           "razaoSexo": 100
       },
       // ... mais regiões
   ];
   ```

4. **Salvar como**
   ```
   tabelas/1-para/tabela-2-moderna.html
   ```

---

## 📁 Tabelas para Replicar (Pará)

Conforme encontrado, temos **51 tabelas** na região Pará:

### Grupo 1: Demografia
- [x] Tabela 1 - População, Área e Densidade (✅ PRONTA)
- [ ] Tabela 2 - População por Sexo e Razão de Sexo
- [ ] Tabela 3 - População por Faixa Etária
- [ ] Tabela 4 - Proporção de Idosos e Índice de Envelhecimento

### Grupo 2: Educação
- [ ] Tabela 5 - Matrículas em Creches e Ensinos
- [ ] Tabela 6 - Estabelecimentos de Creche e Ensinos
- [ ] Tabela 7 - Docentes em Creches e Ensinos
- [ ] Tabela 8 - Taxas de Aprovação, Reprovação (Ensino Fundamental)
- [ ] Tabela 9 - Taxas de Aprovação, Reprovação (Ensino Médio)
- [ ] Tabela 10 - Distorção idade-série
- [ ] Tabela 11 - IDEB Escola Pública
- [ ] Tabela 12 - Média de Alunos por Turma

### Grupo 3: Saúde
- [ ] Tabela 13 - Taxas de Mortalidade Infantil
- [ ] Tabela 14 - Taxas de Mortalidade Geral
- [ ] Tabela 15 - Taxa de Natalidade
- [ ] Tabela 16 - Nascidos Vivos e Pré-natal
- [ ] Tabela 17 - Nascidos Vivos por Faixa Etária da Mãe
- [ ] Tabela 18 - Óbitos por Causas
- [ ] Tabela 19 - Caracterização Hospitalar por Tipo
- [ ] Tabela 20 - Médicos e Profissionais de Saúde
- [ ] Tabela 21 - Caracterização dos Leitos
- [ ] Tabela 22 - Equipamentos Hospitalares

### Grupo 4: Trabalho e Renda
- [ ] Tabela 23 - Vínculos Empregatícios (Total e por Sexo)
- [ ] Tabela 24 - Vínculos por Grande Setor
- [ ] Tabela 25 - Vínculos por Setor Econômico
- [ ] Tabela 26 - Vínculos por Escolaridade
- [ ] Tabela 27 - Remuneração Média
- [ ] Tabela 28 - Informações de Famílias (CADÚnico, Bolsa Família)
- [ ] Tabela 29 - Benefícios Previdenciários

### Grupo 5: Segurança Pública
- [ ] Tabela 30 - Óbitos por Agressão (Homicídios)
- [ ] Tabela 31 - Óbitos de Jovens por Agressão
- [ ] Tabela 32 - Óbitos por Acidente de Trânsito

### Grupo 6: Meio Ambiente
- [ ] Tabela 33 - Desflorestamento e Focos de Calor
- [ ] Tabela 34 - Área de Floresta e Hidrografia
- [ ] Tabela 35 - Área Territorial e CAR

### Grupo 7: Economia
- [ ] Tabela 36 - PIB Total, Valor Adicionado
- [ ] Tabela 37 - VA Total e por Setores
- [ ] Tabela 38 - Participação do VA (Relação Estado)
- [ ] Tabela 39 - Participação do VA (Relação Município)
- [ ] Tabela 40 - PIB (Ranking Estadual)
- [ ] Tabela 41 - PIB per Capita
- [ ] Tabela 42 - Balança Comercial
- [ ] Tabela 43 - Lavoura Permanente
- [ ] Tabela 44 - Lavoura Temporária
- [ ] Tabela 45 - Efetivo de Rebanho
- [ ] Tabela 46 - Produção de Origem Animal

### Grupo 8: Infraestrutura
- [ ] Tabela 49 - Consumo de Energia Elétrica
- [ ] Tabela 50 - Frota de Veículos (Licenciados/Não Licenciados)
- [ ] Tabela 51 - Frota de Veículos por Tipo

---

## ⚡ Processo Automatizado (Recomendado)

Criar um script Python que:

```python
def replicar_todas_tabelas():
    """
    Lê todos os Excel da pasta
    Extrai dados
    Cria HTML moderno
    Salva em tabelas/1-para/
    """
    for arquivo_excel in listar_tabelas():
        dados = extrair_dados(arquivo_excel)
        html = criar_template_html(dados)
        salvar_html(html)
```

**Benefícios:**
- ✅ Automatizado
- ✅ Consistente
- ✅ Rápido (51 tabelas em segundos)
- ✅ Sem erros manuais

---

## 🌍 Replicação para Outras Regiões

Após completar Pará (13 regiões), replicar para:

1. **Araguaia** (tabelas-excel/2 Araguaia/)
2. **Baixo Amazonas** (tabelas-excel/3 Baixo Amazonas/)
3. **Carajás** (tabelas-excel/4 Carajás/)
4. ... (10 regiões mais)

**Total:** 51 tabelas × 13 regiões = **663 tabelas modernas**

---

## 💡 Dicas de Implementação

### 1. Validação de Dados
- Verificar se os números fazem sentido
- Checar formatação de datas
- Validar cálculos de agregações

### 2. Nomeação de Colunas
- Manter consistência
- Adicionar fontes quando necessário
- Incluir notas/observações

### 3. Performance
- Limitar a 100 linhas por página
- Usar busca indexada
- Lazy load para muitas tabelas

### 4. Integração ao Site
- Criar links no index.html
- Adicionar breadcrumbs
- Incluir botão "voltar"

---

## 📊 Métrica de Progresso

```
Pará:
- Tabela 1: ✅ 100% PRONTA
- Tabelas 2-51: ⏳ Aguardando replicação

Próximas Regiões: ⏱️ Planejado
```

---

## 🎯 Recomendação

**Para agora (próximas replicações):**

1. Validar a Tabela 1 Moderna
2. Testar com usuários
3. Fazer ajustes se necessário
4. Criar script automatizado
5. Aplicar a todas as 51 tabelas de Pará
6. Depois estender para outras regiões

**Estimativa:** 
- Tabela 1 validação: 1 dia
- Script automatizado: 1-2 dias  
- Aplicar 51 tabelas: 1 hora (automático)
- Testar: 1 dia
- **Total: 3-4 dias** para Pará completo

---

## 📞 Suporte

Se durante a replicação encontrar:
- ❓ Dúvidas: Consulte [TABELA_MODERNA_README.md](TABELA_MODERNA_README.md)
- 🐛 Bugs: Adicione ao arquivo [criar_tabelas_modernas.py](criar_tabelas_modernas.py)
- 💻 Dificuldades técnicas: Revise o [TESTE_TABELA_MODERNA.md](TESTE_TABELA_MODERNA.md)

---

**Pronto para começar a replicação!** 🚀

