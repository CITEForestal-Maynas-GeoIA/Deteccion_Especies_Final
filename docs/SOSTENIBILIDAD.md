# Plan de Sostenibilidad

Estrategia para garantizar la continuidad técnica, operativa, energética
y económica del sistema de detección de especies con LibreYOLO en el
**CITEforestal Maynas**.

---

## 1. Objetivo

Asegurar que el sistema permanezca operativo, actualizado y alineado con
las necesidades institucionales del CITEforestal Maynas, minimizando su
huella energética y maximizando su impacto en el monitoreo forestal.

---

## 2. Dimensiones de Sostenibilidad

### 2.1 Sostenibilidad Técnica

| Aspecto                  | Acción                                                 | Frecuencia |
|--------------------------|--------------------------------------------------------|------------|
| Actualización LibreYOLO  | Revisar releases en GitHub y actualizar dependencias   | Trimestral |
| Re-entrenamiento         | Incorporar nuevas imágenes anotadas de campo           | Semestral  |
| Validación de precisión  | Evaluar mAP@50 sobre conjunto de test actualizado      | Semestral  |
| Documentación            | Mantener README y `docs/` sincronizados con el código  | Continua   |
| Versionado               | Etiquetar releases con SemVer (`v1.0.0`, `v1.1.0`, …)  | Por release |

### 2.2 Sostenibilidad Operativa

| Aspecto       | Acción                                                                 |
|---------------|------------------------------------------------------------------------|
| Capacitación  | Formar al menos **2 técnicos** en uso y mantenimiento del pipeline     |
| Repositorio   | Alojar en GitHub institucional con control de versiones               |
| Datos         | Política de respaldo de imágenes y checkpoints en almacenamiento NAS  |
| Integración   | Articular con OSINFOR y otras entidades del sector forestal            |
| Documentación | Guía de instalación y troubleshooting accesible al personal técnico   |

### 2.3 Sostenibilidad Energética (Green AI)

El entrenamiento y la inferencia de modelos de visión por computadora
tienen un costo energético no despreciable. Se adoptan prácticas de
**Green AI**:

- **Mixed Precision (AMP)**: reduce consumo energético 20–40 % en GPUs con Tensor Cores.
- **Modelos ligeros**: preferir variantes *nano* / *tiny* cuando la precisión lo permita.
- **Inferencia eficiente**: exportar a ONNX / TensorRT para despliegue en edge.
- **Medición de huella**: integrar [CodeCarbon](https://github.com/mlco2/codecarbon)
  o GreenTensor para monitorear emisiones por ejecución.
- **Reutilización**: evitar re-entrenamientos innecesarios; usar *fine-tuning* selectivo.

### 2.4 Sostenibilidad Económica

| Estrategia         | Descripción                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Software libre     | LibreYOLO es MIT — sin costos de licencia                                   |
| Hardware existente | Aprovechar GPUs disponibles en CITEforestal o cloud gratuito de investigación |
| Datos abiertos     | Contribuir con datasets anotados (previo acuerdo institucional)             |
| Alianzas           | Colaborar con OSINFOR, universidades y proyectos como ARBOR                 |

---

## 3. Indicadores de Sostenibilidad

| Indicador                          | Meta                          |
|------------------------------------|-------------------------------|
| Modelos actualizados por año       | ≥ 2                           |
| Técnicos capacitados activos       | ≥ 2                           |
| Precisión del modelo (mAP@50)      | ≥ 0.80 en especies objetivo   |
| Tiempo de inactividad por fallo    | < 1 semana                    |
| Huella energética por inferencia   | Medida y documentada          |
| Cobertura de documentación         | 100 % de módulos en `src/`    |

---

## 4. Riesgos y Mitigación

| Riesgo                        | Impacto | Mitigación                                            |
|-------------------------------|---------|-------------------------------------------------------|
| Obsolescencia del modelo      | Alto    | Re-entrenamiento periódico con datos nuevos           |
| Pérdida de conocimiento       | Alto    | Documentación técnica + capacitación cruzada          |
| Falta de datos anotados       | Medio   | Convenios con OSINFOR y proyectos de investigación    |
| Costos de cómputo             | Medio   | Modelos ligeros + exportación a formatos eficientes   |
| Rotación de personal técnico  | Medio   | Guías paso a paso y repositorio bien documentado      |
| Cambios en LibreYOLO (API)    | Bajo    | Fijar versiones en `requirements.txt`                 |

---

## 5. Roles y Responsabilidades

| Rol                     | Responsabilidad principal                                   |
|-------------------------|-------------------------------------------------------------|
| Responsable técnico     | Mantener el repositorio, revisar PRs, aprobar releases      |
| Técnico de campo        | Captura de imágenes y validación en terreno                 |
| Anotador de datos       | Etiquetado de bounding boxes para re-entrenamiento          |
| Coordinación CITE       | Gestión de convenios, presupuesto y articulación sectorial  |

