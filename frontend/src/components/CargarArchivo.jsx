import { useState } from 'react'
import './CargarArchivo.css'
export default function CargaArchivo({ onResultados }) {
    const [file, setFile] = useState(null)
    const [loading, setLoading] = useState(false)
    const [isDragging, setIsDragging] = useState(false)
    const [error, setError] = useState(null)

// Manejadores de Drag & Drop
    const handleDragOver = (e) => {
        e.preventDefault()
        setIsDragging(true)
    }

    const handleDragLeave = (e) => {
        e.preventDefault()
        setIsDragging(false)
    }

    const handleDrop = (e) => {
        e.preventDefault()
        setIsDragging(false)
        setError(null)
        
        const droppedFile = e.dataTransfer.files[0]
        if (droppedFile && droppedFile.name.endsWith('.zip')) {
            setFile(droppedFile)
        } else {
            setError("Por favor, asegúrate de subir un archivo con formato .zip")
        }
    }

    const handleFileChange = (e) => {
        setError(null)
        const selectedFile = e.target.files[0]
        if (selectedFile) setFile(selectedFile)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!file) return

        setLoading(true)
        setError(null)
        
        const formData = new FormData()
        formData.append('archivo', file)

        try {
            const res = await fetch('http://localhost:8000/api/analizar', {
                method: 'POST',
                body: formData
            })

            if (!res.ok) {
                const errorJson = await res.json()
                const mensajeBackend = errorJson.detail || 'Error desconocido del servidor'
                throw new Error(mensajeBackend)
            }

            const data = await res.json()
            onResultados(data) 
        } catch (error) {
            console.error("Error detallado:", error)
            // VALIDACIÓN INTELIGENTE:
            // Si el error contiene la palabra 'fetch' o 'NetworkError', sabemos que el servidor está caído
            if (error.message.includes('fetch') || error.message.includes('NetworkError')) {
                setError("🔌 No se pudo establecer conexión con el servidor. Por favor, verifica que el backend de Python esté encendido.")
            } else {
                // Si no es un error de red, significa que es el error semántico (400, 422, 500) 
                // que capturamos en el 'throw new Error(mensajeBackend)' de arriba
                setError(error.message)
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="cuerpo-formulario">
            
            {/* Zona de Drag & Drop interactiva */}
            <div 
                className={`zona-carga ${isDragging ? 'zona-carga-activa' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    accept=".zip"
                    id="file-upload"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                />
                <label htmlFor="file-upload" className="zona-carga-label">
                    <span className="file-icon">{file ? '📦' : '📁'}</span>
                    
                    <span className="file-label-text">
                        {file ? file.name : 'Haz clic para seleccionar o arrastra tu .zip aquí'}
                    </span>
                    
                    {!file && (
                        <span className="file-hint">
                            Abre WhatsApp {'>'} Info del grupo {'>'} Exportar chat {'>'} Sin archivos
                        </span>
                    )}
                </label>
            </div>

            {/* Mensaje de Error en UI (reemplaza al alert) */}
            {error && <div className="alerta-error">{error}</div>}

            <button type="submit" className="btn-wa" disabled={loading || !file}>
                {loading ? (
                    <span className="flex-centro">
                        <span className="spinner"></span> Analizando chat...
                    </span>
                ) : 'Analizar Chat'}
            </button>
        </form>
    )
}