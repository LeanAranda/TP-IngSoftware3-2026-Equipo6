import React from 'react';
import WordCloud from "./WordCloud";
import './TableroPrincipal.css'
// Componentes modulares
import TarjetaTopEmojis from './TarjetaTopEmojis';
import TarjetaMensajesUsuario from './TarjetaMensajesUsuario';
import TarjetaFranjasHorarias from './TarjetaFranjasHorarias';

export default function TableroPrincipal({ datos, onReiniciar }) {
    return (
        <div className="tablero-container tablero-wrapper">

            {/* Cabecera sin estilos en línea */}
            <div className="flex-entre">
                <h2 className="titulo-principal">Resultados del Análisis</h2>
                <button
                    onClick={onReiniciar}
                    className="btn-wa btn-header"
                >
                    ↻ Analizar otro chat
                </button>
            </div>

            {/* Cuadrícula global */}
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

                {/* Componentes modulares */}
                <TarjetaTopEmojis emojis={datos.emojis} />
                
                <TarjetaMensajesUsuario graficoUsuarios={datos.grafico_usuarios} />
                
                <TarjetaFranjasHorarias horarios={datos.horarios} />

                {/* 6. Nube de Palabras */}
                <div className="tarjeta tarjeta-ancho-total">
                    <h3 className="tarjeta-titulo">☁️ Nube de Palabras</h3>
                    <div className="nube-palabras-container">
                        <WordCloud words={datos.nube_palabras} />
                    </div>
                </div>

            </div>
        </div>
    );
}