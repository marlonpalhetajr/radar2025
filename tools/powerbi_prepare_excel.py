import argparse
import hashlib
import re
from pathlib import Path

import pandas as pd


def slugify(value: str) -> str:
    value = str(value).strip()
    value = re.sub(r"[\s/\\]+", "_", value)
    value = re.sub(r"[^0-9A-Za-z_\-]+", "", value)
    return value or "sheet"


def safe_filename(name: str, max_len: int = 120) -> str:
    name = str(name)
    if len(name) <= max_len:
        return name
    digest = hashlib.sha1(name.encode("utf-8", errors="ignore")).hexdigest()[:8]
    if "." in name:
        base, ext = name.rsplit(".", 1)
        ext = f".{ext}"
    else:
        base, ext = name, ""
    keep = max_len - len(ext) - 1 - len(digest)
    if keep < 1:
        return name[:max_len]
    return f"{base[:keep]}_{digest}{ext}"


def detect_header_row(df: pd.DataFrame, max_scan: int = 20) -> int:
    scan = df.head(max_scan)
    counts = scan.notna().sum(axis=1)
    if counts.max() == 0:
        return 0
    return int(counts.idxmax())


def clean_columns(columns) -> list[str]:
    cleaned = []
    seen = {}
    for col in columns:
        name = str(col).strip()
        if not name or name.lower().startswith("unnamed"):
            name = "col"
        name = re.sub(r"\s+", " ", name)
        name = name.replace(" ", "_")
        name = re.sub(r"[^0-9A-Za-z_]+", "", name)
        if not name:
            name = "col"
        count = seen.get(name, 0) + 1
        seen[name] = count
        cleaned.append(f"{name}_{count}" if count > 1 else name)
    return cleaned


def parse_metadata(file_path: Path) -> dict:
    filename = file_path.stem
    region = file_path.parent.name
    tabela_match = re.search(r"(?i)tabela\s*(\d+)", filename)
    tabela_num = tabela_match.group(1) if tabela_match else ""
    year_matches = re.findall(r"(19|20)\d{2}", filename)
    year = year_matches[-1] if year_matches else ""
    titulo = re.sub(r"(?i)^tabela\s*\d+\s*-\s*", "", filename).strip()
    return {
        "regiao": region,
        "tabela_num": tabela_num,
        "titulo": titulo,
        "ano": year,
        "arquivo": filename,
        "arquivo_path": str(file_path),
    }


def coerce_numeric_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    numeric_cols = []
    for col in df.columns:
        series = df[col]
        if series.dtype == "object":
            s = series.astype(str).str.replace(".", "", regex=False)
            s = s.str.replace(",", ".", regex=False)
            s = s.str.replace("\u00A0", "", regex=False)
            s = s.str.strip()
            num = pd.to_numeric(s, errors="coerce")
            ratio = num.notna().mean()
            if ratio >= 0.7:
                df[col] = num
                numeric_cols.append(col)
        elif pd.api.types.is_numeric_dtype(series):
            numeric_cols.append(col)
    return df, numeric_cols


def clean_sheet(raw_df: pd.DataFrame) -> pd.DataFrame:
    header_idx = detect_header_row(raw_df)
    header = raw_df.iloc[header_idx].fillna("")
    df = raw_df.iloc[header_idx + 1 :].copy()
    df.columns = clean_columns(header)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    return df


def process_file(file_path: Path, output_dir: Path, make_long: bool) -> list[pd.DataFrame]:
    data = pd.read_excel(file_path, sheet_name=None, header=None)
    all_frames = []
    meta = parse_metadata(file_path)

    for sheet_name, raw_df in data.items():
        if raw_df.dropna(how="all").empty:
            continue

        df = clean_sheet(raw_df)
        if df.empty:
            continue

        df, numeric_cols = coerce_numeric_columns(df)

        for key, val in meta.items():
            df[key] = val
        df["aba"] = sheet_name

        out_dir = output_dir / meta["regiao"]
        out_dir.mkdir(parents=True, exist_ok=True)
        base_name = slugify(meta["arquivo"])
        out_name = safe_filename(f"{base_name}__{slugify(sheet_name)}.csv")
        df.to_csv(out_dir / out_name, index=False, encoding="utf-8-sig")
        all_frames.append(df)

        if make_long and numeric_cols:
            id_cols = [c for c in df.columns if c not in numeric_cols]
            long_df = df.melt(id_vars=id_cols, value_vars=numeric_cols, var_name="variavel", value_name="valor")
            long_name = safe_filename(f"{base_name}__{slugify(sheet_name)}__long.csv")
            long_df.to_csv(out_dir / long_name, index=False, encoding="utf-8-sig")

    return all_frames


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Excel tables for Power BI")
    parser.add_argument("--input", required=True, help="Caminho da pasta com os Excel")
    parser.add_argument("--output", required=False, help="Caminho da pasta de saída")
    parser.add_argument("--long", action="store_true", help="Gerar também versão em formato longo")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        raise SystemExit(f"Pasta não encontrada: {input_dir}")

    output_dir = Path(args.output) if args.output else input_dir.parent / f"{input_dir.name}_cleaned"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_frames = []
    for file_path in input_dir.rglob("*.xlsx"):
        if file_path.name.startswith("~$"):
            continue
        all_frames.extend(process_file(file_path, output_dir, args.long))

    if all_frames:
        consolidated = pd.concat(all_frames, ignore_index=True)
        consolidated.to_csv(output_dir / "_all_tables.csv", index=False, encoding="utf-8-sig")

    print(f"Concluído. Saída em: {output_dir}")


if __name__ == "__main__":
    main()
