<p align="center">
<img src="./img/unla.png" alt="Logo UNLa" width="200"/>
</p>

# 📊 Analizador Estadístico de Chats de WhatsApp (Equipo 6)
**Universidad Nacional de Lanús (UNLa)**  
**Cátedra:** Ingeniería de Software 3  
**Profesor:** Nicolás Pérez  

---

### 👥 Integrantes

| Nombre Completo | Usuario GitHub | Rol Principal |
| :--- | :--- | :--- |
| **Anahí Maitén Mansilla** | [Anahimm](https://github.com/Anahimm) | Tester / Dev |
| **Diego David Fernandez** | [fernandezDiegoDavid](https://github.com/fernandezDiegoDavid) | Ingeniería / Backend |
| **Leandro Aranda** | [LeanAranda](https://github.com/LeanAranda) | PM / Dev |
| **Lucas Alberto Encinas** | [LucasEncinas](https://github.com/LucasEncinas) | Frontend / UI |

---

Aplicación integral para el análisis de interacciones en grupos de WhatsApp a partir de archivos `.zip`.

> [!IMPORTANT]
> **Enfoque de Ingeniería de Software 3:** Este proyecto demuestra un proceso **Gestionado (CMMI Nivel 4)**, priorizando la trazabilidad desde la WBS hasta los commits atómicos en GitHub.

## 📥 Clonación del Repositorio
Para comenzar, clona el proyecto en tu máquina local e ingresa a la carpeta raíz:
```bash
git clone https://github.com/LeanAranda/TP-IngSoftware3-2026-Equipo6.git
cd TP-IngSoftware3-2026-Equipo6
```

## 🛠️ Arquitectura y Decisiones Técnicas
Se optó por una arquitectura desacoplada **Backend (FastAPI) + Frontend (React)** para garantizar la independencia de procesos.

1. **Backend (Python 3.x + Pandas):** Elegido por su eficiencia en el manejo de estructuras de datos (DataFrames) y procesamiento semántico mediante **SpaCy** (con descarga automatizada del modelo `es_core_news_sm`).
2. **Frontend (React 19 + Vite):** Seleccionado para una visualización dinámica. Ante conflictos de librerías, se migró a **d3-cloud** (Commit `4346aa3`) para asegurar compatibilidad.
3. **Gestión de Errores:** Implementación de contratos mediante `HTTPException` para asegurar una comunicación robusta entre capas.

## 📈 Trazabilidad del Proyecto
Utilizamos **Kanban** y una estrategia de **Feature Branching** para vincular cada tarea con una evidencia física de desarrollo.

| Tarea WBS | Actividad | Responsable | Hash de Commit Clave |
| :--- | :--- | :--- | :--- |
| **1.2** | Parsing y Modularización | Ana / Diego | `331404a` / `2a4a2e0` |
| **2.1** | Estadísticas Avanzadas | Ana / Diego | `6fe4b34` / `3d0ec08` |
| **2.2** | UI y Gráficos Dinámicos | Lean / Lucas | `f8874ce` / `a98f6e7` |
| **2.3.2** | Gestión de Errores | Diego | `4533b1f` / `dadea2e` |

---

## 🚀 Guía de Instalación Rápida
*Cada capa cuenta con documentación detallada para su despliegue dentro de sus respectivas carpetas.*

*   **Para inicializar el Servidor:** Ingrese a la carpeta de la API y siga las instrucciones de su entorno virtual: [README de Backend](./backend/README.md)
*   **Para inicializar la Interfaz:** Ingrese a la carpeta del Dashboard e instale los paquetes de Node: [README de Frontend](./frontend/README.md)
