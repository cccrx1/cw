<template>
  <div class="reminder-list-container">
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
        <div class="reminder-list-section">
          <div class="section-header">
            <h2>提醒列表</h2>
            <el-button type="primary" @click="handleAddReminder">新增提醒</el-button>
          </div>
          <el-card>
            <el-form :inline="true" :model="filterForm" class="filter-form">
              <el-form-item label="状态">
                <el-select v-model="filterForm.status" placeholder="选择状态">
                  <el-option label="全部" value="" />
                  <el-option label="活跃" value="active" />
                  <el-option label="已关闭" value="inactive" />
                  <el-option label="已完成" value="done" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="fetchReminders">查询</el-button>
              </el-form-item>
            </el-form>
          </el-card>
          <el-table :data="filteredReminders" style="width: 100%" v-loading="loading">
            <el-table-column prop="title" label="提醒标题" />
            <el-table-column prop="reminder_type" label="类型" width="120">
              <template #default="scope">
                {{ reminderTypeMap[scope.row.reminder_type] }}
              </template>
            </el-table-column>
            <el-table-column prop="remind_at" label="提醒时间" width="180" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button size="small" @click="handleEditReminder(scope.row.id)">编辑</el-button>
                <el-button size="small" @click="handleToggleReminder(scope.row.id, scope.row.status)">{{ scope.row.status === 'active' ? '关闭' : '开启' }}</el-button>
                <el-button type="danger" size="small" @click="handleDeleteReminder(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="filteredReminders.length === 0 && !loading" class="empty-state">
            <el-empty description="暂无提醒数据" />
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

const router = useRouter()
const reminders = ref<any[]>([])
const loading = ref(false)

const activeIndex = ref('reminders')

const filterForm = reactive({
  status: ''
})

const reminderTypeMap = {
  vaccine: '疫苗',
  checkup: '体检',
  medicine: '用药',
  revisit: '复诊',
  other: '其他'
}

const filteredReminders = computed(() => {
  if (!filterForm.status) {
    return reminders.value
  }
  return reminders.value.filter(reminder => reminder.status === filterForm.status)
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

const fetchReminders = async () => {
  try {
    loading.value = true
    const response = await api.get('/reminders')
    reminders.value = response.data.items
  } catch (error) {
    console.error('获取提醒列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAddReminder = () => {
  // 这里可以跳转到新增提醒页面，暂时先alert
  alert('新增提醒功能开发中')
}

const handleEditReminder = (id: number) => {
  // 这里可以跳转到编辑提醒页面，暂时先alert
  alert(`编辑提醒 ID: ${id}`)
}

const handleToggleReminder = (id: number, status: string) => {
  api.post(`/reminders/${id}/toggle`).then(() => {
    fetchReminders()
  }).catch(error => {
    console.error('切换提醒状态失败:', error)
  })
}

const handleDeleteReminder = (id: number) => {
  if (confirm('确定要删除这个提醒吗？')) {
    api.delete(`/reminders/${id}`).then(() => {
      fetchReminders()
    }).catch(error => {
      console.error('删除提醒失败:', error)
    })
  }
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'active':
      return 'success'
    case 'inactive':
      return 'info'
    case 'done':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'active':
      return '活跃'
    case 'inactive':
      return '已关闭'
    case 'done':
      return '已完成'
    default:
      return status
  }
}

onMounted(() => {
  fetchReminders()
})
</script>

<style scoped>
.reminder-list-container {
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

.reminder-list-section {
  padding: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
}

.filter-form {
  margin-bottom: 20px;
}

.empty-state {
  margin-top: 50px;
  text-align: center;
}
</style>