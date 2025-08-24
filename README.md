# Irys Faucet Bot

这是一个用于自动领取 Irys 水龙头代币的 Python 脚本。该脚本支持批量处理多个钱包地址，并通过代理服务器和验证码服务来完成自动化领取。

## irys游戏（近期会更新游戏脚本）
- 打字游戏
- https://spritetype.irys.xyz
- 贪吃蛇游戏
- https://play.irys.xyz/

## 功能特性

- 🚀 批量处理多个钱包地址
- 🔐 自动处理 Turnstile CAPTCHA 验证
- 🌐 支持代理服务器
- ⚙️ 配置文件管理
- 📊 详细的执行日志
- 🛡️ 错误处理和重试机制

## 环境要求

- Python 3.7+
- requests 库

## 安装步骤

1. 克隆或下载项目文件
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 配置说明

### 1. 配置文件 (config.json)

编辑 `config.json` 文件，填入你的配置信息：

```json
{
  "api_key": "你的yescaptcha的api",
  "site_key": "0x4AAAAAAA6vnrvBCtS4FAl-",
  "website_url": "https://irys.xyz/faucet",
  "address_file": "address.txt",
  "proxy_file": "proxies.txt",
  "captcha_wait_time": 5,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
```

**配置项说明：**
- `api_key`: YesCaptcha 服务的 API 密钥
- `site_key`: Turnstile 验证码的站点密钥
- `website_url`: Irys 水龙头网站地址
- `address_file`: 钱包地址文件名
- `proxy_file`: 代理服务器文件名
- `captcha_wait_time`: 验证码轮询等待时间（秒）
- `user_agent`: HTTP 请求的用户代理字符串

### 2. 钱包地址文件 (address.txt)

在 `address.txt` 文件中，每行填入一个钱包地址：

```
0x1234567890abcdef1234567890abcdef12345678
0xabcdef1234567890abcdef1234567890abcdef12
0x9876543210fedcba9876543210fedcba98765432
```

### 3. 代理服务器文件 (proxies.txt)

在 `proxies.txt` 文件中，每行填入一个代理服务器地址，格式为 `http://用户名:密码@IP:端口`：

```
http://username:password@proxy1.example.com:8080
http://username:password@proxy2.example.com:8080
http://username:password@proxy3.example.com:8080
```

**注意：** 钱包地址和代理服务器的数量必须一致，脚本会按行号一一对应使用。

## 使用方法

1. 确保所有配置文件都已正确设置
2. 运行脚本：
   ```bash
   python bot.py
   ```

## 运行示例

```
📋 共加载 3 个地址和代理
🚀 开始批量领取...

🚀 [1/3] 开始领取：0x1234...5678（代理：http://proxy1.example.com:8080）
⏳ 等待 CAPTCHA：0x1234...5678
✅ 成功领取 0x1234...5678：Successfully claimed tokens
-----------------------------
🚀 [2/3] 开始领取：0xabcd...ef12（代理：http://proxy2.example.com:8080）
⏳ 等待 CAPTCHA：0xabcd...ef12
✅ 成功领取 0xabcd...ef12：Successfully claimed tokens
-----------------------------
🚀 [3/3] 开始领取：0x9876...5432（代理：http://proxy3.example.com:8080）
⏳ 等待 CAPTCHA：0x9876...5432
✅ 成功领取 0x9876...5432：Successfully claimed tokens
-----------------------------
🎉 所有任务完成！
```

## 错误处理

脚本包含完善的错误处理机制：

- **配置文件错误**：检查 config.json 格式和必要字段
- **文件不存在**：检查 address.txt 和 proxies.txt 是否存在
- **数量不匹配**：确保地址和代理数量一致
- **网络错误**：自动处理网络超时和连接错误
- **API 错误**：显示详细的 API 响应错误信息

## 注意事项

1. **API 密钥**：请确保 YesCaptcha API 密钥有效且有足够余额
2. **代理质量**：使用高质量的代理服务器以提高成功率
3. **频率限制**：注意 Irys 水龙头的频率限制，避免过于频繁的请求
4. **网络环境**：确保网络连接稳定
5. **Python 版本**：建议使用 Python 3.7 或更高版本

## 文件结构

```
irys-faucet/
├── bot.py              # 主程序文件
├── config.json         # 配置文件
├── requirements.txt    # Python 依赖包
├── address.txt         # 钱包地址文件
├── proxies.txt         # 代理服务器文件
└── README.md          # 说明文档
```

## 许可证

本项目仅供学习和研究使用，请遵守相关网站的使用条款和法律法规。
