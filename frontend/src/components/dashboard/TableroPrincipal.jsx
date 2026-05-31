export default function TableroPrincipal({ datos, onReiniciar }) {
    return (
        <div className="tablero-container" style={{ marginTop: '2rem' }}>

            {/* Cabecera usando nuestra clase flex-entre */}
            <div className="flex-entre">
                <h2 style={{ margin: 0, color: 'var(--texto-principal)' }}>Resultados del Análisis</h2>
                <button
                    onClick={onReiniciar}
                    className="btn-wa"
                    style={{ width: 'auto', padding: '0.5rem 1rem', margin: 0 }}
                >
                    ↻ Analizar otro chat
                </button>
            </div>

            {/* Cuadrícula usando la clase global */}
            <div className="grid-tablero">

                {/* 1. Usuario Top */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">🏆 Usuario más activo</h3>
                    <p className="texto-destacado">
                        {datos.usuario_top}
                    </p>
                </div>

                {/* 2. Días Pico */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">📅 Días con más mensajes</h3>
                    <ul className="lista-datos">
                        {Object.entries(datos.dias_pico).map(([fecha, cantidad]) => (
                            <li key={fecha}>
                                <strong>{fecha}</strong>: {cantidad} msjs
                            </li>
                        ))}
                    </ul>
                </div>

                {/* 3. Placeholder: Top Emojis */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">🔥 Top Emojis</h3>
                    <p className="placeholder-grafico">[ Aquí irá la cuadrícula de emojis ]</p>
                </div>

                {/* 4. Placeholder: Gráfico de Usuarios */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">📊 Mensajes por Usuario</h3>
                    <p className="placeholder-grafico">[ Aquí irá el BarChart de Recharts ]</p>
                </div>

                {/* 5. Placeholder: Gráfico de Horarios */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">⏰ Franjas Horarias</h3>
                    <p className="placeholder-grafico">[ Aquí irá el PieChart de Recharts ]</p>
                </div>

                {/* 6. Placeholder: Nube de Palabras (Combinando clases) */}
                <div className="tarjeta tarjeta-ancho-total">
                    <h3 className="tarjeta-titulo">☁️ Nube de Palabras</h3>
                    <p className="placeholder-grafico">[ Aquí irá el componente react-wordcloud ]</p>
                </div>

            </div>
        </div>
    )
}