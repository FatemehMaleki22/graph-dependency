<template>
  <div id="app">
    <h1>Graph Visualization</h1>
    <Graph />
  </div>
</template>

<script setup>
import Graph from './components/Graph.vue';
</script>

<style>

#app {
  padding: 20px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 2px;
}
</style>
