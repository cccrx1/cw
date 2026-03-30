<template>
  <div class="assistant-container">
    <el-container>
      <el-header height="60px" class="header">
        <div class="header-content">
          <h1 class="logo">宠物信息管理系统</h1>
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="home">首页</el-menu-item>
            <el-menu-item index="pets">宠物管理</el-menu-item>
            <el-menu-item index="reminders">提醒</el-menu-item>
            <el-menu-item index="assistant">咨询助手</el-menu-item>
            <el-menu-item index="profile">个人中心</el-menu-item>
            <el-menu-item index="logout" @click="handleLogout">退出登录</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="assistant-main">
        <div class="assistant-content">
          <div class="sessions-sidebar">
            <div class="sidebar-header">
              <h3>会话列表</h3>
              <el-button type="primary" size="small" @click="handleCreateSession">新建会话</el-button>
            </div>
            <el-tree
              :data="sessions"
              node-key="id"
              :default-expanded-keys="[currentSessionId]"
              @node-click="handleSessionClick"
            >
              <template #default="{ node, data }">
                <div class="session-item">
                  <span class="session-title">{{ data.title }}</span>
                  <div class="session-actions">
                    <el-button size="small" @click.stop="handleRenameSession(data.id, data.title)">重命名</el-button>
                    <el-button size="small" type="danger" @click.stop="handleDeleteSession(data.id)">删除</el-button>
                  </div>
                </div>
              </template>
            </el-tree>
          </div>
          <div class="chat-area">
            <div class="chat-header" v-if="currentSession">
              <h3>{{ currentSession.title }}</h3>
              <el-button size="small" @click="handleRegenerateMessage" :loading="regenerating">重新生成</el-button>
            </div>
            <div class="chat-messages" v-if="currentSession">
              <div
                v-for="message in messages"
                :key="message.id"
                :class="['message-item', message.role === 'user' ? 'user-message' : 'assistant-message']"
              >
                <div class="message-avatar">{{ message.role === 'user' ? '我' : '助手' }}</div>
                <div class="message-content" v-html="renderMarkdown(message.content)"></div>
                <div class="message-time">{{ formatTime(message.created_at) }}</div>
              </div>
              <div v-if="loading" class="loading-message">
                <el-icon class="is-loading"><Loading /></el-icon>
                <span>思考中...</span>
              </div>
            </div>
            <div class="chat-input" v-if="currentSession">
              <el-input
                v-model="inputMessage"
                type="textarea"
                :rows="3"
                placeholder="请输入您的问题..."
                @keyup.enter.exact="handleSendMessage"
                @keyup.enter.shift="$event.preventDefault()"
              />
              <div class="input-actions">
                <el-button type="primary" @click="handleSendMessage" :loading="loading">发送</el-button>
              </div>
            </div>
            <div class="empty-state" v-else>
              <el-empty description="请选择或创建一个会话" />
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from './../api'
import MarkdownIt from 'markdown-it'
import { Loading } from '@element-plus/icons-vue'

const router = useRouter()
const sessions = ref<any[]>([])
const messages = ref<any[]>([])
const currentSessionId = ref<number | null>(null)
const inputMessage = ref('')
const loading = ref(false)
const regenerating = ref(false)

const md = new MarkdownIt()

const activeIndex = ref('assistant')

const currentSession = computed(() => {
  if (!currentSessionId.value) return null
  return sessions.value.find(session => session.id === currentSessionId.value) || null
})

const handleSelect = (key: string) => {
  switch (key) {
    case 'home':
      router.push('/')
      break
    case 'pets':
      router.push('/pets')
      break
    case 'reminders':
      router.push('/reminders')
      break
    case 'assistant':
      router.push('/assistant')
      break
    case 'profile':
      router.push('/profile')
      break
  }
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  router.push('/auth/login')
}

const fetchSessions = async () => {
  try {
    const response = await api.get('/chat/sessions')
    sessions.value = response.data.items
    if (sessions.value.length > 0 && !currentSessionId.value) {
      currentSessionId.value = sessions.value[0].id
      fetchMessages(currentSessionId.value)
    }
  } catch (error) {
    console.error('获取会话列表失败:', error)
  }
}

