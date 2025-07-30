<template>
  <div class="call-statistics-container">
    <!-- Greeting Section -->
    <div class="greeting-section">
      <h2>{{ greeting }}, {{ userName }}!</h2>
    </div>

    <!-- Divider -->
    <el-divider />

    <!-- Charts and Statistics Section -->
    <div class="stats-container">
      <!-- Left Chart -->
      <div class="chart-section">
        <div class="chart-controls">
          <div class="control-group">
            <label>Call Type:</label>
            <select v-model="selectedCategory" @change="fetchChartData">
              <option value="Technical Support">Technical Support</option>
              <option value="Sales Leads">Sales Leads</option>
              <option value="Product Information Inquiry">Product Information Inquiry</option>
              <option value="Product Tracking">Product Tracking</option>
              <option value="Complain">Complain</option>
              <option value="N/A">N/A</option>
            </select>
          </div>
          <div class="control-group">
            <label>Time Range:</label>
            <select v-model="selectedRange" @change="fetchChartData">
              <option value="7">Last 7 Days</option>
              <option value="15">Last 15 Days</option>
              <option value="30">Last 30 Days</option>
            </select>
          </div>
        </div>
        <div ref="chartRef" class="chart" style="height: 90%;"></div>
      </div>

      <!-- Right Summary -->
      <div class="summary-section">
        <div class="summary-card">
          <h3>Call Statistics</h3>
          <div class="stats-content">
            <!-- Pie Chart Section -->
            <div class="pie-chart-container">
              <div ref="pieChartRef" class="pie-chart"></div>
              <div class="pie-chart-label">
                <div class="percentage">{{ percentage }}%</div>
                <div class="category-name">{{ selectedCategory }}</div>
              </div>
            </div>

            <!-- Statistics Grid -->
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-label">Total Calls (Selected)</div>
                <div class="stat-value">{{ summary.selectedTotalCalls }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Total Calls (All)</div>
                <div class="stat-value">{{ summary.allTotalCalls }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Daily Average (Selected)</div>
                <div class="stat-value">{{ summary.avgPerDay }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Peak Day (All)</div>
                <div class="stat-value">{{ summary.maxDaily }}</div>
                <div class="stat-subtext">({{ summary.maxDate }})</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Today (Selected)</div>
                <div class="stat-value">{{ summary.todayCalls }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">Today (All)</div>
                <div class="stat-value">{{ summary.todayTotalCalls }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable vue/multi-word-component-names */
import { ref, onMounted, computed, watch } from 'vue';
import * as echarts from 'echarts';
export default {
  name: 'Dashboard',
  props: {
    userName: {
      type: String,
      default: 'Jack'
    },
    calls: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    // 计算问候语
    const greeting = computed(() => {
      const hour = new Date().getHours();
      if (hour < 12) return 'Good Morning';
      if (hour < 18) return 'Good Afternoon';
      return 'Good Evening';
    });

    // 图表相关
    const chartRef = ref(null);
    const pieChartRef = ref(null);
    const chartInstance = ref(null);
    const pieChartInstance = ref(null);
    const selectedRange = ref('15');
    const selectedCategory = ref('Technical Support');
    const percentage = ref(0);

    // 统计数据
    const summary = ref({
      selectedTotalCalls: 0,
      allTotalCalls: 0,
      avgPerDay: 0,
      maxDaily: 0,
      maxDate: '',
      todayCalls: 0,
      todayTotalCalls: 0
    });

    // 初始化柱状图
    const initChart = () => {
      if (!chartRef.value) return;

      chartInstance.value = echarts.init(chartRef.value);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params) => {
            const selectedType = params[0];
            const totalType = params[1];
            const percent = ((selectedType.value / totalType.value) * 100).toFixed(1);
            return `
              <div><strong>${selectedType.name}</strong></div>
              <div>${selectedType.seriesName}: ${selectedType.value}</div>
              <div>${totalType.seriesName}: ${totalType.value}</div>
              <div>Selected Percentage: ${percent}%</div>
            `;
          }
        },
        legend: {
          data: ['Selected Type', 'Total Calls']
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: 'Call Volume'
        },
        series: [
          {
            name: 'Selected Type',
            type: 'bar',
            data: [],
            itemStyle: {
              color: '#355bd4'
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}'
            }
          },
          {
            name: 'Total Calls',
            type: 'bar',
            data: [],
            itemStyle: {
              color: '#5470c6'
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}'
            }
          }
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          top: '15%',
          containLabel: true
        }
      };

      chartInstance.value.setOption(option);
    };

    // 初始化饼图
    const initPieChart = () => {
      if (!pieChartRef.value) return;

      pieChartInstance.value = echarts.init(pieChartRef.value);
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: [
          {
            name: 'Call Distribution',
            type: 'pie',
            radius: ['70%', '90%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold',
                formatter: '{d}%'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 0, name: 'Selected' },
              { value: 100, name: 'Other' }
            ],
            color: ['#5470c6', '#eee']
          }
        ]
      };

      pieChartInstance.value.setOption(option);
    };

    // 更新饼图数据
    const updatePieChart = (selectedTotal, allTotal) => {
      if (!pieChartInstance.value) return;

      const otherTotal = allTotal - selectedTotal;
      const percent = allTotal > 0 ? (selectedTotal / allTotal * 100).toFixed(1) : 0;
      percentage.value = percent;

      pieChartInstance.value.setOption({
        series: [{
          data: [
            { value: selectedTotal, name: selectedCategory.value },
            { value: otherTotal, name: 'Other Types' }
          ]
        }]
      });
    };

    // 处理通话数据
    const fetchChartData = () => {
      const days = parseInt(selectedRange.value);
      const today = new Date();
      today.setHours(0, 0, 0, 0); // 设置为当天开始时间

      // 生成日期标签和映射
      const dateLabels = [];
      const dateMap = {};

      for (let i = days - 1; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);

        // 使用本地日期格式 (YYYY-MM-DD)
        const dateStr = date.toISOString().split('T')[0];

        // 生成月/日格式的标签 (MM/DD)
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const label = `${month}/${day}`;

        dateLabels.push(label);
        dateMap[dateStr] = i; // 存储日期索引
      }

      // 初始化每天的数据
      const selectedData = new Array(days).fill(0);
      const totalData = new Array(days).fill(0);

      // 统计分类数据
      const categoryCounts = {
        'Technical Support': 0,
        'Sales Leads': 0,
        'Product Information Inquiry': 0,
        'Product Tracking': 0,
        'Complain': 0,
        'N/A': 0
      };

      // 处理通话记录
      props.calls.forEach(call => {
        if (!call.startTime) return;

        // 提取日期部分 (YYYY-MM-DD)
        const callDate = new Date(call.startTime);
        const callDateStr = callDate.toISOString().split('T')[0];

        // 如果通话日期在选定范围内
        if (Object.prototype.hasOwnProperty.call(dateMap, callDateStr)) {
          const index = dateMap[callDateStr];
          totalData[index]++;

          // 统计分类数据
          const tags = call.tag ? call.tag.split(',').map(tag => tag.trim()) : [];
          tags.forEach(tag => {
            if (Object.prototype.hasOwnProperty.call(categoryCounts, tag)) {
              categoryCounts[tag]++;
            }
          });

          // 统计选定分类
          if (tags.includes(selectedCategory.value)) {
            selectedData[index]++;
          }
        }
      });
      console.log(selectedData, totalData)
      // 更新柱状图数据
      chartInstance.value.setOption({
        xAxis: {
          data: dateLabels
        },
        series: [
          {
            name: `${selectedCategory.value} Calls`,
            data: selectedData.reverse()
          },
          {
            name: 'Total Calls',
            data: totalData.reverse()
          }
        ]
      });

      // 计算统计数据
      updateSummaryStats(selectedData, totalData, dateLabels);
    };

    // 计算统计数据
    const updateSummaryStats = (selectedData, totalData, dateLabels) => {
      // 计算当前选择类型的统计数据
      const selectedTotal = selectedData.reduce((sum, val) => sum + val, 0);

      // 计算所有通话类型的统计数据
      const allTotal = totalData.reduce((sum, val) => sum + val, 0);

      // 找到通话量最大的一天
      const maxIndex = totalData.indexOf(Math.max(...totalData));
      const maxDate = dateLabels[maxIndex] || '';

      // 获取今天的数据（最后一天）
      const todayIndex = totalData.length - 1;
      const todaySelected = selectedData[todayIndex] || 0;
      const todayTotal = totalData[todayIndex] || 0;

      summary.value = {
        selectedTotalCalls: selectedTotal,
        allTotalCalls: allTotal,
        avgPerDay: (selectedTotal / selectedData.length).toFixed(1),
        maxDaily: Math.max(...totalData),
        maxDate: maxDate,
        todayCalls: todaySelected,
        todayTotalCalls: todayTotal
      };

      // 更新饼图
      updatePieChart(selectedTotal, allTotal);
    };

    // 生命周期钩子
    onMounted(() => {
      initChart();
      initPieChart();
      fetchChartData();

      // 响应式调整图表大小
      window.addEventListener('resize', () => {
        chartInstance.value?.resize();
        pieChartInstance.value?.resize();
      });
    });

    // 监听calls数据变化
    watch(() => props.calls, () => {
      fetchChartData();
    });

    // 监听筛选条件变化
    watch([selectedRange, selectedCategory], () => {
      fetchChartData();
    });

    return {
      greeting,
      chartRef,
      pieChartRef,
      selectedRange,
      selectedCategory,
      summary,
      percentage,
      fetchChartData
    };
  }
};
</script>

