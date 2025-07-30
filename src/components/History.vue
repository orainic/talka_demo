<template>
  <div class="history-container">
    <div class="header-bar">
      <div class="header-title">
        <div class="img"></div>
        <h2>Call History</h2>
      </div>
      <div class="search-box">
        <i class="fas fa-search"></i>
        <input type="text" v-model="searchQuery" placeholder="Search call records...">
      </div>
    </div>

    <div class="filter-section">
      <div class="filter-item">
        <label><i class="fas fa-filter"></i> Time Range</label>
        <select v-model="timeFilter">
          <option value="all">All Time</option>
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
        </select>
      </div>

      <div class="filter-item">
        <label><i class="fas fa-sort"></i> Sort By</label>
        <select v-model="sortBy">
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
          <option value="longest">Longest Duration</option>
          <option value="shortest">Shortest Duration</option>
        </select>
      </div>
    </div>

    <table class="history-table">
      <thead>
      <tr>
        <th><i class="fas fa-hashtag"></i> CALL ID</th>
        <th><i class="fas fa-clock"></i> START TIME</th>
        <th><i class="fas fa-stopwatch"></i> DURATION</th>
        <th><i class="fas fa-phone"></i> PHONE NUMBER</th>
        <th><i class="fas fa-file-alt"></i> SUMMARY</th>
        <th><i class="fas fa-file-alt"></i> Tag</th>
        <th><i class="fas fa-file-alt"></i> Name</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="call in filteredCalls" :key="call.id" @click="viewCallDetail(call)">
        <td class="call-id">{{ call.id }}</td>
        <td class="start-time">{{ call.startTime }}</td>
        <td><span class="duration">{{ call.duration }}s</span></td>
        <td class="phone-number">{{ call.phoneNumber }}</td>
        <td class="summary">{{ call.summary }}</td>
        <td class="phone-number">
  <span
      v-for="(tag, index) in call.tag.split(',')"
      :key="index"
      :class="'tag-label ' + tagClass(tag.trim())"
  >
    {{ tag.trim() }}
  </span>
        </td>

        <td class="phone-number">{{ call.name }}</td>
      </tr>
      <tr v-if="filteredCalls.length === 0">
        <td colspan="5" class="no-results">
          <i class="fas fa-inbox"></i>
          <h3>No matching call records found</h3>
          <p>Please try other search criteria</p>
        </td>
      </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button v-for="page in totalPages" :key="page"
              @click="currentPage = page"
              :class="{active: currentPage === page}">
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'History',
  props: {
    calls: {
      type: Array,
      default: () => ([]),
    }
  },
  data() {
    return {
      searchQuery: '',
      timeFilter: 'all',
      sortBy: 'newest',
      currentPage: 1,
      itemsPerPage: 8,
    };
  },
  computed: {
    filteredCalls() {
      let result = [...this.calls];

      // 搜索过滤
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(call =>
            call.id.toLowerCase().includes(query) ||
            call.phoneNumber.toLowerCase().includes(query) ||
            call.summary.toLowerCase().includes(query)
        );
      }

      // 时间过滤
      if (this.timeFilter !== 'all') {
        const now = new Date();
        result = result.filter(call => {
          const callDate = new Date(call.startTime.split(' ')[0]);

          switch (this.timeFilter) {
            case 'today':
              return callDate.toDateString() === now.toDateString();
            case 'week':
              const oneWeekAgo = new Date(now);
              oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
              return callDate >= oneWeekAgo;
            case 'month':
              const oneMonthAgo = new Date(now);
              oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
              return callDate >= oneMonthAgo;
            default:
              return true;
          }
        });
      }

      // 排序
      result.sort((a, b) => {
        const dateA = new Date(a.startTime);
        const dateB = new Date(b.startTime);

        switch (this.sortBy) {
          case 'newest':
            return dateB - dateA;
          case 'oldest':
            return dateA - dateB;
          case 'longest':
            return b.duration - a.duration;
          case 'shortest':
            return a.duration - b.duration;
          default:
            return 0;
        }
      });

      // 分页
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return result.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.calls.length / this.itemsPerPage);
    }
  },
  methods: {
    viewCallDetail(call) {
      this.$router.push({
        name: 'ChatDetail',
        state: call,
      });
    },
    tagClass(tag) {
      const map = {
        'Product Information Inquiry': 'tag-product',
        'Sales Leads': 'tag-sales',
        'Technical Support': 'tag-support',
        'None': 'tag-none',
      };
      return map[tag] || 'tag-default';
    }
  }
};
</script>

