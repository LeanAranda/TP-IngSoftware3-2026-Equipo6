# 📊 Frontend - Analizador de Chat de WhatsApp

Este sector del frontend contiene la interfaz modular diseñada para la carga, validación y visualización interactiva de historiales de chat de WhatsApp (`.zip`). 

La interfaz fue estilizada siguiendo un diseño moderno y minimalista (inspirado en herramientas de análisis de datos), ofreciendo una experiencia de usuario limpia, responsiva y con soporte para *Drag & Drop*.

## 💻 Cómo Inicializar y Probar el Proyecto

### 1. Instalar dependencias
Abre una terminal en la raíz de la carpeta del frontend y ejecuta:
```bash
npm install
```

### 2. Verificar el Backend

Asegúrate de tener el servidor de FastAPI corriendo en paralelo (por defecto en `http://localhost:8000`). Esto es vital para que las peticiones del frontend no fallen.

### 3. Iniciar el servidor de desarrollo

Levanta la aplicación de React con Vite ejecutando:
```bash
npm run dev
```

### 4. Abrir la aplicación
Ve a tu navegador e ingresa a la dirección local que te indique la terminal (usualmente 🔗 `http://localhost:5173`).

---

## Uso de la herramienta
* **Carga de Datos:** Arrastra y suelta un archivo `.zip` (que contenga un chat exportado de WhatsApp) sobre la zona de carga, o haz clic para seleccionarlo manualmente.
* **Procesamiento:** Presiona el botón **"Analizar Chat"**. 
* **Exploración:** Al finalizar el procesamiento, la vista cambiará automáticamente al **Tablero Principal**, donde el JSON estructurado cobrará vida a través de gráficos interactivos y una Nube de Palabras dinámica.

---

## Tecnologías de Visualización Implementadas
Para garantizar renderizados fluidos y manejo eficiente del DOM en React 19 se utilizaron:
* **Chart.js / React-Chartjs-2:** Para los reportes analíticos de ranking de usuarios y franjas horarias.
* **d3-cloud:** Motor de renderizado vectorial optimizado para la nube de palabras.