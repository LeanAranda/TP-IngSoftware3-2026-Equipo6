import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";
import './WordCloud.css'; 

const COLORES_NUBE = [
    '#00a884', 
    '#008f70', 
    '#25D366', 
    '#3b4a54', 
    '#4b5563', 
];

const WordCloud = ({ words }) => {
    const svgRef = useRef(null);
    const [tooltip, setTooltip] = useState({
        visible: false,
        text: "",
        count: 0,
        x: 0,
        y: 0
    });

    useEffect(() => {
        if (!words || words.length === 0) return;

        const scale = d3.scaleLinear()
            .domain([d3.min(words, d => d.value), d3.max(words, d => d.value)]) 
            .range([12, 70]);

        d3.select(svgRef.current).selectAll("*").remove();

        const layout = cloud()
            .size([600, 400]) 
            .words(
                words
                    .sort((a, b) => b.value - a.value)
                    .slice(0, 100)
                    .map((d) => ({
                        text: d.text,
                        size: scale(d.value),
                        value: d.value 
                    }))
            )
            .padding(4)
            .rotate(() => (Math.random() > 0.5 ? 0 : 90)) 
            .font("'-apple-system', 'Segoe UI', Roboto, sans-serif")
            .fontSize(d => d.size)
            .on("end", draw);

        layout.start();

        function draw(words) {
            const svg = d3.select(svgRef.current)
                .attr("viewBox", `0 0 ${layout.size()[0]} ${layout.size()[1]}`)
                .attr("preserveAspectRatio", "xMidYMid meet")
                .attr("class", "wordcloud-svg"); 

            const g = svg.append("g")
                .attr("transform", `translate(${layout.size()[0] / 2},${layout.size()[1] / 2})`);

            g.selectAll("text")
                .data(words)
                .join("text")
                .style("font-family", "'-apple-system', 'Segoe UI', Roboto, sans-serif")
                .style("font-weight", "bold")
                .style("fill", () => COLORES_NUBE[Math.floor(Math.random() * COLORES_NUBE.length)])
                .attr("text-anchor", "middle")
                .attr("transform", d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
                .style("font-size", d => `${d.size}px`)
                .text(d => d.text)
                .style("cursor", "pointer") 
                .style("transition", "opacity 0.2s")
                .on("mouseover", function(event, d) { 
                    d3.select(this).style("opacity", 0.6); 
                })
                .on("mousemove", function(event, d) {
                    setTooltip({
                        visible: true,
                        text: d.text,
                        count: d.value,
                        x: event.clientX + 15, // Usamos clientX para posicionamiento fixed
                        y: event.clientY + 15  // Usamos clientY para posicionamiento fixed
                    });
                })
                .on("mouseout", function() { 
                    d3.select(this).style("opacity", 1);
                    setTooltip(prev => ({ ...prev, visible: false }));
                });
        }
    }, [words]);

    return (
        <div className="wordcloud-wrapper">
            <svg ref={svgRef} className="wordcloud-svg" />
            
            {tooltip.visible && (
                <div 
                    className="wordcloud-tooltip"
                    style={{ 
                        top: tooltip.y, 
                        left: tooltip.x 
                    }}
                >
                    <strong>{tooltip.text}</strong>: {tooltip.count} veces
                </div>
            )}
        </div>
    );
};

export default WordCloud;