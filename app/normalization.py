# app/normalization.py
from app.parsers import (
    parse_episode_header, parse_text_sections, parse_frases_destacadas,
    parse_lectura, parse_cine, parse_personalidades, parse_series_tv,
    parse_diccionario, parse_simple_object, parse_contact_section,
    parse_call_to_action
)

def normalize_full_episode(full_data: dict) -> dict:
    normalized = {}
    for key, content in full_data.items():
        key_lower = key.lower()
        if key_lower.startswith("episodio") and "reporte minoritario" in key_lower:
            normalized["episode_header"] = parse_episode_header(content)
        elif key_lower.startswith("análisis detallado"):
            normalized["analisis_detallado"] = parse_text_sections(content)
        elif key_lower.startswith("frases destacadas"):
            normalized["frases_destacadas"] = parse_frases_destacadas(content)
        elif key_lower.startswith("lectura"):
            normalized["lectura"] = parse_lectura(content)
        elif key_lower.startswith("cine"):
            normalized["cine"] = parse_cine(content)
        elif key_lower.startswith("personalidades"):
            normalized["personalidades"] = parse_personalidades(content)
        elif key_lower.startswith("series de tv"):
            normalized["series_de_tv"] = parse_series_tv(content)
        elif key_lower.startswith("diccionario del episodio"):
            normalized["diccionario"] = parse_diccionario(content)
        elif key_lower.startswith("mapa conceptual"):
            normalized["mapa_conceptual"] = parse_simple_object(content)
        elif key_lower.startswith("¿faltó algo"):
            normalized["sugerencias"] = parse_contact_section(content)
        elif key_lower.startswith("¡seguí con proyecto porrini!"):
            normalized["proyecto_porrini"] = parse_call_to_action(content)
        elif key_lower.startswith("¡descubrí california secreta!"):
            normalized["california_secreta"] = parse_call_to_action(content)
        else:
            normalized[key] = content.strip()
    return normalized
