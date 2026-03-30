<template>
  <div class="home-container">
    <el-container>
      <el-header height="60px" class="header">
        <div class="header-content">
          <h1 class="logo">宠物信息管理系统</h1>
          <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
            <el-menu-item index="home">首页</el-menu-item>
            <el-menu-item v-if="!isLoggedIn" index="login">登录</el-menu-item>
            <el-menu-item v-if="!isLoggedIn" index="register">注册</el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="pets">宠物管理</el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="reminders">提醒</el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="assistant">咨询助手</el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="profile">个人中心</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <div class="articles-section">
          <h2>宠物科普知识</h2>
          <el-select v-model="selectedCategory" placeholder="选择分类">
            <el-option label="全部" value="" />
            <el-option v-for="category in categories" :key="category" :label="category" :value="category" />
          </el-select>
          <div class="articles-grid">
            <el-card v-for="article in articles" :key="article.id" class="article-card">
              <img v-if="article.cover_url" :src="article.cover_url" class="article-cover" />
              <h3>{{ article.title }}</h3>
              <p class="article-category">{{ article.category }}</p>
              <p class="article-content">{{ article.content_md.substring(0, 100) }}...</p>
              <el-button type="primary" @click="viewArticle(article.id)">查看详情</el-button>
            </el-card>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const articles = ref<any[]>([])
const categories = ref<string[]>([])
const selectedCategory = ref('')

const isLoggedIn = computed(() => {
  return localStorage.getItem('access_token') !== null
})

const activeIndex = ref('home')

const handleSelect = (key: string) => {
  switch (key) {
    case 'home':
      router.push('/')
      break
    case 'login':
      router.push('/auth/login')
      break
    case 'register':
      router.push('/auth/register')
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

const fetchArticles = async () => {
  try {
    const response = await api.get('/articles')
    articles.value = response.data.items
    // 提取所有分类
    const catSet = new Set<string>()
    response.data.items.forEach((item: any) => catSet.add(item.category))
    categories.value = Array.from(catSet)
  } catch (error) {
    console.error('获取文章失败:', error)
  }
}

const viewArticle = (id: number) => {
  // 这里可以跳转到文章详情页，暂时先alert
  alert(`查看文章ID: ${id}`)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.home-container {
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

.articles-section {
  padding: 20px;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.article-card {
  transition: transform 0.3s ease;
}

.article-card:hover {
  transform: translateY(-5px);
}

.article-cover {
  width: 100%;
  height: 200px;
  object-fit: cover;
  margin-bottom: 15px;
}

.article-category {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.article-content {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
}
</style>