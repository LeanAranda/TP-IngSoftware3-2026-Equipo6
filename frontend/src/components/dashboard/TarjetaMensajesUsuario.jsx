import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import './TarjetaMensajesUsuario.css';

export default function TarjetaMensajesUsuario({ graficoUsuarios }) {
    const usuariosData = useMemo(() => {
        return Object.entries(graficoUsuarios).map(([usuario, cantidad]) => ({
            usuario,
            cantidad
        }));
    }, [graficoUsuarios]);

    return (
        <div className="tarjeta">
            <h3 className="tarjeta-titulo">📊 Mensajes por Usuario</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={usuariosData} margin={{ top: 10, right: 10, left: -20, bottom: 60 }}>
                    <XAxis
                        dataKey="usuario"
                        angle={-35}
                        textAnchor="end"
                        height={70}
                        tickLine={false}
                        axisLine={false}
                        className="eje-x-usuarios"
                    />
                    <YAxis
                        tickLine={false}
                        axisLine={false}
                        className="eje-y-usuarios"
                    />
                    <Tooltip />
                    <Bar dataKey="cantidad" fill="#8884d8" radius={[4, 4, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}