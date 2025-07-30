<template>
  <div id="app">
    <Sidebar :dark-mode="darkMode" @toggle-dark-mode="toggleDarkMode" />
    <div class="main-content">
      <div class="content-wrapper">
        <router-view :calls="calls"></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue'

export default {
  name: 'App',
  components: {
    Sidebar
  },
  data() {
    return {
      calls: [],
      socket: null,
      reconnectAttempts: 0,
      maxReconnectAttempts: 5,
      darkMode: false
    }
  },
  methods: {
    initWebSocket() {
      this.socket = new WebSocket("ws://localhost:8765");

      this.socket.onopen = () => {
        console.log("WebSocket connected");
        this.socket.send('test');
        this.reconnectAttempts = 0;
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.generateMockData(data);
          console.log("Received update:", data);
        } catch (err) {
          console.error("WebSocket message parse error:", err);
        }
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      this.socket.onclose = (event) => {
        console.log("WebSocket disconnected:", event.reason);

        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
          console.log(`Reconnecting in ${delay}ms...`);

          setTimeout(() => {
            this.reconnectAttempts++;
            this.initWebSocket();
          }, delay);
        }
      };
    },

    generateMockData(data) {
      const keys = ['SipID','CallId','DateTime','PhoneNumber','CallDuration','BillDuration','ClientName','Transcript','Summary','Tag'];
      const result = data.slice(1).map(row => {
        return keys.reduce((obj, key, index) => {
          obj[key] = row[index];
          return obj;
        }, {});
      });

      this.calls = result.map(item => ({
        id: item.CallId,
        startTime: item.DateTime,
        duration: item.CallDuration || 0,
        phoneNumber: item.PhoneNumber,
        summary: item.Summary,
        transcript: item.Transcript,
        tag: item.Tag,
        name: item.ClientName,
      }));
    },

    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      if (this.darkMode) {
        document.body.classList.add('dark');
      } else {
        document.body.classList.remove('dark');
      }
    }
  },
  mounted() {
    this.initWebSocket();
    if (this.darkMode) {
      document.body.classList.add('dark');
    }
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

html, body {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

#app {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: #f0f2f5;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  background: #f0f2f5;
  padding-left: 75px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 16px;
  }
}

body.dark {
  background: #121212;
  color: #e0e0e0;
}

body.dark #app {
  background: #121212;
}

body.dark .content-wrapper {
  background: #121212;
}

body.dark .sidebar {
  background: linear-gradient(to bottom, #1f2d3a, #111a23);
}

body.dark .call-statistics-container,
body.dark .history-container,
body.dark .chat-detail,
body.dark .box,
body.dark .summary-box,
body.dark .summary-card,
body.dark .chart-section,
body.dark .pie-chart-container,
body.dark .stat-item,
body.dark .search-box,
body.dark .filter-item select {
  background: #1e1e1e;
  color: #e0e0e0;
}

body.dark .history-table th,
body.dark .history-table td {
  color: #e0e0e0;
}

body.dark .history-table th {
  background: #1f2d3a;
}
</style>
