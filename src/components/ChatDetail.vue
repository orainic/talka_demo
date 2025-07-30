<template>
  <div class="chat-detail">
    <!-- 固定在顶部的返回按钮 -->
    <button @click="goBack" class="back-btn fixed-back">
      <i class="fas fa-arrow-left"></i> Back
    </button>
    
    <!-- 对话历史区域 -->
    <div class="section history-section">
      <h2><i class="fas fa-comments"></i> Conversation History</h2>
      <div class="box scrollable-box">
        <div v-for="(bubble, index) in bubbles" :key="index" 
             class="chat-line" :class="bubble.speaker === 'ai' ? 'chat-ai' : 'chat-user'">
          <div class="bubble" :class="bubble.speaker === 'ai' ? 'bubble-ai' : 'bubble-user'">
            <div class="speaker-tag">
              <i :class="bubble.speaker === 'ai' ? 'fas fa-robot' : 'fas fa-user'"></i>
              {{ bubble.speaker === 'ai' ? 'AI Assistant' : 'User' }}
            </div>
            {{ bubble.content }}
            <div class="timestamp">{{ bubble.timestamp }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="line"></div>
    
    <!-- 总结区域 -->
    <div class="section summary-section">
      <h2><i class="fas fa-file-alt"></i> Summary</h2>
      <div class="summary-box scrollable-box">
        <h3><i class="fas fa-lightbulb"></i> Key Points</h3>
        <p>{{ summary || 'No summary information yet' }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatDetail',
  data() {
    return {
      bubbles: [],
      summary: '',
      handler: null,
    };
  },
  mounted() {
    this.summary = history.state.summary
    this.processTranscript(history.state.transcript)
  },
  methods: {
    processTranscript(transcript) {
      const lines = transcript.split('\n');
      const bubbles = [];
      let currentSpeaker = null;
      let currentContent = "";
      
      lines.forEach((line) => {
        const trimmed = line.trim();
        if (!trimmed) return;
        
        let speaker = null;
        let content = "";
        
        if (/^AI agent:/i.test(trimmed)) {
          speaker = "ai";
          content = trimmed.replace(/^AI agent:/i, "").trim();
        } else if (/^User:/i.test(trimmed)) {
          speaker = "user";
          content = trimmed.replace(/^User:/i, "").trim();
        } else {
          // 没有新 speaker，继续上一个人的内容
          speaker = currentSpeaker;
          content = trimmed;
        }
        
        if (speaker === currentSpeaker) {
          currentContent += "\n" + content;
        } else {
          if (currentSpeaker && currentContent) {
            bubbles.push({
              speaker: currentSpeaker, 
              content: currentContent,
            });
          }
          currentSpeaker = speaker;
          currentContent = content;
        }
      });
      
      if (currentSpeaker && currentContent) {
        bubbles.push({
          speaker: currentSpeaker, 
          content: currentContent,
        });
      }
      
      this.bubbles = bubbles;
    },
    goBack() {
      if (this.$router) {
        this.$router.go(-1);
      } else {
        window.history.back();
      }
    }
  }
};
</script>

<style scoped>
.chat-detail {
  padding: 70px 25px 25px; /* 顶部内边距增大给固定按钮留空间 */
  background: white;
  height: 100vh; /* 使用视口高度 */
  display: flex;
  flex-direction: column;
}

/* 固定在顶部的返回按钮 */
.fixed-back {
  position: fixed;
  top: 15px;
  left: 100px;
  z-index: 100;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  padding: 12px 22px;
  background: linear-gradient(135deg, #3498db, #2c80b9);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  margin-bottom: 25px;
  font-weight: 500;
  box-shadow: 0 6px 15px rgba(52, 152, 219, 0.25);
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-size: 1.05rem;
}

.back-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(52, 152, 219, 0.35);
  background: linear-gradient(135deg, #2c80b9, #3498db);
}

.back-btn i {
  margin-right: 10px;
}

.section {
  margin-bottom: 20px;
  animation: fadeIn 0.6s ease;
}

/* 对话历史区域高度60% */
.history-section {
  flex: 0 0 60%; /* 占据60%高度 */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 隐藏溢出内容 */
}

/* 总结区域高度40% */
.summary-section {
  flex: 1; /* 占据剩余40%高度 */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 隐藏溢出内容 */
}

/* 可滚动区域 */
.scrollable-box {
  overflow-y: auto; /* 垂直滚动 */
  flex: 1; /* 填充可用空间 */
  min-height: 0; /* 防止溢出 */
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f1f1f1;
  font-size: 1.7rem;
  display: flex;
  align-items: center;
  flex-shrink: 0; /* 防止标题被压缩 */
}

h2 i {
  margin-right: 12px;
  color: #3498db;
}

.box {
  background: #fff;
  border: 1px solid #e1e5eb;
  padding: 25px;
  border-radius: 15px;
  font-size: 1.05rem;
  line-height: 1.75;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
  transition: all 0.4s ease;
  height: 100%; /* 填充父容器高度 */
}

.box:hover {
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  border-color: #d0d8e4;
}

.chat-line {
  display: flex;
  margin-bottom: 25px;
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-25px); }
  to { opacity: 1; transform: translateX(0); }
}

.chat-ai {
  justify-content: flex-start;
}

.chat-user {
  justify-content: flex-end;
}

.bubble {
  padding: 18px 24px;
  border-radius: 22px;
  max-width: 75%;
  color: white;
  white-space: pre-wrap;
  word-break: break-word;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.12);
  position: relative;
  overflow: hidden;
}

.bubble::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
}

.bubble-ai {
  background: linear-gradient(135deg, #3498db, #2980b9);
  border-top-left-radius: 0;
}

.bubble-user {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  border-top-right-radius: 0;
}

.line {
  height: 1px;
  background: linear-gradient(to right, transparent, #3498db, transparent);
  width: 85%;
  margin: 10px auto;
  flex-shrink: 0; /* 防止被压缩 */
}

.timestamp {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.85);
  text-align: right;
  margin-top: 10px;
  font-style: italic;
}

.speaker-tag {
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.speaker-tag i {
  margin-right: 8px;
}

/* Animation for bubbles */
.chat-line:nth-child(odd) {
  animation-delay: 0.1s;
}

.chat-line:nth-child(even) {
  animation-delay: 0.2s;
}

.summary-box {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 25px;
  border-radius: 15px;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #495057;
  border-left: 4px solid #3498db;
  height: 100%; /* 填充父容器高度 */
}

.summary-box h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.summary-box h3 i {
  margin-right: 10px;
  color: #3498db;
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .bubble {
    max-width: 82%;
  }
}

@media (max-width: 600px) {
  .bubble {
    max-width: 90%;
    padding: 15px 20px;
  }
  
  .back-btn {
    padding: 10px 18px;
    font-size: 1rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }

  .chat-detail {
    padding: 60px 15px 15px;
  }

  .fixed-back {
    left: 15px;
  }
}

@media (max-width: 480px) {
  .bubble {
    max-width: 95%;
  }
  
  .box {
    padding: 15px;
  }

  .summary-box {
    padding: 15px;
  }
}
</style>