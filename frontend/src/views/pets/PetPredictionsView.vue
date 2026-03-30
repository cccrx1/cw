<template>
  <div class="pet-predictions-container">
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
        <div class="pet-predictions-section">
          <h2>预测结果</h2>
          <el-card v-loading="loading">
            <el-descriptions :column="1">
              <el-descriptions-item label="风险等级">
                <el-tag :type="getRiskLevelType(prediction.risk_level)">{{ getRiskLevelText(prediction.risk_level) }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="摘要">{{ prediction.summary }}</el-descriptions-item>
              <el-descriptions-item label="建议">{{ prediction.suggestion }}</el-descriptions-item>
              <el-descriptions-item label="风险因素" v-if="prediction.risk_factors && prediction.risk_factors.length > 0">
                <el-tag v-for="(factor, index) in prediction.risk_factors" :key="index" type="warning" style="margin-right: 10px; margin-bottom: 10px;">{{ factor }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="建议提醒" v-if="prediction.recommended_reminders && prediction.recommended_reminders.length > 0">
                <div v-for="(reminder, index) in prediction.recommended_reminders" :key="index" class="recommended-reminder">
                  <el-card>
                    <h4>{{ reminder.title }}</h4>
                    <p>类型: {{ reminderTypeMap[reminder.reminder_type] }}</p>
                    <p>建议时间: {{ getReminderDate(reminder.days_from_now) }}</p>
                    <el-button type="primary" size="small" @click="handleCreateReminder(reminder)">创建提醒</el-button>
                  </el-card>
                </div>
              </el-descriptions-item>
              <el-descriptions-item label="预测时间">{{ prediction.created_at }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../../api'

const router = useRouter()
const route = useRoute()
const loading = ref(false)

const petId = computed(() => route.params.id as string)
const predictionId = computed(() => route.params.predictionId as string)

const prediction = reactive({
  risk_level: '',
  summary: '',
  suggestion: '',
  risk_factors: [] as string[],
  recommended_reminders: [] as any[],
  created_at: ''
})

const reminderTypeMap = {
  vaccine: '疫苗',
  checkup: '体检',
  medicine: '用药',
  revisit: '复诊',
  other: '其他'
}

const activeIndex = ref('pets')

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

const fetchPredictionDetail = async () => {
  try {
    loading.value = true
    const response = await api.get(`/predictions/${predictionId.value}`)
    const data = response.data
    prediction.risk_level = data.risk_level
    prediction.summary = data.summary
    prediction.suggestion = data.suggestion
    prediction.risk_factors = data.risk_factors || []
    prediction.recommended_reminders = data.recommended_reminders || []
    prediction.created_at = data.created_at
  } catch (error) {
    console.error('获取预测详情失败:', error)
  } finally {
    loading.value = false
  }
}

const handleCreateReminder = (recommendedReminder: any) => {
  const reminderData = {
    pet_id: petId.value,
    title: recommendedReminder.title,
    reminder_type: recommendedReminder.reminder_type,
    remind_at: new Date(Date.now() + recommendedReminder.days_from_now * 24 * 60 * 60 * 1000).toISOString(),
    repeat_rule: 'none',
    status: 'active'
  }
  api.post('/reminders', reminderData).then(() => {
    alert('提醒创建成功')
  }).catch(error => {
    console.error('创建提醒失败:', error)
  })
}

const getRiskLevelType = (level: string) => {
  switch (level) {
    case 'low':
      return 'success'
    case 'medium':
      return 'warning'
    case 'high':
      return 'danger'
    default:
      return 'info'
  }
}

const getRiskLevelText = (level: string) => {
  switch (level) {
    case 'low':
      return '低风险'
    case 'medium':
      return '中风险'
    case 'high':
      return '高风险'
    default:
      return level
  }
}

const getReminderDate = (daysFromNow: number) => {
  const date = new Date()
  date.setDate(date.getDate() + daysFromNow)
  return date.toLocaleDateString()
}

onMounted(() => {
  fetchPredictionDetail()
})
</script>

<style scoped>
.pet-predictions-container {
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

.pet-predictions-section {
  padding: 20px;
}

.pet-predictions-section h2 {
  margin-bottom: 20px;
}

.recommended-reminder {
  margin-bottom: 15px;
}
</style>