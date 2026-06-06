import { PieChart, Pie, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function TableroPrincipal({ datos, onReiniciar }) {

    const usuariosData = Object.entries(datos.grafico_usuarios).map(([usuario, cantidad]) => ({
        usuario,
        cantidad
    }));

    const horariosData = Object.entries(datos.horarios).map(([franja, cantidad]) => ({
        franja,
        cantidad
    }));

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

                {/* 3. Top Emojis*/}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">🔥 Top Emojis</h3>
                    <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={datos.emojis}>
                            <XAxis dataKey="emoji" className="recharts-text" />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="cantidad" fill="#ff9800" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* 4. Gráfico de Usuarios */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">📊 Mensajes por Usuario</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={usuariosData}>
                            <XAxis dataKey="usuario" angle={-30} textAnchor="end" height={70} />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="cantidad" fill="#8884d8" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* 5. Gráfico de Horarios */}
                <div className="tarjeta">
                    <h3 className="tarjeta-titulo">⏰ Franjas Horarias</h3>
                    <ResponsiveContainer width="100%" height={250}>
                        <PieChart>
                            <Pie
                                data={horariosData}
                                dataKey="cantidad"
                                nameKey="franja"
                                cx="50%"
                                cy="50%"
                                outerRadius={80}
                                fill="#82ca9d"
                                label={({ name }) => name}
                            />
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
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