<style scoped>
.call-statistics-container {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  margin: 0 auto;
  padding: 20px;
  height: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.greeting-section {
  padding: 15px 0;
}

.greeting-section h2 {
  margin: 0;
  color: #333;
  font-weight: normal;
}

.stats-container {
  display: flex;
  gap: 30px;
  margin-top: 20px;
  height: 90%;
}

.chart-section {
  flex: 3;
  background-color: #f9fafc;
  padding: 15px;
  border-radius: 8px;
}

.summary-section {
  flex: 1;
}

.chart-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
}

.control-group {
  display: flex;
  align-items: center;
}

.control-group label {
  margin-right: 10px;
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
}

.control-group select {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
  color: #606266;
  outline: none;
  transition: border-color 0.3s;
  min-width: 120px;
}

.control-group select:focus {
  border-color: #409eff;
}

.summary-card {
  background-color: #f9fafc;
  padding: 20px;
  border-radius: 8px;
  height: 100%;
}

.summary-card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
  color: #333;
}

.stats-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 40px);
}

.pie-chart-container {
  position: relative;
  height: 180px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  border-radius: 8px;
  background-color: #fff;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.pie-chart {
  width: 100%;
  height: 100%;
}

.pie-chart-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  pointer-events: none;
}

.percentage {
  font-size: 24px;
  font-weight: bold;
  color: #5470c6;
}

.category-name {
  font-size: 14px;
  color: #606266;
  margin-top: 5px;
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  flex-grow: 1;
  overflow-y: auto;
}

.stat-item {
  background-color: #fff;
  padding: 15px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-subtext {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
  }

  .chart-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .control-group {
    width: 100%;
  }

  .control-group select {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .pie-chart-container {
    height: 150px;
  }
}
</style>
