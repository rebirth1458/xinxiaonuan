<script setup>
import { ref, nextTick, computed } from 'vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const inputMsg = ref('')
const activeConversation = ref(0)
const showSidebar = ref(true)

// 对话历史数据
const conversations = ref([
  {
    id: 0,
    title: '新对话',
    lastMessage: '你好，我是信小暖，你的AI助手',
    lastTime: '2024-03-20 09:00:10',
    messages: [
      { 
        id: 1, 
        content: '你好，我是信小暖，你的AI助手。我可以：\n- 回答问题和提供建议\n- 协助编写和优化代码\n- 帮助生成文档和报告\n- 提供学习和工作建议', 
        time: '2024-03-20 09:00:00', 
        sender: 'other',
        tools: [
          { name: '深度思考', icon: 'fas fa-brain' },
          { name: '联网搜索', icon: 'fas fa-search' },
          { name: '代码模式', icon: 'fas fa-code' },
          { name: 'PPT制作', icon: 'fas fa-file-powerpoint' },
          { name: '指令中心', icon: 'fas fa-terminal' }
        ]
      }
    ]
  }
])

// 工具栏选项
const tools = ref([
  { name: '心理测试', icon: 'fas fa-brain' },

])

const currentMessages = computed(() => {
  const conversation = conversations.value.find(c => c.id === activeConversation.value)
  return conversation ? conversation.messages : []
})

const sendMessage = () => {
  if (!inputMsg.value.trim()) {
    ElMessage.warning('不能发送空消息')
    return
  }

  const newMsg = {
    id: currentMessages.value.length + 1,
    content: inputMsg.value.trim(),
    time: dayjs().format('YYYY-MM-DD HH:mm:ss'),
    sender: 'me'
  }

  const conversation = conversations.value.find(c => c.id === activeConversation.value)
  if (conversation) {
    conversation.messages.push(newMsg)
    conversation.lastMessage = newMsg.content
    conversation.lastTime = newMsg.time
  }
  
  inputMsg.value = ''
  
  nextTick(() => {
    const container = document.querySelector('.message-list')
    container.scrollTop = container.scrollHeight
  })
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const switchConversation = (conversationId) => {
  activeConversation.value = conversationId
}

const createNewConversation = () => {
  const newId = conversations.value.length
  conversations.value.push({
    id: newId,
    title: '新对话',
    lastMessage: '',
    lastTime: dayjs().format('YYYY-MM-DD HH:mm:ss'),
    messages: []
  })
  activeConversation.value = newId
}

const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}
</script>