<style scoped>
.history-container {
  padding: 25px;
  background: white;
  height: 100%;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-title h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin: 0;
}

.header-title .img {
  background-color: #3498db;
  mask: url('../assets/logo.png') no-repeat center;
  mask-size: cover;
  width: 30px;
  height: 30px;
}

.header-title i {
  font-size: 1.8rem;
  color: #3498db;
}

.search-box {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 50px;
  padding: 10px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  flex: 1;
  max-width: 400px;
}

.search-box input {
  border: none;
  background: transparent;
  padding: 8px 12px;
  width: 100%;
  font-size: 1rem;
  outline: none;
}

.search-box i {
  color: #6c757d;
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 180px;
}

.filter-item label {
  font-weight: 500;
  margin-bottom: 8px;
  color: #495057;
}

.filter-item select {
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid #ced4da;
  background: white;
  font-size: 1rem;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.history-table th {
  background: linear-gradient(135deg, #3498db, #2c80b9);
  color: white;
  text-align: left;
  padding: 18px 20px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

.history-table th i {
  margin-right: 8px;
}

.history-table tr {
  border-bottom: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.history-table tr:last-child {
  border-bottom: none;
}

.history-table tr:hover {
  background-color: #f1f8ff;
  cursor: pointer;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.history-table td {
  padding: 18px 20px;
  color: #495057;
  font-size: 1.05rem;
}

.call-id {
  font-weight: 600;
  color: #2c3e50;
}

.start-time {
  color: #3498db;
  font-weight: 500;
}

.duration {
  display: inline-block;
  padding: 5px 12px;
  border-radius: 20px;
  background: #e8f4ff;
  color: #2c80b9;
  font-weight: 500;
}

.phone-number {
  font-weight: 500;
  color: #2c3e50;
}

.summary {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  gap: 10px;
}

.pagination button {
  padding: 10px 18px;
  border: none;
  background: #f1f8ff;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.pagination button:hover {
  background: #3498db;
  color: white;
}

.pagination button.active {
  background: #3498db;
  color: white;
}

.no-results {
  text-align: center;
  padding: 50px;
  color: #6c757d;
}

.no-results i {
  font-size: 3rem;
  color: #ced4da;
  margin-bottom: 20px;
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .history-table {
    display: block;
    overflow-x: auto;
  }

  .header-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-box {
    max-width: 100%;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .history-table th,
  .history-table td {
    padding: 14px 12px;
    font-size: 0.95rem;
  }

  .header-title h2 {
    font-size: 1.5rem;
  }

  .filter-item {
    min-width: 140px;
  }
}

@media (max-width: 600px) {
  .history-container {
    padding: 15px;
  }

  .filter-section {
    flex-direction: column;
    gap: 10px;
  }

  .filter-item {
    width: 100%;
  }
}

.tag-label {
  display: inline-block;
  padding: 4px 10px;
  margin: 2px 6px 2px 0;
  border-radius: 12px;
  font-size: 0.82rem;
  font-weight: 500;
  color: white;
  white-space: nowrap;
}

.tag-product {
  background-color: #007bff;
}

.tag-sales {
  background-color: #fd7e14;
}

.tag-support {
  background-color: #28a745;
}

.tag-none {
  background-color: #6c757d;
}

.tag-default {
  background-color: #adb5bd;
}

</style>