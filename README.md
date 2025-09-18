# Background Remover App

Aplicacion de escritorio construida con Flet para Windows que elimina el fondo de imagenes usando la libreria rembg. El flujo esta pensado para procesar lotes completos de archivos y organizar los resultados en carpetas con sello de tiempo.

## Caracteristicas
- Interfaz grafica en Flet con tema oscuro optimizada para pantallas 16:9
- Seleccion multiple de imagenes PNG, JPG, JPEG y BMP
- Carpeta de salida configurable o uso de un destino por defecto (`Carpeta_Stream`)
- Barra de progreso y mensajes de estado durante el procesamiento
- Crea nuevas imagenes procesadas y resguardo de los originales en subcarpetas

## Requisitos previos
- Python 3.12 instalado y accesible desde la terminal
- `pip` 24+ (incluido en Python 3.12)
- (Opcional) [uv](https://docs.astral.sh/uv/) para manejar dependencias mas rapido

## Instalacion (uv recomendado)
```powershell
# 1. Clona el repositorio
git clone https://github.com/pabloacalvo/BackgroundDeletePCApp.git
cd BackgroundDeletePCApp

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv .venv
.\.venv\Scripts\activate

# 3. Instala dependencias declaradas en pyproject.toml
pip install --upgrade pip
pip install -e .
```
Si preferis usar `uv`, reemplaza los dos ultimos comandos por:
```powershell
pip install uv
uv sync
```

## Ejecucion
```powershell
python Remover_background_UI.py
```
Flet abrira una ventana de la aplicacion. No es necesario lanzar un servidor adicional.

## Como usarla
1. Marca la casilla **Usar carpeta por defecto** si quieres que los resultados se guarden dentro de `Carpeta_Stream` en la misma ruta de origen.
2. Si prefieres otra ubicacion, desmarca la casilla e introduce una ruta en **Carpeta de salida personalizada**.
3. Pulsa **Seleccionar Imagen** y elige uno o varios archivos admitidos.
4. Revisa el listado de archivos seleccionados y, cuando estes conforme, presiona **Remover fondos**.
5. Sigue el avance en la barra de progreso. Al finalizar se mostrara un dialogo de exito.

Cada ejecucion crea una carpeta fechada (por ejemplo `2025-09-15_00_00-30`) dentro de la carpeta de salida. Adentro encontraras:
- Las imagenes procesadas sin fondo
- Un subdirectorio `originals` con los archivos originales movidos desde la carpeta fuente

## Consejos y solucion de problemas
- La primera ejecucion de `rembg` puede tardar unos segundos adicionales mientras se carga el modelo ONNX.
- Verifica que tengas permisos de escritura en la carpeta de salida seleccionada.
- Si planeas procesar imagenes muy grandes, asegurate de contar con suficiente memoria RAM disponible.
- Para restablecer la interfaz tras un error, presiona **OK** en el dialogo y vuelve a lanzar el proceso.

## Estructura del proyecto
```
BackgroundDeletePCApp/
|-- Remover_background_UI.py      # UI principal en Flet
|-- utils/
|   `-- backgroud_remove.py       # Logica de eliminacion de fondo y manejo de carpetas
|-- pyproject.toml                # Metadatos y dependencias
`-- README.md                     # Documentacion del proyecto
```

