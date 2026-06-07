# CFA 二级笔记站点

这个仓库使用 MkDocs Material 构建 CFA Level II 笔记网站，并由 Docker 中的 Caddy 提供访问。默认地址为 `http://服务器IP:8889`。

## 服务器一键部署

服务器需要预先安装：

- Git
- curl
- Docker Engine
- Docker Compose 插件

首次部署和以后更新都可以执行同一条命令：

```bash
curl -fsSL https://raw.githubusercontent.com/guai6mmt/CFA-notes/main/scripts/install.sh | bash
```

脚本会自动完成以下操作：

1. 首次运行时，将仓库下载到 `~/CFA-notes`。
2. 已经部署过时，拉取 GitHub 上的最新代码。
3. 构建站点镜像并启动容器。
4. 等待健康检查通过，并输出访问地址。

部署成功后访问：

```text
http://服务器IP:8889
```

如果服务器启用了防火墙，需要放行 TCP 端口 `8889`。默认部署没有账号密码，能够访问该端口的人都可以查看笔记。

## HTTPS 和反向代理

如果服务器已经使用 Nginx、Caddy 等反向代理，建议只允许本机访问笔记容器。首次运行一键部署命令时增加两个环境变量：

```bash
curl -fsSL https://raw.githubusercontent.com/guai6mmt/CFA-notes/main/scripts/install.sh \
  | NOTES_BIND_ADDRESS=127.0.0.1 NOTES_PORT=8889 bash
```

配置会保存到 `~/CFA-notes/.env`，后续更新仍然只需执行普通的一键部署命令。`.env` 不会提交到 Git。

## 常用排查命令

查看容器状态：

```bash
cd ~/CFA-notes
docker compose ps
```

查看最近日志：

```bash
cd ~/CFA-notes
docker compose logs --tail=200 notes
```

查看首页是否正常响应：

```bash
curl --fail --show-error http://127.0.0.1:8889/
```

如果在 `.env` 中修改过 `NOTES_PORT`，将上面的 `8889` 替换为实际端口。

## 私有仓库部署

上面的一键命令适用于可以公开读取的 GitHub 仓库。如果以后将仓库改为私有仓库，需要先为服务器配置 GitHub SSH deploy key，然后首次执行：

```bash
git clone git@github.com:guai6mmt/CFA-notes.git ~/CFA-notes
bash ~/CFA-notes/scripts/deploy.sh
```

之后更新仍然只需执行：

```bash
bash ~/CFA-notes/scripts/deploy.sh
```

## 本地预览

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\stage_docs.py
.\.venv\Scripts\mkdocs serve
```

访问 <http://127.0.0.1:8000>。

Docker 构建时会自动整理笔记文件。本地新增图片或修改笔记后，如需再次预览，请重新运行 `scripts/stage_docs.py`。

## 日常修改后上传 GitHub

每次本地修改笔记或新增图片后，在当前仓库目录运行：

```powershell
git status
python scripts\stage_docs.py
git add -A
git commit -m "Update CFA notes"
git push origin main
```

如果只是少量文字修改，也可以跳过 `stage_docs.py`。提交前建议先看一眼 `git status`，确认本次改动都是要上传的内容。

## 其他说明

- 页面中的公式使用固定版本的 MathJax CDN。浏览器需要能够访问 `https://unpkg.com` 才能渲染公式。
- 一键部署脚本会先拉取代码、校验 Compose 配置、构建镜像，再等待站点通过健康检查。构建失败时不会替换当前正在运行的容器。
