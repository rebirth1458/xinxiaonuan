<script setup>
import MyHeader from '../components/header.vue'
import Myfooter from '../components/footer.vue'
import Main from '../components/main.vue'
import siderbar from '../components/siderbar.vue'
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
                <Main></Main>
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
