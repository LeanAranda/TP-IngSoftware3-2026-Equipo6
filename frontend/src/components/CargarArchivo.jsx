import { useState } from 'react'

export default function CargaArchivo({ onResultados }) {
    const [file, setFile] = useState(null)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!file) return

        setLoading(true)
        const formData = new FormData()
        formData.append('archivo', file)

        try {
            const res = await fetch('http://localhost:8000/api/analizar', {
                method: 'POST',
                body: formData
            })

            if (!res.ok) {
                const errorText = await res.text()
                throw new Error(`Error del servidor (${res.status}): ${errorText}`)
            }

            const data = await res.json()
            onResultados(data) // Pasamos los datos al componente App
        } catch (error) {
            console.error("Error detallado:", error)
            alert(`Error al subir el archivo: ${error.message}`)
        } finally {
            setLoading(false)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="cuerpo-formulario">
            <div className="zona-carga">
                <input
                    type="file"
                    accept=".zip"
                    id="file-upload"
                    onChange={(e) => setFile(e.target.files[0])}
                    style={{ display: 'none' }}
                />
                <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
                    <span className="file-icon">📁</span>
                    <span className="file-label-text">
                        {file ? file.name : 'Selecciona o arrastra el archivo ZIP del chat'}
                    </span>
                </label>
            </div>

            <button type="submit" className="btn-wa" disabled={loading || !file}>
                {loading ? 'Analizando datos...' : 'Subir ZIP'}
            </button>
        </form>
    )
}