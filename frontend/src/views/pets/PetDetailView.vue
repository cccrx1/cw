<template>
  <div class="pet-detail-container">
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
        <div class="pet-detail-section">
          <div class="section-header">
            <h2>宠物详情</h2>
            <div>
              <el-button @click="handleEditPet">编辑</el-button>
              <el-button type="primary" @click="handlePredict" :loading="predictLoading">触发预测</el-button>
            </div>
          </div>
          <el-card v-loading="loading">
            <el-descriptions :column="2">
              <el-descriptions-item label="宠物名称">{{ pet.name }}</el-descriptions-item>
              <el-descriptions-item label="物种">{{ speciesMap[pet.species] }}</el-descriptions-item>
              <el-descriptions-item label="品种">{{ pet.breed || '未知' }}</el-descriptions-item>
              <el-descriptions-item label="性别">{{ genderMap[pet.gender] }}</el-descriptions-item>
              <el-descriptions-item label="出生日期">{{ pet.birth_date || '未知' }}</el-descriptions-item>
              <el-descriptions-item label="体重(kg)">{{ pet.weight_kg }}</el-descriptions-item>
              <el-descriptions-item label="患病史" :span="2">{{ pet.disease_history || '无' }}</el-descriptions-item>
              <el-descriptions-item label="疫苗史" :span="2">{{ pet.vaccine_history || '无' }}</el-descriptions-item>
              <el-descriptions-item label="备注" :span="2">{{ pet.note || '无' }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
          <div class="predictions-section" style="margin-top: 20px;">
            <h3>预测记录</h3>
            <el-table :data="predictions" style="width: 100%" v-loading="predictionsLoading">
              <el-table-column prop="risk_level" label="风险等级" width="120">
                <template #default="scope">
                  <el-tag :type="getRiskLevelType(scope.row.risk_level)">{{ getRiskLevelText(scope.row.risk_level) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="summary" label="摘要" />
              <el-table-column prop="created_at" label="预测时间" width="180" />
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button size="small" @click="handleViewPrediction(scope.row.id)">查看详情</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div v-if="predictions.length === 0 && !predictionsLoading" class="empty-state">
              <el-empty description="暂无预测记录" />
            </div>
          </div>
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
const predictLoading = ref(false)
const predictionsLoading = ref(false)

const petId = computed(() => route.params.id as string)

const pet = reactive({
  name: '',
  species: '',
  breed: '',
  gender: '',
  birth_date: '',
  weight_kg: 0,
  disease_history: '',
  vaccine_history: '',
  note: ''
})

const predictions = ref<any[]>([])

const speciesMap = {
  dog: '狗狗',
  cat: '猫咪',
  other: '其他'
}

const genderMap = {
  male: '公',
  female: '母',
  unknown: '未知'
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

const fetchPetDetail = async () => {
  try {
    loading.value = true
    const response = await api.get(`/pets/${petId.value}`)
    const data = response.data
    pet.name = data.name
    pet.species = data.species
    pet.breed = data.breed
    pet.gender = data.gender
    pet.birth_date = data.birth_date
    pet.weight_kg = data.weight_kg
    pet.disease_history = data.disease_history
    pet.vaccine_history = data.vaccine_history
    pet.note = data.note
  } catch (error) {
    console.error('获取宠物详情失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchPredictions = async () => {
  try {
    predictionsLoading.value = true
    const response = await api.get(`/pets/${petId.value}/predictions`)
    predictions.value = response.data.items
  } catch (error) {
    console.error('获取预测记录失败:', error)
  } finally {
    predictionsLoading.value = false
  }
}

const handleEditPet = () => {
  router.push(`/pets/${petId.value}/edit`)
}

const handlePredict = async () => {
  if (confirm('确定要触发患病风险预测吗？')) {
    try {
      predictLoading.value = true
      await api.post(`/pets/${petId.value}/predict`)
      alert('预测完成，请查看预测结果')
      fetchPredictions()
    } catch (error) {
      console.error('预测失败:', error)
    } finally {
      predictLoading.value = false
    }
  }
}

const handleViewPrediction = (id: number) => {
  router.push(`/pets/${petId.value}/predictions`)
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

onMounted(() => {
  fetchPetDetail()
  fetchPredictions()
})
</script>

<style scoped>
.pet-detail-container {
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

.pet-detail-section {
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

.predictions-section h3 {
  margin-bottom: 15px;
}

.empty-state {
  margin-top: 30px;
  text-align: center;
}
</style>