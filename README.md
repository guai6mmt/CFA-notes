# CFA 二级笔记站点

这个仓库使用 MkDocs Material 将 Markdown 笔记构建为适合手机阅读的网站，并由 Caddy 在服务器的 `8889` 端口提供访问。

## 本地预览

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\stage_docs.py
.\.venv\Scripts\mkdocs serve
```

访问 <http://127.0.0.1:8000>。

## 首次上传到 GitHub

先在 GitHub 网页中新建一个空的私有仓库，例如 `cfa-level-2-notes`。不要勾选自动生成 README。然后在当前目录运行：

```powershell
git config user.name "YOUR_GITHUB_NAME"
git config user.email "YOUR_GITHUB_EMAIL"
git add -A
git commit -m "Add CFA notes site deployment"
git remote add origin git@github.com:YOUR_GITHUB_USER/cfa-level-2-notes.git
git push -u origin main
```

如果使用 HTTPS 推送，将最后两行中的仓库地址替换为 GitHub 网页上显示的 HTTPS 地址。

## 首次部署

服务器需要安装 Git、Docker Engine 和 Docker Compose 插件。

```bash
git clone git@github.com:YOUR_GITHUB_USER/cfa-level-2-notes.git
cd cfa-level-2-notes
docker compose up -d --build
```

部署完成后直接访问：

```text
http://服务器IP:8889
```

如服务器启用了防火墙，请放行 TCP 端口 `8889`。站点不需要账号密码，能够访问该端口的人都可以直接查看笔记。

## 更新服务器

本地编辑笔记并推送到 GitHub 后，在服务器仓库目录运行：

```bash
git pull --ff-only
docker compose up -d --build
```

Docker 构建时会自动整理笔记文件。本地新增图片或修改笔记后，如需再次预览，请重新运行：

```powershell
.\.venv\Scripts\python scripts\stage_docs.py
```

服务器也可以直接运行：

```bash
bash scripts/deploy.sh
```

## GitHub 私有仓库

笔记建议存放在私有仓库中。服务器可以使用 SSH deploy key 拉取代码，避免保存个人 GitHub 密码。
