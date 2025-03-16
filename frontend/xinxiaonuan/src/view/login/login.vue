<template>
    <div class="container">
        <div class="login-wrapper">
            <div class="header">欢迎来到信小暖</div>
            <div class="form-wrapper">
                <form :model="loginForm" :rules="loginRules" ref="loginFormRef">
                    <input 
                        v-model="loginForm.username"
                        type="text" 
                        name="username" 
                        placeholder="用户名" 
                        class="input-item"
                    >
                    <input 
                        v-model="loginForm.password"
                        type="password" 
                        name="password" 
                        placeholder="密码" 
                        class="input-item"
                    >
                    <div class="btn" @click="handleLogin">登录</div>
                    <div class="register-link">
                        <router-link to="/register">还没有账号？点击注册</router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import qs from 'qs';
import requestUtil from '../../plugins/axios'; // 根据实际情况调整路径
import router from '../../router/index'
const loginForm = ref({
    username: '',
    password: ''
});

const errors = ref({
    username: '',
    password: ''
});

function validateForm() {
    let valid = true;

    if (!loginForm.value.username) {
        errors.value.username = '用户名不能为空';
        valid = false;
    } else {
        errors.value.username = '';
    }

    if (!loginForm.value.password) {
        errors.value.password = '密码不能为空';
        valid = false;
    } else {
        errors.value.password = '';
    }

    return valid;
}

async function handleLogin() {
    // 清除之前的错误信息
    errors.value.username = '';
    errors.value.password = '';
    //requestUtil.post("user/login?"+qs.stringify(loginForm.value)
    if (validateForm()) {
        try {
            // 发送登录请求
            let result = await requestUtil.post("user/login?"+qs.stringify(loginForm.value))
            let data = result.data;
            console.log(data)
            if (data.code == 200) {
                console.log('成功:', "登录成功");
                window.sessionStorage.setItem("token", data.token);
                window.sessionStorage.setItem("user",JSON.stringify(data.user))
                // 可能还需要进行页面跳转或其他操作
                router.replace('/xiaonuan')
            } else {
                alert('错误:', "登录失败: " + data.message);
            }
        } catch (error) {
            alert("用户名或密码不正确");
        }
    } else {
        alert("用户名与密码不能为空");
    }
}
</script>

<style scoped>

html {
    height: 100%;
}
body {
    height: 100%;
}
.container {
    /* margin-top: 5%; */
    height: 980px;
    width: 100%;
    background-image: linear-gradient(to right, #fbc2eb, #a6c1ee);
}
.login-wrapper {
    background-color: #fff;
    width: 358px;
    height: 588px;
    border-radius: 15px;
    padding: 0 50px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
.header {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
    line-height: 200px;
}
.input-item {
    display: block;
    width: 100%;
    margin-bottom: 20px;
    border: 0;
    padding: 10px;
    border-bottom: 1px solid rgb(128, 125, 125);
    font-size: 15px;
    outline: none;
}
.input-item:placeholder {
    text-transform: uppercase;
}
.btn {
    text-align: center;
    padding: 10px;
    margin: 0 auto;
    width: 100%;
    margin-top: 40px;
    background-image: linear-gradient(to right, #a6c1ee, #fbc2eb);
    color: #fff;

    cursor: pointer;
}
.msg {
    text-align: center;
    line-height: 88px;
}
a {
    text-decoration-line: none;
    color: #abc1ee;
}
.register-link {
    text-align: center;
    margin-top: 20px; 
}

.register-link a {
    color: #666; 
    font-size: 14px; 
    text-decoration: none; 
}

.register-link a:hover {
    color: #ff6f61; 
    text-decoration: underline; 
}
</style>