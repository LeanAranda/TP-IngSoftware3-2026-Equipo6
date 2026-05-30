import { useState } from 'react'
import './App.css' // <-- Importamos los estilos separados

function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('archivo', file) // Nombre exacto que espera FastAPI

    try {
      const res = await fetch('/api/analizar', {
        method: 'POST',
        body: formData
      })

      if (!res.ok) {
        const errorText = await res.text()
        throw new Error(`Error del servidor (${res.status}): ${errorText}`)
      }

      const data = await res.json()
      setResult(data) // Guardamos la data en el estado para el futuro
    } catch (error) {
      console.error("Error detallado:", error)
      alert(`Error al subir el archivo: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="analyzer-card">
        
        {/* Encabezado */}
        <header className="wp-header">
          <h1>📊 Analizador de Chat WhatsApp</h1>
          <p>Sube tu archivo .zip para procesar las estadísticas</p>
        </header>

        {/* Formulario de Carga */}
        <form onSubmit={handleSubmit} className="form-body">
          <div className="drop-zone">
            <input
              type="file"
              accept=".zip"
              id="file-upload"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ display: 'none' }} // Escondemos el input nativo feo
            />
            <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
              <span className="file-icon">📁</span>
              <span className="file-label-text">
                {file ? file.name : 'Selecciona o arrastra el archivo ZIP del chat'}
              </span>
            </label>
          </div>

          <button type="submit" className="wp-btn" disabled={loading || !file}>
            {loading ? 'Analizando datos...' : 'Subir ZIP'}
          </button>

          {/* Feedback visual temporal de que los datos llegaron bien */}
          {result && (
            <div className="success-alert">
              ✅ ¡Chat procesado con éxito! Datos listos para graficar.
            </div>
          )}
        </form>

      </div>
    </div>
  )
}

export default App