<template>
  <div>
    <input type="text" v-model="filterText" placeholder="Search" class="filter-input" />
    <button @click="filterNodes" class="filter-btn"> {{ isFiltered ? "Clear Filter" : "Filter Nodes" }}</button>
  </div>

  <div class="graph-container">
    <svg id="graph"></svg>
    <div v-if="selectedNode" class="node-info">
      <strong>{{ selectedNode.label }}</strong><br />
      ID: {{ selectedNode.id }}<br />
      Label: {{ selectedNode.label }}<br />
      Group: {{ selectedNode.group }}
    </div>
  </div>
</template>

<script setup>

import { onMounted, ref, computed, watchEffect } from "vue";
import * as d3 from "d3";
import axios from "axios"

const graphContainer = ref(null);
const selectedNode = ref(null)
const filterText = ref("")
const isFiltered = ref(false);

const filteredNodes = computed(() => {
  if (!filterText.value.trim()) return graphContainer.value?.nodes || []
  return graphContainer.value.nodes.filter((node) =>
    node.label.toLowerCase().includes(filterText.value.toLowerCase())
  )
})

onMounted(async () => {
  //graphContainer.value = await d3.json('/src/data/lang-graph.json')
  const response = await axios.get("http://localhost:8001/api/graph")
  graphContainer.value = {
    nodes: response.data.nodes,
    links: response.data.edges.map(e => ({
      source: e.from,
      target: e.to
    }))
  }
  drawGraph()
});

const filterNodes = () => {
  if (isFiltered.value) filterText.value = ''
  isFiltered.value = !isFiltered.value
  d3.select("#graph").selectAll("*").remove()
  drawGraph()
}


const drawGraph = () => {

  const svg = d3.select("#graph")
  svg.attr("width", 800).attr("height", 500)

  const nodes = filteredNodes.value
  const nodeIds = new Set(nodes.map(n => n.id))

  const links = graphContainer.value.links.filter(link => {
    const sourceId = typeof link.source === 'object' ? link.source.id : link.source
    const targetId = typeof link.target === 'object' ? link.target.id : link.target
    return nodeIds.has(sourceId) && nodeIds.has(targetId)
  })

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(400, 300))

  const link = svg.append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", d => d.color || "#aaa")
    .attr("stroke-width", d => d.weight || 1)

  
  const connected = new Map() 
  graphContainer.value?.links.forEach(link => {
    const source = typeof link.source === 'object' ? link.source.id : link.source
    const target = typeof link.target === 'object' ? link.target.id : link.target

    if (!connected.has(source)) connected.set(source, new Set())
    if (!connected.has(target)) connected.set(target, new Set())

    connected.get(source).add(target)
    connected.get(target).add(source)
  })

  const node = svg.append("g")
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 10)
    .attr("fill", d => d.color || "#1f77b4")
    .call(drag(simulation))
    .on("click", (_, d) => {
      selectedNode.value = d

      const highlightIds = new Set([d.id, ...(connected.get(d.id) || [])])
      node
        .attr("fill", n => highlightIds.has(n.id) ? "#ff5722" : "#d3d3d3")

      link
        .attr("stroke", l => {
          const s = typeof l.source === 'object' ? l.source.id : l.source
          const t = typeof l.target === 'object' ? l.target.id : l.target
          return highlightIds.has(s) && highlightIds.has(t) ? "#ff9800" : "#ccc"
        })
        .attr("stroke-width", l => {
          const s = typeof l.source === 'object' ? l.source.id : l.source
          const t = typeof l.target === 'object' ? l.target.id : l.target
          return highlightIds.has(s) && highlightIds.has(t) ? 3 : 1
        })

      label
        .attr("fill", n => highlightIds.has(n.id) ? "black" : "#aaa")
    })

  const label = svg.append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text(d => d.label)
    .attr("font-size", 12)
    .attr("dx", 12)
    .attr("dy", ".35em")

  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y)

    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)

    label
      .attr("x", d => d.x)
      .attr("y", d => d.y)
  })
}
const drag = (simulation) => {
  const dragstarted = (event, d) => {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    d.fx = d.x
    d.fy = d.y
  }
  const dragged = (event, d) => {
    d.fx = event.x
    d.fy = event.y
  }
  const dragended = (event, d) => {
    if (!event.active) simulation.alphaTarget(0)
    d.fx = null
    d.fy = null
  }

  return d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended)

}

</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 500px;
  border: 1px solid #ddd;
  position: relative;
}

.node-info {
  position: absolute;
  top: 20px;
  right: 20px;
  left: 820px;
  padding: 10px;
  background: #f8f8f8;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  width: 200px;
}

.filter-input {
  margin-bottom: 10px;
  padding: 5px 10px;
  font-size: 14px;
  width: 300px;
}

.filter-btn {
  padding: 7px 15px;
  font-size: 14px;
  background-color: #357df2;
  color: white;
  border: none;
  cursor: pointer;
  margin: 5px;
}
</style>
