import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";

const WordCloud = ({ words }) => {
    const svgRef = useRef(null);

    const scale = d3.scaleLinear()
        .domain([d3.min(words, d => d.value), d3.max(words, d => d.value)]) // valores reales
        .range([10, 65]); // rango fijo de tamaños en px


    useEffect(() => {
        const layout = cloud()
            .size([600, 400]) // tamaño del canvas
            .words(
                words
                    .sort((a, b) => b.value - a.value)
                    .slice(0, 100)
                    .map((d) => ({
                        text: d.text,
                        size: scale(d.value) // siempre entre 10 y 65
                    }))
            )
            .padding(5)
            .rotate(() => (Math.random() > 0.5 ? 0 : 90)) // rotación aleatoria
            .font("Impact")
            .fontSize(d => Math.min(d.size, 80)) // límite máximo
            .on("end", draw);

        layout.start();

        function draw(words) {
            const svg = d3.select(svgRef.current)
                .attr("viewBox", `0 0 ${layout.size()[0]} ${layout.size()[1]}`)
                .attr("preserveAspectRatio", "xMidYMid meet")
                .style("width", "100%")
                .style("height", "100%");


            svg.selectAll("text")
                .data(words)
                .join("text")
                .style("font-family", "Impact")
                .style("fill", () => d3.schemeCategory10[Math.floor(Math.random() * 10)])
                .attr("text-anchor", "middle")
                .attr(
                    "transform",
                    d => `translate(${d.x + layout.size()[0] / 2},${d.y + layout.size()[1] / 2})rotate(${d.rotate})`
                )
                .style("font-size", (d) => `${d.size}px`)
                .text((d) => d.text);
        }
    }, [words]);

    return <svg ref={svgRef}></svg>;
};

export default WordCloud;