import { useState } from 'react'
import CargaArchivo from './components/CargarArchivo'
import TableroPrincipal from './components/dashboard/TableroPrincipal'
import './App.css'

function App() {
  const [result, setResult] = useState(null)

  return (
    <div className="app-container">
      <div className={`contenedor-principal ${result ? "modo-tablero" : "modo-carga"}`}>
        <header className="cabecera-wa">
          <h1>📊 Analizador de Chat WhatsApp</h1>
          <p>Sube tu archivo .zip para procesar las estadísticas</p>
        </header>

        {/* Renderizado condicional: Si no hay resultado, muestra CargaArchivo. Si lo hay, muestra el Tablero */}
        {!result ? (
          <CargaArchivo onResultados={setResult} />
        ) : (
          <TableroPrincipal 
            datos={result} 
            onReiniciar={() => setResult(null)} 
          />
        )}

      </div>
    </div>
  )
}

export default App