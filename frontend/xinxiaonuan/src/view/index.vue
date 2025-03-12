<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import MyHeader from '../layout/header.vue'
import Myfooter from '../layout/footer.vue'
import Main from '../layout/main.vue'
import siderbar from '../layout/siderbar.vue'
const route = useRoute();
let isHomeRoute = ref(route.path === '/xiaonuan');
// 监听路由变化，更新 isHomeRoute
watch(
  () => route.path,
  (newPath) => {
    isHomeRoute.value = newPath === '/xiaonuan';
  }
);
</script>

<template>
    <el-container>
      <el-header>
        <MyHeader></MyHeader>
      </el-header>
      <el-container>
        <el-aside width="200px">
            <siderbar></siderbar>
        </el-aside>
        <el-container>
            <el-main>
                <Main v-if="!isHomeRoute"></Main>
                <div v-else>
                    <h1>欢迎来到主页</h1>
                    <p>这里是你的主页信息。</p>
                </div>
            </el-main>
            <el-footer>
                <Myfooter></Myfooter>
            </el-footer>
        </el-container>
      </el-container>
    </el-container>
   
</template>

<style scope>
.el-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.common-layout{
    height: 100%;
}
</style>
