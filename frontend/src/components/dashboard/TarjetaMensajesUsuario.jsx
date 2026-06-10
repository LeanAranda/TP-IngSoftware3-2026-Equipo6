import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

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
                <BarChart data={usuariosData}>
                    <XAxis dataKey="usuario" angle={-30} textAnchor="end" height={70} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="cantidad" fill="#8884d8" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}