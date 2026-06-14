# ⚙️ Backend - Análisis de WhatsApp

La lógica de procesamiento de datos con Python (FastAPI y Pandas) ya se encuentra implementada y testeada.

## Pasos para inicializar el entorno

### 1. Crear y activar el entorno virtual
Abre una terminal en la raíz del proyecto y ejecuta según tu sistema operativo:

**En Windows (PowerShell):**
```powershell
python -m venv .venv --clear
.\.venv\Scripts\Activate.ps1
```
> 💡 *Si PowerShell arroja un error de políticas, ejecuta primero:* `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

**En Mac / Linux / Git Bash:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias
Abre una terminal en la carpeta donde se encuentran `main.py` y `requirements.txt` y ejecuta:
```bash
pip install -r requirements.txt
```

### 3. Encender el servidor
Una vez instalado todo, levanta el motor de la API con el siguiente comando:

```bash
uvicorn main:app --reload
```
> ⚠️ **Importante:** No cierres esta terminal mientras estés trabajando en React, de lo contrario el backend se apagará y el frontend no podrá consultar los datos.

### 4. Probar la API (Swagger UI)
Con el servidor encendido, ingresa desde tu navegador a la documentación interactiva:
🔗 http://127.0.0.1:8000/docs

Desde allí puedes probar el funcionamiento subiendo un archivo `.zip` real mediante el botón **Try it out**.

---

## 🔌 Datos del Endpoint para el Frontend (React)

Para conectar la interfaz de usuario con este backend, la configuración del consumo debe respetar los siguientes parámetros:

* **URL:** `http://127.0.0.1:8000/api/analizar`
* **Método:** `POST`
* **Formato esperado (Body):** Un objeto `FormData` con un campo clave llamado `archivo` que contenga el archivo `.zip` exportado de WhatsApp.

### Estructura de la respuesta JSON:
La API procesa el chat y devuelve un objeto con la siguiente estructura limpia para renderizar los gráficos:
* `usuario_top`: Nombre del participante con más mensajes.
* `grafico_usuarios`: Diccionario con el Top 5 de usuarios y sus totales.
* `dias_pico`: Top 5 de días con mayor actividad.
* `horarios`: Distribución de mensajes agrupada por franjas horarias (Madrugada, Mañana, Tarde, Noche).
* `emojis`: Top 5 de emojis más usados con sus respectivas frecuencias.
* `nube_palabras`: Array de objetos con el formato `[{"text": "palabra", "value": cantidad}]` listo para usar en librerías de Word Cloud.