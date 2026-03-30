<template>
  <div class="profile-container">
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
      <el-main>
        <div class="profile-section">
          <h2>个人中心</h2>
          <el-card class="profile-card">
            <template #header>
              <div class="card-header">
                <span>个人资料</span>
              </div>
            </template>
            <el-form :model="userInfo" :rules="rules" ref="userFormRef" label-width="80px">
              <el-form-item label="用户名" prop="username">
                <el-input v-model="userInfo.username" disabled />
              </el-form-item>
              <el-form-item label="邮箱" prop="email">
                <el-input v-model="userInfo.email" />
              </el-form-item>
              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="userInfo.nickname" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleUpdate" :loading="loading">保存修改</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          <el-card class="password-card" style="margin-top: 20px;">
            <template #header>
              <div class="card-header">
                <span>修改密码</span>
              </div>
            </template>
            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px">
              <el-form-item label="新密码" prop="password">
                <el-input v-model="passwordForm.password" type="password" show-password />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading">修改密码</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const userFormRef = ref()
const passwordFormRef = ref()
const loading = ref(false)
const passwordLoading = ref(false)

const userInfo = reactive({
  username: '',
  email: '',
  nickname: ''
})

const passwordForm = reactive({
  password: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ]
}

const passwordRules = {
  password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' }
  ]
}

const activeIndex = ref('profile')

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

const fetchUserInfo = async () => {
  try {
    const response = await api.get('/auth/me')
    userInfo.username = response.data.username
    userInfo.email = response.data.email
    userInfo.nickname = response.data.nickname
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

const handleUpdate = async () => {
  if (!userFormRef.value) return
  
  try {
    await userFormRef.value.validate()
    loading.value = true
    await api.put('/auth/me', userInfo)
    alert('个人资料更新成功')
  } catch (error) {
    console.error('更新失败:', error)
  } finally {
    loading.value = false
  }
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true
    await api.post('/auth/change-password', { password: passwordForm.password })
    alert('密码修改成功')
    passwordForm.password = ''
  } catch (error) {
    console.error('修改密码失败:', error)
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.profile-container {
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

.profile-section {
  padding: 20px;
}

.profile-card,
.password-card {
  max-width: 600px;
  margin: 0 auto;
}

.card-header {
  font-size: 16px;
  font-weight: bold;
}
</style>