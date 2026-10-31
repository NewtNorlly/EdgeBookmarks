# Edge Bookmarks

一个简单的、浏览器书签风格的网络书签页。

**Live:** https://newtnorlly.github.io/EdgeBookmarks/

## 这个仓库是什么

- `site/`：GitHub Pages 静态站点，无 JavaScript、无外部依赖。
- `site/index.html`：由 `scripts/build_site.py` 生成的公开书签页（229 条）。
- `site/data/bookmarks.json`：公开书签数据（A/B/C/S/D 五级，229 条）。
- `site/bookmarks-import.html`：229 条公开书签的可导入版本。
- `scripts/build_site.py`：把书签数据生成静态 HTML。
- `.github/workflows/deploy.yml`：push 到 `main` 后自动生成并部署 Pages。

`private/` 目录被 `.gitignore` 忽略，保存本地维护用的书签导出，**不会进入公开仓库**。

## 收藏分级

| 层级 | 内容 | 数量 |
|---|---|---:|
| A | 学术资源、正版影视 | 49 |
| B | 阅读、开发、影视、工具 | 73 |
| C | 影视资源（第三方小站） | 34 |
| S | 私人记录与自有资产 | 34 |
| D | 敏感内容 | 39 |
| **合计** |  | **229** |

## 页面设计

- 浏览器书签管理器式的双栏布局：左侧文件夹树，右侧书签列表。
- 瑞士风格网格：白纸、黑字、红色强调、细分割线、严格左对齐。
- 字体只用 **宋体 / SimSun** 与 **Times New Roman**。
- 全站最小字号 **20px**。
- 无搜索、无筛选、无卡片、无阴影、无圆角、无动画、无深色模式。
- 页面加了 `noindex, nofollow`，不被搜索引擎收录。

## 更新流程

1. 编辑 `site/data/bookmarks.json`。
2. 重新生成页面：

   ```powershell
   python scripts/build_site.py
   ```

3. 检查 `site/index.html`。
4. 提交并推送：

   ```powershell
   git add site scripts .github README.md .gitignore
   git commit -m "Update bookmarks"
   git push
   ```

5. GitHub Actions 会自动重新生成页面并发布 Pages。

## License

个人收藏数据，未授权请勿转载或再分发。
