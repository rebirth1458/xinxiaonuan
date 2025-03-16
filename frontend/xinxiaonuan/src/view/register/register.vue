<template>
    <div class="container">
            <div class="login-wrapper">
                <div class="header">注册</div>
                <div class="form-wrapper">
                    <input v-model="RegForm.username" type="text" name="username" placeholder="账户" class="input-item">
                    <input v-model="RegForm.password" type="password" name="password" placeholder="密码" class="input-item">
                    <input v-model="RegForm.repassword" type="password" name="repassword" placeholder="再次确认密码" class="input-item">
                    <div @click="handleRegister" class="btn">注册！</div>
                    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
                </div>
            </div>
        </div>
</template>
    
<script setup>
import { ref } from 'vue';
import qs from 'qs';
import requestUtil from '../../plugins/axios'; 
import router from '../../router/index'
const RegForm=ref({
    username: '',
    password: '',
    repassword: ''
})

const errorMsg = ref('');

async function handleRegister() {
    errorMsg.value = '';
    if (!RegForm.value.username || !RegForm.value.password || !RegForm.value.repassword) {
        errorMsg.value = '输入不能为空';
        return;
    }

    if (RegForm.value.password !== RegForm.value.repassword) {
        errorMsg.value = '两次输入的密码不匹配，请重新输入。';
        return;
    }
    try {
        const data= {
            username: RegForm.value.username,
            password: RegForm.value.password
        };
        const response = await requestUtil.post('/user/register', qs.stringify(data));
        if(response.data.code=== 200){
            alert('注册成功！');
            router.push('/login');
        }
    } catch (err) {
        console.error("注册失败", err);
        errorMsg.value = '注册失败，请稍后再试或联系管理员。';
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
    width: 100%;
    margin-top: 40px;
    background-image: linear-gradient(to right, #a6c1ee, #fbc2eb);
    color: #fff;
    margin: 0 auto;
}
.msg {
    text-align: center;
    line-height: 88px;
}
a {
    text-decoration-line: none;
    color: #abc1ee;
}
.error {
    color: red;
    font-size: 12px;
}
</style>