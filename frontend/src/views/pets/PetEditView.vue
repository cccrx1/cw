<template>
  <div class="pet-edit-container">
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
        <div class="pet-edit-section">
          <h2>{{ isEdit ? '编辑宠物' : '新增宠物' }}</h2>
          <el-card>
            <el-form :model="petForm" :rules="rules" ref="petFormRef" label-width="120px">
              <el-form-item label="宠物名称" prop="name">
                <el-input v-model="petForm.name" placeholder="请输入宠物名称" />
              </el-form-item>
              <el-form-item label="物种" prop="species">
                <el-select v-model="petForm.species" placeholder="请选择物种">
                  <el-option label="狗狗" value="dog" />
                  <el-option label="猫咪" value="cat" />
                  <el-option label="其他" value="other" />
                </el-select>
              </el-form-item>
              <el-form-item label="品种" prop="breed">
                <el-input v-model="petForm.breed" placeholder="请输入品种" />
              </el-form-item>
              <el-form-item label="性别" prop="gender">
                <el-select v-model="petForm.gender" placeholder="请选择性别">
                  <el-option label="公" value="male" />
                  <el-option label="母" value="female" />
                  <el-option label="未知" value="unknown" />
                </el-select>
              </el-form-item>
              <el-form-item label="出生日期" prop="birth_date">
                <el-date-picker
                  v-model="petForm.birth_date"
                  type="date"
                  placeholder="请选择出生日期"
                  value-format="YYYY-MM-DD"
                  :max="new Date()"
                />
              </el-form-item>
              <el-form-item label="体重(kg)" prop="weight_kg">
                <el-input v-model.number="petForm.weight_kg" type="number" placeholder="请输入体重" />
              </el-form-item>
              <el-form-item label="患病史" prop="disease_history">
                <el-input v-model="petForm.disease_history" type="textarea" placeholder="请输入患病史" />
              </el-form-item>
              <el-form-item label="疫苗史" prop="vaccine_history">
                <el-input v-model="petForm.vaccine_history" type="textarea" placeholder="请输入疫苗史" />
              </el-form-item>
              <el-form-item label="备注" prop="note">
                <el-input v-model="petForm.note" type="textarea" placeholder="请输入备注" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSubmit" :loading="loading">{{ isEdit ? '保存修改' : '创建宠物' }}</el-button>
                <el-button @click="handleCancel">取消</el-button>
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
import { useRouter, useRoute } from 'vue-router'
import api from '../../api'

const router = useRouter()
const route = useRoute()
const petFormRef = ref()
const loading = ref(false)

const petId = computed(() => route.params.id as string)
const isEdit = computed(() => petId.value !== 'new')

const petForm = reactive({
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

const rules = {
  name: [
    { required: true, message: '请输入宠物名称', trigger: 'blur' }
  ],
  species: [
    { required: true, message: '请选择物种', trigger: 'blur' }
  ],
  weight_kg: [
    { required: true, message: '请输入体重', trigger: 'blur' },
    { type: 'number', min: 0.1, message: '体重必须大于0', trigger: 'blur' }
  ]
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
  if (!isEdit.value) return
  
  try {
    loading.value = true
    const response = await api.get(`/pets/${petId.value}`)
    const pet = response.data
    petForm.name = pet.name
    petForm.species = pet.species
    petForm.breed = pet.breed
    petForm.gender = pet.gender
    petForm.birth_date = pet.birth_date
    petForm.weight_kg = pet.weight_kg
    petForm.disease_history = pet.disease_history
    petForm.vaccine_history = pet.vaccine_history
    petForm.note = pet.note
  } catch (error) {
    console.error('获取宠物详情失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!petFormRef.value) return
  
  try {
    await petFormRef.value.validate()
    loading.value = true
    if (isEdit.value) {
      await api.put(`/pets/${petId.value}`, petForm)
      alert('宠物信息更新成功')
    } else {
      await api.post('/pets', petForm)
      alert('宠物创建成功')
    }
    router.push('/pets')
  } catch (error) {
    console.error('操作失败:', error)
  } finally {
    loading.value = false
  }
}

const handleCancel = () => {
  router.push('/pets')
}

onMounted(() => {
  fetchPetDetail()
})
</script>

<style scoped>
.pet-edit-container {
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

.pet-edit-section {
  padding: 20px;
}

.pet-edit-section h2 {
  margin-bottom: 20px;
}
</style>