<template>
  <div class="chat-layout">
    <!-- 右侧对话记录 -->
    <div class="nav-sidebar" :class="{ 'nav-sidebar-collapsed': !showSidebar }">
      <div class="nav-header">
        <div class="logo">
          <img src="https://example.com/logo.png" alt="Logo" class="logo-img">
          <span class="logo-text">信小暖</span>
        </div>
        <el-button type="primary" class="new-chat-btn" @click="createNewConversation">
          <i class="fas fa-plus"></i> 新建对话
        </el-button>
      </div>

      <div class="nav-sections">
        <div class="section-title">最近对话</div>
        <div class="conversation-list">
          <div
            v-for="conv in conversations"
            :key="conv.id"
            class="conversation-item"
            :class="{ active: activeConversation === conv.id }"
            @click="switchConversation(conv.id)"
          >
            <i class="fas fa-comments"></i>
            <div class="conversation-info">
              <div class="conversation-title">{{ conv.title }}</div>
              <div class="conversation-preview">{{ conv.lastMessage }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="main-container">
      <div class="chat-header">
        <el-button class="toggle-sidebar" @click="toggleSidebar">
          <i class="fas fa-bars"></i>
        </el-button>
        <div class="header-title">信小暖 AI助手</div>
      </div>

      <div class="chat-container">
        <el-scrollbar class="message-list">
          <div 
            v-for="msg in currentMessages" 
            :key="msg.id"
            class="message-item"
            :class="msg.sender === 'me' ? 'right' : 'left'"
          >
            <el-avatar 
              v-if="msg.sender === 'other'"
              class="avatar"
              :size="40" 
              src="https://example.com/ai-avatar.png"
            />
            <div class="message-content">
              <div class="message-bubble">
                <div class="message-text" v-html="msg.content.replace(/\n/g, '<br>')"></div>

              </div>
              <div class="message-time">{{ dayjs(msg.time).format('HH:mm') }}</div>
            </div>
            <el-avatar 
              v-if="msg.sender === 'me'"
              class="avatar"
              :size="40" 
              src="https://example.com/user-avatar.png"
            />
          </div>
        </el-scrollbar>

        <div class="input-area">
          <div class="tool-bar">
            <div v-for="tool in tools" :key="tool.name" class="tool-item">
              <i :class="tool.icon"></i>
              <span>{{ tool.name }}</span>
            </div>
          </div>
          <div class="input-wrapper">
            <el-input
              v-model="inputMsg"
              type="textarea"
              :rows="3"
              placeholder="输入消息..."
              resize="none"
              @keydown="handleKeydown"
              class="input-box"
            />
            <el-button 
              type="primary" 
              class="send-btn"
              @click="sendMessage"
            >
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
}

.nav-sidebar {
  width: 280px;
  background-color: #fff;
  border-left: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.05);
}

.nav-sidebar-collapsed {
  width: 0;
  overflow: hidden;
}

.nav-header {
  padding: 20px;
  background: linear-gradient(to bottom, #fff, #f9fafc);
  border-radius: 0 0 16px 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.logo-img {
  width: 32px;
  height: 32px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.new-chat-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 10px;
  height: 40px;
}

.nav-sections {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.section-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 12px;
  padding-left: 4px;
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}

.conversation-item:hover {
  background-color: #f5f7fa;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.conversation-item.active {
  background-color: #ecf5ff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.conversation-info {
  flex: 1;
  overflow: hidden;
}

.conversation-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.conversation-preview {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 16px;
  margin: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.chat-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 16px;
  background: linear-gradient(to bottom, #fff, #f9fafc);
  border-radius: 16px 16px 0 0;
}

.toggle-sidebar {
  padding: 8px;
  border: none;
  background: transparent;
}

.header-title {
  flex: 1;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.message-list {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.message-item.left {
  flex-direction: row;
}

.message-item.right {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 80%;
}

.message-bubble {
  padding: 16px;
  border-radius: 16px;
  background-color: #f4f4f5;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-item.right .message-bubble {
  background-color: #ecf5ff;
}

.message-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.message-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  color: #606266;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.tool-item:hover {
  background-color: #fff;
  color: #409eff;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  text-align: right;
}

.input-area {
  padding: 20px;
  background-color: #fff;
  border-radius: 0 0 16px 16px;
}

.tool-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px 0;
}

.input-wrapper {
  display: flex;
  gap: 12px;
}

.input-box {
  flex: 1;
}

.input-box :deep(.el-textarea__inner) {
  border-radius: 12px;
  resize: none;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  border: 1px solid #e4e7ed;
  padding: 12px;
}

.input-box :deep(.el-textarea__inner:focus) {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.send-btn {
  align-self: flex-end;
  height: 40px;
  padding: 0 24px;
  border-radius: 10px;
  transition: all 0.3s;
}

.send-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
}

:deep(.el-scrollbar__bar.is-horizontal) {
  display: none;
}

:deep(.el-scrollbar__bar.is-vertical) {
  width: 6px;
}

:deep(.el-scrollbar__thumb) {
  background-color: #909399;
  opacity: 0.3;
  border-radius: 3px;
}

:deep(.el-scrollbar__thumb:hover) {
  opacity: 0.5;
}
</style>