const fetchMessages = async (sessionId: number) => {
  try {
    const response = await api.get(`/chat/sessions/${sessionId}/messages`)
    messages.value = response.data.items
  } catch (error) {
    console.error('获取消息失败:', error)
  }
}

const handleCreateSession = async () => {
  try {
    const response = await api.post('/chat/sessions', { title: '新会话' })
    sessions.value.push(response.data)
    currentSessionId.value = response.data.id
    messages.value = []
  } catch (error) {
    console.error('创建会话失败:', error)
  }
}

const handleSessionClick = (data: any) => {
  currentSessionId.value = data.id
  fetchMessages(data.id)
}

const handleRenameSession = (sessionId: number, currentTitle: string) => {
  const newTitle = prompt('请输入新的会话标题:', currentTitle)
  if (newTitle && newTitle.trim()) {
    api.put(`/chat/sessions/${sessionId}`, { title: newTitle.trim() }).then(() => {
      const session = sessions.value.find(s => s.id === sessionId)
      if (session) {
        session.title = newTitle.trim()
      }
    }).catch(error => {
      console.error('重命名会话失败:', error)
    })
  }
}

const handleDeleteSession = (sessionId: number) => {
  if (confirm('确定要删除这个会话吗？')) {
    api.delete(`/chat/sessions/${sessionId}`).then(() => {
      sessions.value = sessions.value.filter(s => s.id !== sessionId)
      if (currentSessionId.value === sessionId) {
        currentSessionId.value = sessions.value.length > 0 ? sessions.value[0].id : null
        if (currentSessionId.value) {
          fetchMessages(currentSessionId.value)
        } else {
          messages.value = []
        }
      }
    }).catch(error => {
      console.error('删除会话失败:', error)
    })
  }
}

const handleSendMessage = async () => {
  if (!inputMessage.value.trim() || !currentSessionId.value) return
  
  const content = inputMessage.value.trim()
  inputMessage.value = ''
  
  try {
    loading.value = true
    const response = await api.post(`/chat/sessions/${currentSessionId.value}/messages`, { content })
    fetchMessages(currentSessionId.value)
  } catch (error) {
    console.error('发送消息失败:', error)
  } finally {
    loading.value = false
  }
}

const handleRegenerateMessage = async () => {
  if (!currentSessionId.value) return
  
  try {
    regenerating.value = true
    const response = await api.post(`/chat/sessions/${currentSessionId.value}/messages/regenerate`)
    fetchMessages(currentSessionId.value)
  } catch (error) {
    console.error('重新生成消息失败:', error)
  } finally {
    regenerating.value = false
  }
}

const renderMarkdown = (content: string) => {
  return md.render(content)
}

const formatTime = (time: string) => {
  return new Date(time).toLocaleString()
}

onMounted(() => {
  fetchSessions()
})
</script>

<style scoped>
.assistant-container {
  min-height: 100vh;
}

.header {
  background-color: #409eff;
  color: white;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  margin: 0;
  font-size: 20px;
}

.el-menu-demo {
  background-color: transparent;
  border-bottom: none;
}

.el-menu-item {
  color: white;
}

.assistant-main {
  padding: 0;
  height: calc(100vh - 60px);
}

.assistant-content {
  display: flex;
  height: 100%;
}

.sessions-sidebar {
  width: 300px;
  border-right: 1px solid #e0e0e0;
  padding: 20px;
  overflow-y: auto;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sidebar-header h3 {
  margin: 0;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

.session-item:hover {
  background-color: #f5f7fa;
}

.session-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.session-actions {
  display: flex;
  gap: 5px;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
}

.user-message .message-avatar {
  background-color: #67c23a;
}

.message-content {
  flex: 1;
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-message .message-content {
  background-color: #ecf5ff;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin: 0 10px;
  align-self: flex-end;
}

.loading-message {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
  color: #909399;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background-color: white;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
}
</style>