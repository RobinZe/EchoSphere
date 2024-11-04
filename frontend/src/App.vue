<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <div id="app">
    <ResumeMatcher />
  </div>
</template>

<script>
import ResumeMatcher from './components/ResumeMatcher.vue';

export default {
  name: 'App',
  components: {
    ResumeMatcher,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
