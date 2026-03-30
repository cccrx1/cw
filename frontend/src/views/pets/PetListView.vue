<template>
  <div class="pet-list-container">
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
        <div class="pet-list-section">
          <div class="section-header">
            <h2>宠物列表</h2>
            <el-button type="primary" @click="handleAddPet">新增宠物</el-button>
          </div>
          <el-table :data="pets" style="width: 100%" v-loading="loading">
            <el-table-column prop="name" label="宠物名称" width="180" />
            <el-table-column prop="species" label="物种" width="120">
              <template #default="scope">
                {{ speciesMap[scope.row.species] }}
              </template>
            </el-table-column>
            <el-table-column prop="breed" label="品种" width="180" />
            <el-table-column prop="gender" label="性别" width="100">
              <template #default="scope">
                {{ genderMap[scope.row.gender] }}
              </template>
            </el-table-column>
            <el-table-column prop="birth_date" label="出生日期" width="150" />
            <el-table-column prop="weight_kg" label="体重(kg)" width="100" />
            <el-table-column label="操作" width="250">
              <template #default="scope">
                <el-button type="primary" size="small" @click="handleViewPet(scope.row.id)">查看</el-button>
                <el-button size="small" @click="handleEditPet(scope.row.id)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDeletePet(scope.row.id, scope.row.name)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="pets.length === 0 && !loading" class="empty-state">
            <el-empty description="暂无宠物数据" />
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const pets = ref<any[]>([])
const loading = ref(false)

const activeIndex = ref('pets')

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

const fetchPets = async () => {
  try {
    loading.value = true
    const response = await api.get('/pets')
    pets.value = response.data.items
  } catch (error) {
    console.error('获取宠物列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleAddPet = () => {
  router.push('/pets/new')
}

const handleViewPet = (id: number) => {
  router.push(`/pets/${id}`)
}

const handleEditPet = (id: number) => {
  router.push(`/pets/${id}/edit`)
}

const handleDeletePet = (id: number, name: string) => {
  if (confirm(`确定要删除宠物 ${name} 吗？`)) {
    api.delete(`/pets/${id}`).then(() => {
      fetchPets()
    }).catch(error => {
      console.error('删除宠物失败:', error)
    })
  }
}

onMounted(() => {
  fetchPets()
})
</script>

<style scoped>
.pet-list-container {
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

.pet-list-section {
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

.empty-state {
  margin-top: 50px;
  text-align: center;
}
</style>