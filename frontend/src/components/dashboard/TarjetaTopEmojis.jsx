import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function TarjetaTopEmojis({ emojis }) {
    return (
        <div className="tarjeta">
            <h3 className="tarjeta-titulo">🔥 Top Emojis</h3>
            <ResponsiveContainer width="100%" height={250}>
                <BarChart data={emojis}>
                    <XAxis dataKey="emoji" className="recharts-text" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="cantidad" fill="#ff9800" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}