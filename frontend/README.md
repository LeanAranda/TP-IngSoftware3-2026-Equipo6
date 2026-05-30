# 📊 Frontend - Componente de Carga y Procesamiento de Chats

Este sector del frontend contiene la interfaz modular diseñada para la carga, validación y envío de archivos de historial de chat de WhatsApp (`.zip`) hacia el backend desarrollado en FastAPI.

La interfaz fue estilizada siguiendo la identidad visual y paleta de colores característica de **WhatsApp Web**, ofreciendo una experiencia de usuario limpia, intuitiva y responsiva.

## 💻 Cómo Probar esta Funcionalidad

1.  Asegúrate de tener el backend de FastAPI corriendo en su respectivo puerto (ej: `http://localhost:8000`).
2.  Verifica que el archivo `vite.config.js` tenga configurado el proxy apuntando a la dirección local de tu backend para resolver las rutas `/api/*`.
3.  Inicia el servidor de desarrollo del frontend:
3. Instala las dependencias necesarias del proyecto ejecutando:
   ```bash
   npm install
   ```
   Inicia el servidor de desarrollo del frontend:
    ```bash
    npm run dev
    ```
4.  Selecciona un archivo `.zip` que contenga un chat exportado de WhatsApp (Android o iOS) y presiona **"Subir ZIP"**. 
5.  5. Abre tu navegador en la dirección local del frontend: `http://localhost:5173`.
Al finalizar el análisis, el componente mostrará un mensaje de éxito indicando que el estado `result` ya contiene el JSON estructurado con métricas (usuarios top, emojis, franjas horarias y nube de palabras), quedando listo para la fase de graficación.