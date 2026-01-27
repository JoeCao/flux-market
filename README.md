# 股票市场K线图展示系统

一个基于 Vue 3 + FastAPI 的股票K线图可视化系统，支持查看美股实时K线数据和技术指标。

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Vite** - 快速的构建工具
- **ECharts** - 强大的数据可视化库
- **Axios** - HTTP 客户端

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **akshare** - 金融数据获取库
- **pandas** - 数据处理
- **uvicorn** - ASGI 服务器

## 项目结构

```
flux-market/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口
│   │   ├── api/            # API 路由
│   │   ├── services/       # 业务逻辑
│   │   └── models/         # 数据模型
│   ├── requirements.txt    # Python 依赖
│   └── run.py             # 启动脚本
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   ├── views/         # 页面视图
│   │   ├── api/           # API 调用
│   │   └── types/         # TypeScript 类型
│   └── package.json
│
└── venv/                  # Python 虚拟环境
```

## 功能特性

- ✅ 实时获取美股K线数据
- ✅ 支持自定义日期范围查询
- ✅ 显示 MA5/MA10/MA20 移动平均线
- ✅ 成交量柱状图
- ✅ 支持前复权/后复权/不复权
- ✅ 交互式图表（缩放、拖拽、数据提示）
- ✅ 响应式设计

## 快速开始

### 1. 环境要求

- Python 3.11+
- Node.js 16+
- npm 或 yarn

### 2. 安装依赖

**后端依赖：**
```bash
# 激活虚拟环境
source venv/bin/activate

# 安装 Python 依赖
pip install -r backend/requirements.txt
```

**前端依赖：**
```bash
# 进入前端目录
cd frontend

# 安装 npm 依赖
npm install
```

### 3. 启动服务

**启动后端服务：**
```bash
# 在项目根目录
cd backend
source ../venv/bin/activate
python run.py
```

后端服务将在 http://localhost:8000 启动

**启动前端服务：**
```bash
# 在项目根目录
cd frontend
npm run dev
```

前端服务将在 http://localhost:5173 启动

### 4. 访问应用

打开浏览器访问：http://localhost:5173

## 使用说明

1. **输入股票代码**：在顶部输入框输入美股代码（如 AAPL, TSLA, GOOGL）
2. **选择日期范围**：可选，默认显示最近30天数据
3. **选择复权方式**：前复权/后复权/不复权
4. **点击查询**：系统将获取并展示K线图

## API 文档

后端服务启动后，访问 http://localhost:8000/docs 查看自动生成的 Swagger API 文档。

### 主要接口

**获取K线数据：**
```
GET /api/stock/kline?symbol=AAPL&start_date=2026-01-01&end_date=2026-01-26&adjust=qfq
```

参数：
- `symbol`: 股票代码（必填）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `adjust`: 复权类型（可选，默认 qfq）

## 开发说明

### 后端开发

后端使用 FastAPI 框架，支持热重载：

```bash
cd backend
source ../venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 前端开发

前端使用 Vite，支持热模块替换（HMR）：

```bash
cd frontend
npm run dev
```

### 构建生产版本

**前端构建：**
```bash
cd frontend
npm run build
```

构建产物将输出到 `frontend/dist` 目录。

## 扩展功能建议

- [ ] 支持更多技术指标（MACD、KDJ、RSI、布林带）
- [ ] 多股票对比功能
- [ ] 实时数据推送（WebSocket）
- [ ] 自选股管理
- [ ] 数据导出（CSV、图片）
- [ ] 深色/浅色主题切换
- [ ] 移动端适配

## 常见问题

**Q: 后端启动失败？**
A: 确保已激活虚拟环境并安装所有依赖。检查 Python 版本是否为 3.11+。

**Q: 前端无法连接后端？**
A: 确保后端服务已启动在 8000 端口，检查 CORS 配置。

**Q: 股票数据获取失败？**
A: 检查网络连接，某些股票代码可能不存在或数据源暂时不可用。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**开发时间**: 2026-01-26
**技术支持**: Claude Sonnet 4.5
