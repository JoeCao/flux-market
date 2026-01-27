#!/bin/bash

# 一键启动前后端服务
# 后端: FastAPI (端口 8000)
# 前端: Vite (端口 5173)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Stock Market Terminal 启动脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 清理函数：退出时终止所有子进程
cleanup() {
    echo ""
    echo -e "${YELLOW}正在停止服务...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo -e "${GREEN}服务已停止${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 检查 Python 虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${RED}错误: 未找到 Python 虚拟环境 (venv)${NC}"
    echo "请先运行: python3 -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt"
    exit 1
fi

# 检查 node_modules
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}前端依赖未安装，正在安装...${NC}"
    cd frontend && npm install && cd ..
fi

# 启动后端
echo -e "${GREEN}[1/2] 启动后端服务 (FastAPI)...${NC}"
source venv/bin/activate
cd backend
python run.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 2

# 启动前端
echo -e "${GREEN}[2/2] 启动前端服务 (Vite)...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  服务启动成功!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "  后端地址: ${YELLOW}http://localhost:8000${NC}"
echo -e "  前端地址: ${YELLOW}http://localhost:5173${NC}"
echo -e "  API 文档: ${YELLOW}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
echo ""

# 等待子进程
wait
