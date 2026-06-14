import React, { useMemo } from 'react';
import { PieChart, Pie, Tooltip, ResponsiveContainer, Legend } from "recharts";
import './TarjetaFranjasHorarias.css';

export default function TarjetaFranjasHorarias({ horarios }) {
    const horariosData = useMemo(() => {
        return Object.entries(horarios).map(([franja, cantidad]) => ({
            franja,
            cantidad
        }));
    }, [horarios]);

    return (
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
                        innerRadius={50} 
                        outerRadius={80}
                        paddingAngle={3}
                        fill="#82ca9d"
                    />
                    <Tooltip />
                    <Legend 
                        verticalAlign="bottom" 
                        height={36} 
                        iconType="circle" 
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}