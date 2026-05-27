// Recursos compartilhados para o Repositório Radar
const DATA_MANIFEST_URL = 'dados_repositorio/manifest.json';
const REQUIRED_COLUMNS = ['tema', 'indicador', 'ri', 'localidade', 'nivel1', 'nivel2', 'nivel3', 'ano', 'valor'];
let dataManifestCache = null;

function normalizeCompare(value) {
  return (value || '')
    .toString()
    .trim()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

async function getDataManifest() {
  if (Array.isArray(dataManifestCache)) {
    return dataManifestCache;
  }

  const response = await fetch(DATA_MANIFEST_URL, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error(`Falha ao carregar manifesto de dados (${response.status})`);
  }

  const manifest = await response.json();
  if (!Array.isArray(manifest)) {
    throw new Error('Manifesto de dados inválido');
  }

  dataManifestCache = manifest.filter(entry => entry && entry.valid && entry.path);
  return dataManifestCache;
}

function parseCSVLine(line, delimiter = ';') {
  const result = [];
  let current = '';
  let insideQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      insideQuotes = !insideQuotes;
    } else if (char === delimiter && !insideQuotes) {
      result.push(current.trim().replace(/^"|"$/g, ''));
      current = '';
    } else {
      current += char;
    }
  }

  result.push(current.trim().replace(/^"|"$/g, ''));
  return result;
}

function parseCSVText(text, delimiter = ';') {
  const lines = text.split(/\r?\n/).filter(line => line.trim());
  if (lines.length === 0) return [];

  const headers = parseCSVLine(lines[0], delimiter).map(header => header.trim().replace(/^\uFEFF/, ''));
  const data = [];

  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i], delimiter);
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index] || '';
    });

    REQUIRED_COLUMNS.forEach(column => {
      if (!(column in row)) {
        row[column] = '';
      }
    });

    data.push(row);
  }

  return data;
}

async function loadDataFromEntries(entries) {
  const chunks = await Promise.all(entries.map(async (entry) => {
    const response = await fetch(encodeURI(entry.path), { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`Falha ao carregar arquivo: ${entry.path}`);
    }

    const text = await response.text();
    const delimiter = entry.delimiter === ',' ? ',' : ';';
    return parseCSVText(text, delimiter);
  }));

  return chunks.flat();
}

async function loadDataByTematica(tematica) {
  try {
    const manifest = await getDataManifest();
    const target = normalizeCompare(tematica);
    const entries = manifest.filter(entry => normalizeCompare(entry.tema || entry.tematica) === target);
    return await loadDataFromEntries(entries);
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    return [];
  }
}

function getUniqueValues(data, field) {
  return [...new Set(data.map(row => row[field]).filter(Boolean))].sort();
}

function formatNumber(value) {
  if (value === undefined || value === null || value === '') return '-';
  const num = Number(String(value).replace(/\./g, '').replace(',', '.'));
  if (!Number.isFinite(num)) return value;
  return num.toLocaleString('pt-BR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  });
}

function downloadXLSX(data, filename) {
  if (data.length === 0) {
    alert('Nenhum dado para fazer download!');
    return;
  }

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Dados');
  XLSX.writeFile(workbook, `${filename}_${new Date().toISOString().split('T')[0]}.xlsx`);
}

function downloadCSV(data, filename) {
  if (data.length === 0) {
    alert('Nenhum dado para fazer download!');
    return;
  }

  const headers = Object.keys(data[0]);
  let csv = headers.join(';') + '\n';

  data.forEach(row => {
    const values = headers.map(header => {
      const value = row[header] ?? '';
      if (typeof value === 'string' && (value.includes(';') || value.includes('"') || value.includes('\n'))) {
        return `"${value.replace(/"/g, '""')}"`;
      }
      return value;
    });
    csv += values.join(';') + '\n';
  });

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);

  link.setAttribute('href', url);
  link.setAttribute('download', `${filename}_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
