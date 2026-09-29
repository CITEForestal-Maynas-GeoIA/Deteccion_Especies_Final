# Arquitectura y Flujo de Trabajo

Documentación técnica del módulo de detección de especies forestales
en imágenes de dron mediante **LibreYOLO**, desarrollado para el
**CITEforestal Maynas**.

---

## 1. Visión General

El sistema implementa un pipeline de detección de objetos (bounding boxes)
aplicado a imágenes aéreas capturadas por dron. Su propósito es asistir
al personal técnico del CITEforestal Maynas en la identificación y
monitoreo de especies forestales en la Amazonía peruana.

El diseño prioriza:
- **Simplicidad operativa**: un único punto de entrada (`src/detect.py`).
- **Modularidad**: funciones separadas por responsabilidad.
- **Reproducibilidad**: configuración centralizada en `CONFIG`.
- **Extensibilidad**: preparado para georreferenciación y procesamiento batch futuro.

---

## 2. Diagrama de Flujo
┌──────────────────────┐
│ Imágenes de dron │
│ (input_dir) │
└──────────┬───────────┘
│
▼
┌──────────────────────┐
│ Listado y filtrado │
│ por extensión │
└──────────┬───────────┘
│
▼
┌──────────────────────┐
│ Carga del modelo │
│ LibreYOLO (.pt) │
└──────────┬───────────┘
│
▼
┌──────────────────────┐
│ Inferencia por │
│ imagen (bounding │
│ boxes + clases) │
└──────────┬───────────┘
│
▼
┌──────────────────────┐
│ Filtrado por │
│ especies objetivo │
└──────────┬───────────┘
│
▼
┌──────────────────────┐
│ Guardado de │
│ imágenes anotadas │
│ (output_dir) │
└──────────────────────┘

---

## 3. Componentes del Sistema

### 3.1 Entrada (`input_dir`)
- **Fuente**: Directorio con imágenes capturadas por dron.
- **Formatos soportados**: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`.
- **Ruta dummy**: `data/imagenes_dron/`
- **Consideración**: para imágenes multiespectrales o de muy alta resolución,
  puede ser necesario un paso previo de tiling (no incluido en v1).

### 3.2 Modelo de Detección (LibreYOLO)
- **Librería**: [`libreyolo`](https://github.com/LibreYOLO/libreyolo) — licencia MIT.
- **API unificada**: misma interfaz para detección, segmentación y pose.
- **Modelos compatibles**: YOLOv9, RF-DETR, RT-DETR, Dome-DETR, entre otros.
- **Checkpoint**: archivo `.pt` entrenado o fine-tuneado para especies forestales.
- **Ruta dummy**: `models/dummy_species_model.pt`

> **Recomendación técnica**: para detección de objetos pequeños en imágenes
> aéreas (copas individuales), evaluar **Dome-DETR**, optimizado para
> visión aérea / remote sensing.

### 3.3 Inferencia
- Se ejecuta por imagen, de forma **secuencial** en la versión actual.
- Parámetros clave:
  - `conf`: umbral de confianza (`confidence_threshold`, por defecto `0.5`).
  - `save=True`: guarda la imagen con bounding boxes dibujados.
  - `project` / `name`: controlan la ruta de salida.

### 3.4 Post-procesamiento
- **Filtrado por confianza**: aplicado por LibreYOLO vía `conf`.
- **Filtrado por clase**: función `filtrar_por_clases()` — actualmente *stub*
  hasta definir los índices de clase del modelo entrenado.
- **Formato de salida**: imágenes anotadas con bounding boxes y etiquetas.

### 3.5 Salida (`output_dir`)
- **Ruta dummy**: `outputs/detecciones/`
- **Contenido**: imágenes anotadas por cada ejecución.
- **Futuro**: exportación a GeoJSON / shapefile con coordenadas GPS.

---

## 4. Estructura del Repositorio

drone-species-detection/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── src/
│ └── detect.py # Pipeline principal
├── docs/
│ ├── ARQUITECTURA.md # Este documento
│ └── SOSTENIBILIDAD.md # Plan de sostenibilidad
├── models/ # Checkpoints (.pt) - no versionados
├── data/
│ └── imagenes_dron/ # Imágenes de entrada - no versionadas
└── outputs/
└── detecciones/ # Resultados - no versionados


---

## 5. Parámetros de Configuración (`CONFIG`)

| Parámetro              | Descripción                              | Valor dummy                     |
|------------------------|------------------------------------------|---------------------------------|
| `model_path`           | Ruta al checkpoint LibreYOLO             | `models/dummy_species_model.pt` |
| `input_dir`            | Directorio de imágenes de dron           | `data/imagenes_dron/`           |
| `output_dir`           | Directorio de resultados                 | `outputs/detecciones/`          |
| `confidence_threshold` | Umbral mínimo de confianza               | `0.5`                           |
| `target_classes`       | Especies a conservar tras el filtrado    | `["especie_1", ...]`            |
| `image_extensions`     | Extensiones aceptadas                    | `*.jpg, *.png, *.tif, ...`      |

---

## 6. Flujo de Trabajo Recomendado

1. **Adquisición**: vuelo de dron sobre áreas de interés del CITEforestal Maynas.
2. **Organización**: copiar imágenes a `data/imagenes_dron/` con nomenclatura consistente.
3. **Configuración**: editar `CONFIG` en `src/detect.py` con rutas y clases reales.
4. **Ejecución**: `python src/detect.py`.
5. **Revisión**: inspeccionar resultados en `outputs/detecciones/`.
6. **Validación**: contrastar detecciones con verificación en campo.
7. **Retroalimentación**: incorporar correcciones al dataset de re-entrenamiento.

---

## 7. Limitaciones Actuales (v1)

- Modelo dummy sin entrenamiento específico para especies amazónicas.
- Procesamiento secuencial (sin batch inference).
- Ausencia de georreferenciación (sin integración GPS / EXIF).
- Filtrado por clase implementado como *stub*.
- Sin interfaz gráfica ni API REST.

---

## 8. Roadmap Técnico Sugerido

| Fase | Entregable                                              |
|------|---------------------------------------------------------|
| v1.1 | Filtrado real por clase + exportación de detecciones a CSV |
| v1.2 | Procesamiento batch con `multiprocessing`               |
| v1.3 | Georreferenciación desde metadatos EXIF / GPS del dron  |
| v1.4 | Exportación a GeoJSON / shapefile                       |
| v2.0 | API REST o CLI configurable + dashboard de resultados   |

---

## 9. Referencias

- LibreYOLO — https://github.com/LibreYOLO/libreyolo
- OSINFOR / Proyecto ARBOR — monitoreo forestal con IA en Perú
- Dome-DETR — detección de objetos pequeños en imágenes aéreas
