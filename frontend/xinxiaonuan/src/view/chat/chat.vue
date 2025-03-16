<template>
  <el-container class="chat-container">
    <el-container class="main-content">
      <el-main class="main-area">
        <div class="content-with-sidebar">
          <div class="message-area">
            <div class="message-list">
              <div v-for="message in currentSessionMessages" :key="message.content" 
                   :class="['message-item', message.type === 'human' ? 'message-human' : 'message-ai']">
                <div class="message-content">
                  {{ message.content }}
                  <span v-if="message.isTyping" class="typing-indicator">▋</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="integrated-sidebar">
            <div class="sidebar-header bubble-card">
              <el-button type="primary" class="new-chat-btn bubble-button" @click="createNewChat">
                <Plus class="icon" />
                新建对话
              </el-button>
              <el-button circle class="bubble-icon-button">
                <Search class="icon" />
              </el-button>
            </div>
            
            <el-scrollbar height="calc(100% - 110px)" class="sidebar-scrollbar">
              <div class="chat-list">
                <div v-for="chat in chatHistory" :key="chat.id" class="chat-item">
                  <el-button text class="bubble-text-button" @click="selectSession(chat.session_id)">
                    {{ chat.title }}
                  </el-button>
                  <el-button 
                    circle 
                    class="delete-button bubble-icon-button" 
                    type="danger" 
                    size="small"
                    @click="deleteSession(chat.session_id)"
                  >
                    <Trash2 class="icon" />
                  </el-button>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </div>
        
        <div class="floating-input-container">
          <div class="input-wrapper bubble-card">
            <el-input 
              placeholder="输入消息..." 
              v-model="inputMessage"
              class="message-input"
              :prefix-icon="MessageCircle"
              @keyup.enter="sendMessage"
            />
            <el-button type="primary" circle class="send-button bubble-icon-button" @click="sendMessage">
              <Send class="icon" />
            </el-button>
          </div>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Search, Settings, MessageCircle, Send, Trash2 } from 'lucide-vue-next'
import requestUtil from '../../plugins/axios'

const inputMessage = ref('')
const chatHistory = ref([])
const currentSessionId = ref(null)
const currentSessionMessages = ref([])

// 获取聊天历史记录
const fetchChatHistory = async () => {
  try {
    var user_id = JSON.parse(sessionStorage.getItem('user')).user_id
    const response = await requestUtil.get(`/user/session?user_id=${user_id}`)
    const history = response.data.chat_data.map(session => ({
      session_id: session.session_id,
      title: session.session_data[0]?.content?.slice(0, 20) || '新对话',
      messages: session.session_data
    }))
    chatHistory.value = history
    
    // 如果有历史记录，默认选择第一个会话
    if (history.length > 0) {
      selectSession(history[0].session_id)
    }
  } catch (error) {
    console.error('获取聊天历史失败:', error)
  }
}

// 选择会话
const selectSession = (sessionId) => {
  currentSessionId.value = sessionId
  const session = chatHistory.value.find(chat => chat.session_id === sessionId)
  if (session) {
    currentSessionMessages.value = session.messages
  }
}

// 创建新会话
const createNewChat = () => {
  const newSession = {
    session_id: "new", 
    title: '新对话',
    messages: []
  }
  chatHistory.value.unshift(newSession)
  selectSession(newSession.session_id)
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || !currentSessionId.value) return
  
  const message = {
    content: inputMessage.value,
    type: 'human'
  }
  
  try {
    var user_id = JSON.parse(sessionStorage.getItem('user')).user_id
    // 添加用户消息到当前会话
    currentSessionMessages.value.push(message)
    
    // 创建AI回复的消息
    const aiMessage = {
      content: '',
      type: 'ai',
      isTyping: false
    }
    currentSessionMessages.value.push(aiMessage)
    
    // 发送消息到后端
    const response = await requestUtil.post(
      `/user/chat`,
      { 
        input: inputMessage.value,
        session_id: currentSessionId.value,
        user_id: user_id
      }
    )

    // 直接设置回复内容
    aiMessage.content = response.data.result;
    
    // 清空输入框
    inputMessage.value = ''
    
    // 更新当前会话中的消息
    const currentSession = chatHistory.value.find(chat => chat.session_id === currentSessionId.value)
    if (currentSession) {
      currentSession.messages = [...currentSessionMessages.value]
      // 如果是新会话，更新标题为第一条消息的前20个字符
      if (currentSession.title === '新对话' && message.content) {
        currentSession.title = message.content.slice(0, 20)
      }
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    // 发生错误时移除AI回复
    currentSessionMessages.value.pop()
  }
}

