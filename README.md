# MCP Collection

一个功能丰富的MCP（Model Context Protocol）工具集合，提供邮件处理、文件系统操作、文本转语音和自动视频编辑等功能。

## 项目安装与启动

### 环境要求

- Python 3.8+
- macOS/Linux/Windows

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd mcp_collection
   ```

2. **创建虚拟环境**
   ```bash
   # 使用uv（推荐）
   uv venv
   source .venv/bin/activate  # macOS/Linux
   # 或者 .venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   uv sync
   # 或者
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   复制环境变量模板并配置：
   ```bash
   cp .env.example .env
   ```
   
   编辑 `.env` 文件，添加必要的API密钥：
   ```env
   ALI_KEY=your_alibaba_cloud_api_key
   ```

5. **启动服务**
   ```bash
   python main.py
   ```

   服务将在 http://localhost:8000 启动，使用SSE（Server-Sent Events）传输协议。

## 功能说明

### 📧 邮件处理工具

#### `get_last_email`
获取指定邮箱中最新的邮件内容。

| 参数 | 类型 | 说明 |
|---|---|---|
| `imap_server` | string | IMAP服务器地址 |
| `port` | int | IMAP服务器端口（993/143） |
| `email_address` | string | 邮箱地址 |
| `password` | string | 邮箱密码 |
| `inbox` | string | 收件箱名称（"INBOX"） |
| `subject` | string | 邮件主题关键词（可选） |

**返回：** 邮件内容字符串，未找到返回空字符串

### 📁 文件系统工具

#### `read_file`
读取指定文件的内容。

| 参数 | 类型 | 说明 |
|---|---|---|
| `file_path` | string | 文件路径 |

**返回：** 文件内容字符串

#### `write_file`
将内容写入指定文件。

| 参数 | 类型 | 说明 |
|---|---|---|
| `file_path` | string | 目标文件路径 |
| `content` | string | 要写入的内容 |

**返回：** "success"（成功）或抛出异常

#### `copy_dir`
复制源目录到目标目录。

| 参数 | 类型 | 说明 |
|---|---|---|
| `from_path` | string | 源目录路径 |
| `to_path` | string | 目标目录路径 |

**返回：** "success"（成功）或抛出FileNotFoundError

### 🔊 文本转语音工具

#### `create_text_to_audio`
将文本转换为音频文件。

| 参数 | 类型 | 说明 |
|---|---|---|
| `text` | string | 要转换的文本内容 |
| `out_path` | string | 输出音频文件路径 |

**返回：** "Success"（成功）或"Failed"（失败）

### 🎬 自动视频编辑工具

#### `auto_cut`
基于剪映草稿的自动视频编辑。

| 参数 | 类型 | 说明 |
|---|---|---|
| `draft_path` | string | 剪映草稿文件路径 |

**返回：** "Success"（成功）

### 🛠️ 技术栈

- **MCP框架**: FastMCP (Model Context Protocol)
- **邮件处理**: imaplib, email
- **文件操作**: os, shutil
- **语音合成**: 阿里巴巴CosyVoice API
- **视频编辑**: pyJianYingDraft (剪映API)
- **异步通信**: Server-Sent Events (SSE)

### 📋 开发指南

#### 添加新工具

1. 在相应的模块文件中添加功能函数
2. 在 `main.py` 中使用 `@mcp.tool()` 装饰器注册新工具
3. 添加详细的docstring说明参数和返回值

#### 测试工具

可以使用任何MCP客户端测试工具功能，例如：

```python
from mcp import Client

client = Client("http://localhost:8000")
result = client.call_tool("read_file", {"file_path": "/path/to/test.txt"})
```

### 🔧 故障排除

#### 常见问题

1. **端口被占用**
   - 检查8000端口是否被占用：`lsof -i :8000`
   - 修改main.py中的端口配置

2. **API密钥错误**
   - 确认.env文件中ALI_KEY已正确配置
   - 检查阿里云API密钥权限

3. **邮件连接失败**
   - 确认邮箱IMAP服务已开启
   - 检查防火墙设置
   - 验证邮箱账号密码正确性

4. **视频编辑失败**
   - 确认剪映草稿文件路径正确
   - 检查必要的素材文件是否存在
   - 验证pyJianYingDraft库安装正确

### 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件