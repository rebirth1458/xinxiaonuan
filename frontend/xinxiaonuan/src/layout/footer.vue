<script setup>
const copyright = `© ${new Date().getFullYear()} 上立信信小暖团队. 保留所有权利.`;
</script>

<template>
  <footer>
    版本: v1.0.0
    <div class="copyright">
      {{ copyright }}
    </div>
  </footer>
</template>

<style scoped>

footer {
  text-align: center;
  padding: 10px;
}

.copyright {
  margin-top: 5px;
  font-size: 0.875em; 
  color: #6c757d; 
}
</style>