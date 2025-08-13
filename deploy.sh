#!/usr/bin/env bash
set -e

#######################################
#           参数与变量定义
#######################################
WORK_DIR="/data/prod_medBrief/MedBrief"
ENV_FILE=".env_prod"
BRANCH_NAME="master"

# ANSI color
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log() {
  echo -e "${GREEN}======== [ $1 ] ========${NC}"
}

#######################################
#           步骤 0：更新代码
#######################################
update_code() {
  log "Step 0: 拉取最新代码"
  cd "$WORK_DIR"
  git fetch
  git checkout "$BRANCH_NAME" || { echo "Error: 切换分支 $BRANCH_NAME 失败"; exit 1; }
  git reset --hard
  git pull --rebase || { echo "Error: Git pull 失败，可能存在未提交的更改"; exit 1; }
  echo "当前所在分支: $(git branch)"
}

#######################################
#           步骤 1：替换配置文件
#######################################
replace_config_files() {
  log "Step 1: 拷贝配置文件"
  cp "$WORK_DIR/frontend/$ENV_FILE" "$WORK_DIR/frontend/.env"
}

#######################################
#           步骤 2：安装依赖
#######################################


#######################################
#           步骤 3：构建并启动容器（后端）
#######################################
restart_backend_frontend() {
  log "Step 3: 重启前后端容器"
  cd "$WORK_DIR"
#  docker compose down || true
  docker compose up --build -d
}

#######################################
#           主执行流程
#######################################
main() {
  update_code
  replace_config_files
  restart_backend_frontend
  log "🎉 系统部署完成！"
}

main "$@"
