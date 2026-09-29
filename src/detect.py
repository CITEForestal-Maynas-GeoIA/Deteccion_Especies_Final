"""
Módulo de detección de especies forestales en imágenes de dron.
CITEforestal Maynas - Detección con LibreYOLO.

Este script carga un modelo LibreYOLO, procesa un directorio de imágenes
aéreas capturadas por dron y guarda los resultados con bounding boxes
dibujados sobre cada detección.

Uso:
    python src/detect.py
"""

from pathlib import Path

from libreyolo import LibreYOLO


# ============================================================
# CONFIGURACIÓN DUMMY - REEMPLAZAR CON RUTAS REALES
# ============================================================
CONFIG = {
    # Ruta al modelo pre-entrenado o checkpoint fine-tuneado.
    # Ejemplo real: "models/especies_maynas_v1.pt"
    "model_path": "models/dummy_species_model.pt",

    # Directorio con imágenes de dron a procesar.
    # Formatos soportados: .jpg, .jpeg, .png, .tif, .tiff
    "input_dir": "data/imagenes_dron/",

    # Directorio de salida para imágenes con bounding boxes dibujados.
    "output_dir": "outputs/detecciones/",

    # Confianza mínima para considerar una detección válida (0.0 - 1.0).
    "confidence_threshold": 0.5,

    # Clases de especies a detectar (DUMMY).
    # Reemplazar por especies objetivo reales, ej:
    # ["shihuahuaco", "cedro", "caoba", "tornillo"]
    "target_classes": ["especie_1", "especie_2", "especie_3"],

    # Extensiones de imagen aceptadas.
    "image_extensions": ["*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff"],
}


def cargar_modelo(model_path: str) -> LibreYOLO:
    """
    Carga el modelo LibreYOLO desde la ruta especificada.

    Args:
        model_path: Ruta al checkpoint del modelo (.pt).

    Returns:
        Instancia del modelo LibreYOLO lista para inferencia.

    Raises:
        FileNotFoundError: Si el archivo del modelo no existe.
    """
    if not Path(model_path).exists():
        raise FileNotFoundError(
            f"Modelo no encontrado: {model_path}. "
            "Descargue o entrene un modelo adecuado para especies forestales "
            "y actualice CONFIG['model_path']."
        )

    print(f"Cargando modelo: {model_path}")
    model = LibreYOLO(model_path)
    return model


def listar_imagenes(input_dir: Path, extensiones: list) -> list:
    """
    Recopila todas las imágenes válidas dentro del directorio de entrada.

    Args:
        input_dir: Directorio raíz con las imágenes de dron.
        extensiones: Lista de patrones glob (ej. ["*.jpg", "*.png"]).

    Returns:
        Lista de rutas (Path) a las imágenes encontradas.
    """
    imagenes = []
    for ext in extensiones:
        imagenes.extend(input_dir.glob(ext))
    return sorted(imagenes)


def procesar_imagen(modelo: LibreYOLO, ruta_imagen: Path,
                    output_dir: Path, conf: float):
    """
    Ejecuta detección sobre una imagen individual y guarda el resultado.

    Args:
        modelo: Instancia del modelo LibreYOLO.
        ruta_imagen: Ruta completa a la imagen de entrada.
        output_dir: Directorio donde guardar la imagen anotada.
        conf: Umbral mínimo de confianza.

    Returns:
        Lista de bounding boxes detectados (vacía si no hay detecciones).
    """
    resultados = modelo(
        str(ruta_imagen),
        conf=conf,
        save=True,
        project=str(output_dir),
        name="detecciones",
    )

    # Estructura típica LibreYOLO: resultados[0].boxes contiene .xyxy, .cls, .conf
    detecciones = resultados[0].boxes if resultados else []
    return detecciones


def filtrar_por_clases(detecciones, clases_objetivo: list):
    """
    Filtra detecciones para conservar únicamente las especies de interés.

    NOTA: Implementación dummy. En producción, mapear los índices de clase
    del modelo entrenado a nombres y filtrar por 'clases_objetivo'.

    Args:
        detecciones: Lista de bounding boxes devueltos por el modelo.
        clases_objetivo: Nombres de las especies a conservar.

    Returns:
        Detecciones filtradas.
    """
    # TODO: Implementar filtrado real una vez definidos los índices de clase
    # del modelo entrenado para especies forestales amazónicas.
    return detecciones


def procesar_directorio(config: dict) -> None:
    """
    Procesa todas las imágenes del directorio de entrada de forma secuencial.

    Args:
        config: Diccionario de configuración (ver CONFIG al inicio del módulo).
    """
    input_dir = Path(config["input_dir"])
    output_dir = Path(config["output_dir"])

    if not input_dir.exists():
        print(f"[ERROR] Directorio de entrada no encontrado: {input_dir}")
        print("        Configure la ruta correcta en CONFIG['input_dir'].")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    imagenes = listar_imagenes(input_dir, config["image_extensions"])
    if not imagenes:
        print(f"[INFO] No se encontraron imágenes en {input_dir}.")
        return

    print(f"[INFO] {len(imagenes)} imágenes encontradas. Iniciando detección...\n")

    modelo = cargar_modelo(config["model_path"])

    resumen = {"procesadas": 0, "con_detecciones": 0, "errores": 0}

    for i, img_path in enumerate(imagenes, start=1):
        print(f"[{i}/{len(imagenes)}] {img_path.name}")
        try:
            detecciones = procesar_imagen(
                modelo,
                img_path,
                output_dir,
                config["confidence_threshold"],
            )
            detecciones_filtradas = filtrar_por_clases(
                detecciones, config["target_classes"]
            )

            n = len(detecciones_filtradas)
            print(f"    -> {n} detección(es)")

            resumen["procesadas"] += 1
            if n > 0:
                resumen["con_detecciones"] += 1

        except Exception as e:
            print(f"    [ERROR] {e}")
            resumen["errores"] += 1

    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)
    print(f"Procesadas   : {resumen['procesadas']}")
    print(f"Con detecc.  : {resumen['con_detecciones']}")
    print(f"Errores      : {resumen['errores']}")
    print(f"Salida       : {output_dir}")


def main() -> None:
    """Punto de entrada principal del script."""
    print("=" * 50)
    print("CITEforestal Maynas - Detección de Especies")
    print("LibreYOLO + Imágenes de Dron")
    print("=" * 50)
    print("[AVISO] Usando configuración DUMMY.")
    print("        Adaptar CONFIG con rutas y clases reales.\n")

    procesar_directorio(CONFIG)


if __name__ == "__main__":
    main()
