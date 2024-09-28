name: Update V2Ray Subscription

on:
  schedule:
    - cron: '0 2 * * *'  # 每天 2:00 执行
  workflow_dispatch:  # 允许手动触发

permissions:
  contents: write  # 确保有推送权限

jobs:
  update_v2ray:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 确保检出完整历史

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests

      - name: Run process_v2ray.py
        run: |
          python python/process_v2ray.py  # 确保替换为您的脚本路径

      - name: Check if v2ray file was updated
        run: |
          if git diff --exit-code json/v2ray; then
            echo "No changes to json/v2ray"
            echo "changed=false" >> $GITHUB_ENV  # 使用环境文件设置输出变量
          else
            echo "Changes detected in json/v2ray"
            echo "changed=true" >> $GITHUB_ENV
          fi

      - name: Commit and push changes
        if: env.changed == 'true'
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add json/v2ray
          git commit -m 'Update V2Ray subscription file' || echo "No changes to commit."
          git push origin main || echo "Push failed; may be due to permissions or branch protection."
