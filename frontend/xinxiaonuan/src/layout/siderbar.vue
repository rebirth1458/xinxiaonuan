<template>
  <div id="app">
    <div class="sidebar">
      <div class="sidebar-header">
        <h1>K</h1>
      </div>
      <ul class="sidebar-list">
        <li v-for="item in menuItems" :key="item.name">
            <router-link :to="{ name: item.name }">
            <i :class="item.icon"></i>
          </router-link>
          <span class="label">{{ item.label }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      menuItems: [
        { name: 'xiaonuan', icon: 'fas fa-home', label: 'Home' },
        { name: 'test', icon: 'fas fa-smile', label: 'test' },
        { name: 'chat', icon: 'fas fa-camera', label: 'chat' },
        // { name: 'grid', link: 'grid.html', icon: 'fas fa-th', label: 'Grid' },
        // { name: 'login', link: 'login.html', icon: 'fas fa-sign-in-alt', label: 'Login' },
        // { name: 'file', link: 'file.html', icon: 'fas fa-file', label: 'File' },
      ]
    };
  }
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.sidebar {
  width: 40px;
  height: 600px;
  background-color: #f8f9fa;
  position: fixed;
  top: 150px;
  left: 20px;
  z-index: 1000;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  text-align: center;
  padding: 1px 0;
  background-color: #343a40;
  color: white;
  border-radius: 10px 10px 0 0;
}

.sidebar-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-list li {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 15%;
  position: relative;
}

.sidebar-list li a {
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: #797b7d;
  width: 100%;
  height: 100%;
}

.label {
  visibility: hidden;
  opacity: 0;
  transition: visibility 0s, opacity 0.5s ease-out;
  white-space: nowrap;
  position: absolute;
  left: 60px;
  top: 50%;
  transform: translateY(-50%);
  background-color: black;
  color: white;
  padding: 5px 10px;
  border-radius: 10px;
  z-index: 1000;
  font-size: 14px;
}

.sidebar-list li:hover .label {
  visibility: visible;
  opacity: 1;
}
</style>