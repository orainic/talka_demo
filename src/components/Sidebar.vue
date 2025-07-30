<template>
  <div class="sidebar">
    <div class="logo-container">
      <img src="../assets/logo.png" alt="App Logo" class="logo">
    </div>
    
    <div class="nav-links">
      <router-link to="/dashboard" class="nav-item" active-class="active" title="Dashboard">
        <i class="fas fa-tachometer-alt icon"></i>
      </router-link>
      
      <router-link to="/history" class="nav-item" active-class="active" title="History">
        <i class="fas fa-history icon"></i>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style scoped>
.sidebar {
  width: 80px; /* 宽度减小 */
  background: linear-gradient(to bottom, #2c3e50, #1a2a38);
  color: white;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  box-shadow: 5px 0 15px rgba(0, 0, 0, 0.2);
  z-index: 10;
  transition: width 0.3s ease; /* 添加过渡效果 */
}

.logo-container {
  padding: 20px 0; /* 减小垂直内边距 */
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  width: 50px; /* 缩小logo尺寸 */
  height: 50px;
  border-radius: 50%;
  margin: 0 auto;
  display: block;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.1);
}

/* 移除应用名称 */
.app-name {
  display: none;
}

.nav-links {
  padding: 20px 0; /* 减小内边距 */
  flex: 1;
}

.nav-item {
  padding: 18px 0; /* 调整内边距 */
  display: flex;
  justify-content: center; /* 图标居中 */
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  font-size: 18px;
  color: #bdc3c7;
  text-decoration: none;
  flex-direction: column; /* 垂直排列 */
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.active {
  background: rgba(52, 152, 219, 0.2);
  color: white;
  border-left: 4px solid #3498db;
}

.nav-item.active .icon {
  color: #3498db;
}

.icon {
  font-size: 22px; /* 增大图标尺寸 */
  transition: all 0.3s;
}

/* 移除媒体查询（不再需要响应式调整） */
</style>