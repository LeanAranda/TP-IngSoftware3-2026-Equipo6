import React, { useEffect, useRef } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";

const WordCloud = ({ words }) => {
    const svgRef = useRef(null);

    useEffect(() => {
        const layout = cloud()
            .size([600, 400]) // tamaño del canvas
            .words(
                words.map((d) => ({
                    text: d.text,
                    size: d.value * 2, // escala del tamaño
                }))
            )
            .padding(5)
            .rotate(() => (Math.random() > 0.5 ? 0 : 90)) // rotación aleatoria
            .font("Impact")
            .fontSize((d) => d.size)
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