# app/parsers.py

def parse_episode_header(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    result = {}
    if not lines:
        return result

    result["titulo"] = lines[0]
    # Extraemos la fecha
    for line in lines:
        if line.startswith("Emitido el:"):
            result["fecha"] = line.replace("Emitido el:", "").strip()
            break
    # Pico de espectadores
    for i, line in enumerate(lines):
        if line.startswith("Pico de"):
            if i + 2 < len(lines):
                result["pico_de_espectadores"] = f"{lines[i+1]} {lines[i+2]}"
            break
    # Marcas de tiempo
    marcas = []
    for i, line in enumerate(lines):
        if "Marcas de tiempo" in line:
            for j in range(i+1, len(lines), 2):
                if j+1 < len(lines):
                    marcas.append({
                        "time": lines[j],
                        "description": lines[j+1]
                    })
            break
    result["marcas_de_tiempo"] = marcas
    return result

def parse_text_sections(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    subsections = {}
    current_header = None
    current_content = []
    header_keywords = {
        "Símbolo discutido", "Resumen", "Repaso de símbolos estudiados",
        "Reflexión sobre la educación contemporánea", "Agradecimientos y balance del año",
        "Diálogo sobre literatura y recomendaciones", "Tabla de contenidos"
    }
    for line in lines:
        if line.endswith(":") or line in header_keywords:
            if current_header:
                subsections[current_header] = "\n".join(current_content)
            current_header = line.rstrip(":")
            current_content = []
        else:
            current_content.append(line)

    if current_header and current_content:
        subsections[current_header] = "\n".join(current_content)
    return subsections

def parse_frases_destacadas(text: str) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("frases destacadas"):
        lines = lines[1:]
    author = None
    if lines and lines[-1].startswith("—"):
        author = lines[-1].lstrip("—").strip()
        phrases = lines[:-1]
    else:
        phrases = lines
    return [{"phrase": phrase, "author": author} for phrase in phrases]

def parse_lectura(text: str) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("lectura"):
        lines = lines[1:]
    entries = []
    i = 0
    while i < len(lines):
        entry = {}
        if i < len(lines):
            entry["titulo"] = lines[i]
            i += 1
        if i < len(lines):
            entry["año"] = lines[i]
            i += 1
        if i < len(lines) and lines[i].startswith("de "):
            entry["autor"] = lines[i][3:].strip()
            i += 1
        desc_lines = []
        while i < len(lines) and "Mencionado en el tiempo" not in lines[i]:
            desc_lines.append(lines[i])
            i += 1
        entry["descripcion"] = " ".join(desc_lines)
        if i < len(lines) and "Mencionado en el tiempo" in lines[i]:
            i += 1
            if i < len(lines):
                entry["tiempo"] = lines[i]
                i += 1
        entries.append(entry)
    return entries

def parse_cine(text: str) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("cine"):
        lines = lines[1:]
    entries = []
    i = 0
    while i < len(lines):
        entry = {}
        if i < len(lines):
            entry["titulo"] = lines[i]
            i += 1
        if i < len(lines) and (lines[i].isdigit() or "-" in lines[i]):
            entry["año"] = lines[i]
            i += 1
        if i < len(lines) and lines[i].startswith("de "):
            entry["director"] = lines[i][3:].strip()
            i += 1
        desc_lines = []
        while i < len(lines) and "Mencionado en el tiempo" not in lines[i]:
            desc_lines.append(lines[i])
            i += 1
        entry["descripcion"] = " ".join(desc_lines)
        if i < len(lines) and "Mencionado en el tiempo" in lines[i]:
            i += 1
            if i < len(lines):
                entry["tiempo"] = lines[i]
                i += 1
        entries.append(entry)
    return entries

def parse_personalidades(text: str) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("personalidades"):
        lines = lines[1:]
    entries = []
    i = 0
    while i < len(lines):
        entry = {}
        if i < len(lines):
            entry["nombre"] = lines[i]
            i += 1
        if i < len(lines):
            entry["lifespan"] = lines[i]
            i += 1
        desc_lines = []
        while i < len(lines) and not lines[i].startswith("Mencionado en el tiempo"):
            desc_lines.append(lines[i])
            i += 1
        entry["descripcion"] = " ".join(desc_lines)
        if i < len(lines) and lines[i].startswith("Mencionado en el tiempo"):
            i += 1
            if i < len(lines):
                entry["tiempo"] = lines[i]
                i += 1
        entries.append(entry)
    return entries

def parse_series_tv(text: str) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("series de tv"):
        lines = lines[1:]
    entries = []
    i = 0
    while i < len(lines):
        entry = {}
        if i < len(lines):
            entry["titulo"] = lines[i]
            i += 1
        if i < len(lines):
            entry["años"] = lines[i]
            i += 1
        desc_lines = []
        while i < len(lines) and "Mencionado en el tiempo" not in lines[i]:
            desc_lines.append(lines[i])
            i += 1
        entry["descripcion"] = " ".join(desc_lines)
        if i < len(lines) and "Mencionado en el tiempo" in lines[i]:
            i += 1
            if i < len(lines):
                entry["tiempo"] = lines[i]
                i += 1
        entries.append(entry)
    return entries

def parse_diccionario(text: str) -> list:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0].lower().startswith("diccionario del episodio"):
        lines = lines[1:]
    entries = []
    i = 0
    while i < len(lines):
        entry = {}
        if i < len(lines):
            entry["termino"] = lines[i]
            i += 1
        def_lines = []
        while i < len(lines) and not lines[i].startswith("Ejemplo:"):
            def_lines.append(lines[i])
            i += 1
        entry["definicion"] = " ".join(def_lines)
        if i < len(lines) and lines[i].startswith("Ejemplo:"):
            i += 1
            ex_lines = []
            while i < len(lines) and not lines[i].startswith("Etimología:"):
                ex_lines.append(lines[i])
                i += 1
            entry["ejemplo"] = " ".join(ex_lines)
        if i < len(lines) and lines[i].startswith("Etimología:"):
            i += 1
            et_lines = []
            while i < len(lines) and "Mencionado en el tiempo" not in lines[i]:
                et_lines.append(lines[i])
                i += 1
            entry["etimologia"] = " ".join(et_lines)
        if i < len(lines) and "Mencionado en el tiempo" in lines[i]:
            i += 1
            if i < len(lines):
                entry["tiempo"] = lines[i]
                i += 1
        entries.append(entry)
    return entries

def parse_simple_object(text: str) -> str:
    return text.strip()

def parse_contact_section(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    result = {}
    if lines and lines[0].lower().startswith("¿faltó algo"):
        lines = lines[1:]
    result["mensaje"] = lines[0] if lines else ""
    for line in lines:
        if line.startswith("@"):
            result["twitter"] = line
        if "@" in line and "gmail" in line:
            result["email"] = line
    return result

def parse_call_to_action(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    result = {}
    if lines:
        result["titulo"] = lines[0]
    if len(lines) > 1:
        result["mensaje"] = lines[1]
    if len(lines) > 2:
        result["accion"] = lines[2]
    return result
