import argparse
import pandas as pd
from pathlib import Path


def coerce_numeric(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.replace(".", "", regex=False)
    s = s.str.replace(",", ".", regex=False)
    s = s.str.replace("\u00A0", "", regex=False)
    s = s.str.strip()
    return pd.to_numeric(s, errors="coerce")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Power BI CSVs")
    parser.add_argument("--input", required=True, help="CSV consolidado (_all_tables.csv)")
    parser.add_argument("--output", required=True, help="Relatório de validação")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    df = pd.read_csv(input_path, low_memory=False)

    total_rows = len(df)
    lines = []
    lines.append(f"Arquivo: {input_path}")
    lines.append(f"Linhas: {total_rows}")
    lines.append(f"Colunas: {len(df.columns)}")
    lines.append("")

    lines.append("== Colunas com muitos nulos (>=50%) ==")
    for col in df.columns:
        null_pct = df[col].isna().mean()
        if null_pct >= 0.5:
            lines.append(f"- {col}: {null_pct:.1%}")
    lines.append("")

    lines.append("== Colunas numéricas potenciais (>=70% conversível) ==")
    for col in df.columns:
        series = df[col]
        if series.dtype == "object":
            numeric = coerce_numeric(series)
            ratio = numeric.notna().mean()
            if ratio >= 0.7:
                non_numeric = series[numeric.isna() & series.notna()].astype(str)
                sample = ", ".join(non_numeric.unique()[:5])
                lines.append(f"- {col}: {ratio:.1%} numérico | exemplos não numéricos: {sample}")
    lines.append("")

    lines.append("== Colunas com data possível (>=80% conversível) ==")
    for col in df.columns:
        series = df[col]
        if series.dtype == "object":
            dt = pd.to_datetime(series, errors="coerce", dayfirst=True)
            ratio = dt.notna().mean()
            if ratio >= 0.8:
                lines.append(f"- {col}: {ratio:.1%} data")
    lines.append("")

    lines.append("== Colunas com texto longo (len média >= 50) ==")
    for col in df.columns:
        series = df[col]
        if series.dtype == "object":
            avg_len = series.dropna().astype(str).str.len().mean()
            if avg_len and avg_len >= 50:
                lines.append(f"- {col}: média {avg_len:.0f} caracteres")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Relatório gerado em: {output_path}")


if __name__ == "__main__":
    main()