// 删除会话
const deleteSession = async (sessionId) => {
  try {
    var user_id = JSON.parse(sessionStorage.getItem('user')).user_id
    await requestUtil.del(`/user/session`, {
      user_id: user_id,
      session_id: sessionId 
    })
    
    // 从本地状态中移除会话
    chatHistory.value = chatHistory.value.filter(chat => chat.session_id !== sessionId)
    
    // 如果删除的是当前会话，切换到第一个会话或清空当前会话
    if (currentSessionId.value === sessionId) {
      if (chatHistory.value.length > 0) {
        selectSession(chatHistory.value[0].session_id)
      } else {
        currentSessionId.value = null
        currentSessionMessages.value = []
      }
    }
  } catch (error) {
    console.error('删除会话失败:', error)
  }
}

onMounted(() => {
  fetchChatHistory()
})
</script>

<style scoped>
.chat-container {
  height: 88vh;
}

.main-content {
  flex-direction: column;
}

.main-area {
  position: relative;
  padding: 0;
  overflow: hidden;
}

.content-with-sidebar {
  display: flex;
  height: 100%;
}

.message-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 80px; /* Space for floating input */
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
  margin-bottom: 16px;
}

.message-human {
  justify-content: flex-end;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-human .message-content {
  background-color: #409EFF;
  color: white;
  border-radius: 12px 12px 0 12px;
}

.message-ai .message-content {
  background-color: white;
  color: #333;
  border-radius: 12px 12px 12px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.integrated-sidebar {
  width: 280px;
  display: flex;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.8);
  border-left: 1px solid #e6e6e6;
  backdrop-filter: blur(10px);
}

/* Bubble styles */
.bubble-card {
  background-color: white;
  border-radius: 18px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 12px;
  margin: 8px;
}

.bubble-button {
  border-radius: 20px;
  padding: 10px 16px;
}

.bubble-icon-button {
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bubble-text-button {
  border-radius: 16px;
  padding: 8px 12px;
  transition: background-color 0.2s;
}

.bubble-text-button:hover {
  background-color: #f0f0f0;
}

/* Sidebar styles */
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.new-chat-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  width: 16px;
  height: 16px;
}

.sidebar-scrollbar {
  flex: 1;
}

.chat-list {
  padding: 8px 12px;
}

.chat-item {
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-item .bubble-text-button {
  flex: 1;
  text-align: left;
  padding: 8px 12px;
  font-weight: normal;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-item .delete-button {
  opacity: 0;
  transition: opacity 0.2s;
}

.chat-item:hover .delete-button {
  opacity: 1;
}

/* Floating input styles */
.floating-input-container {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 280px; /* Adjust for sidebar width */
  display: flex;
  justify-content: center;
  pointer-events: none; /* Allow clicking through the container */
}

.input-wrapper {
  display: flex;
  align-items: center;
  width: 80%;
  max-width: 800px;
  padding: 8px 16px;
  pointer-events: auto; /* Re-enable pointer events for the input */
}

.message-input {
  flex: 1;
}

.message-input :deep(.el-input__wrapper) {
  border-radius: 20px;
  padding: 8px 12px;
  background-color: transparent;
  box-shadow: none;
}

.send-button {
  margin-left: 8px;
}

.typing-indicator {
  display: inline-block;
  animation: blink 1s infinite;
  margin-left: 2px;
}

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}
</style>