import pandas as pd, json, re, sys
from pathlib import Path

BLOCKS = ["07:30", "09:15", "11:00", "12:45", "14:30", "16:15", "18:00", "19:45", "21:30"]

def norm(x):
    return "" if pd.isna(x) else str(x).strip()

def normalize_time(value):
    s = norm(value)
    if not s:
        return ""
    m = re.match(r"^(\d{1,2}):(\d{2})", s)
    if m:
        return f"{int(m.group(1)):02d}:{int(m.group(2)):02d}"
    try:
        ts = pd.to_datetime(s)
        return ts.strftime("%H:%M")
    except Exception:
        return s

def to_minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)

BLOCKS_MIN = [to_minutes(x) for x in BLOCKS]

def is_double(start_min, end_min):
    occupied = [b for b in BLOCKS_MIN if start_min <= b < end_min]
    return len(occupied) >= 2

def clean_cat(c):
    s = norm(c)
    s = s.lstrip("- ").strip()
    s = re.sub(r'(?i)\b(lic\.?|prof\.?|mg\.?|mga\.?|dr\.?|dra\.?)\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip(" -,\t.")
    if "," in s:
        s = s.split(",")[0].strip(" .,-")
    s = re.sub(r'^[.\-–—\s]+|[.\-–—\s]+$', '', s)
    return s

def aula_num(aula):
    s = norm(aula)
    m = re.search(r"-(\d+)$", s)
    if m:
        return str(int(m.group(1)))
    return s

def convert(xlsx_path, json_path):
    df = pd.read_excel(xlsx_path)
    df.columns = [str(c).strip() for c in df.columns]

    records = []
    for _, row in df.iterrows():
        sede = norm(row.get("Sede")).upper()
        if sede == "SI":
            continue
        if sede == "IND":
            sede = "IN"

        inicio = normalize_time(row.get("Inicio"))
        fin = normalize_time(row.get("Fin"))
        if not inicio or not fin:
            continue

        inicio_min = to_minutes(inicio)
        fin_min = to_minutes(fin)
        tipo = norm(row.get("Tipo"))

        records.append({
            "materia": norm(row.get("Materia")),
            "catedra": clean_cat(row.get("Cátedra")),
            "tipo": tipo,
            "tipoKey": tipo.lower(),
            "profesor": norm(row.get("Profesor")),
            "dia": norm(row.get("Día")).lower(),
            "inicio": inicio,
            "fin": fin,
            "inicioMin": inicio_min,
            "finMin": fin_min,
            "aulaNumero": aula_num(row.get("Aula")),
            "sede": sede,
            "esDoble": is_double(inicio_min, fin_min),
        })

    Path(json_path).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generado {json_path} con {len(records)} registros")

if __name__ == "__main__":
    xlsx = sys.argv[1] if len(sys.argv) > 1 else "pasadas.xlsx"
    out = sys.argv[2] if len(sys.argv) > 2 else "data.json"
    convert(xlsx, out)
