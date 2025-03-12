import axios from 'axios';

const instance = axios.create({
  baseURL: '127.0.0.1', // 设置你的 API 基础 URL
  timeout: 1000,                      // 请求超时时间
  headers: {'X-Custom-Header': 'foobar'} // 自定义请求头
});

export default instance;