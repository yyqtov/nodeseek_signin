### 使用说明

#### 1. 配置环境变量

本脚本需要两个主要的环境变量：

- **`NODESEEK_COOKIE`**：用于存储你在 `www.nodeseek.com` 登录后获取的 Cookie，用于签到。
- **`TG_BOT_TOKEN`** 和 **`TG_USER_ID`**：用于发送 Telegram 通知，分别是你 Telegram 机器人 token 和用户 ID。

##### 获取 **`NODESEEK_COOKIE`**：
1. 打开 [www.nodeseek.com](https://www.nodeseek.com) 并登录账号。
2. 按下 **F12** 打开开发者工具，进入 **Network** 面板。
3. 刷新页面，查看网络请求，找到请求到 `www.nodeseek.com` 的请求。
4. 在请求头中找到 `Cookie` 字段，复制整个内容（例如：`__cfduid=xyz; sessionid=abc123;`）。
5. 将这个复制的 Cookie 添加到环境变量中。
   - 如果有多个账号，可以将每个 Cookie 用 `&` 连接（例如：`cookie1&cookie2&cookie3`）。

##### 获取 **Telegram Bot Token** 和 **Chat ID**：

1. [创建一个 Telegram Bot](https://blog.xiny.cc/archives/mTaUz0TW)（请参考教程）。
2. 将 Bot Token 和 Chat ID 添加到环境变量中。

##### 在 Linux 和 Windows 中设置环境变量：

- **Linux/MacOS**：
    在终端中输入以下命令来设置环境变量：
    ```bash
    export NODESEEK_COOKIE="cookie1&cookie2&cookie3"  # 替换为你获取的cookie
    export TG_BOT_TOKEN="your_telegram_bot_token"  # 替换为你的Telegram Bot Token
    export TG_USER_ID="your_telegram_chat_id"  # 替换为你的Telegram用户ID
    ```

- **Windows**：
    1. 在开始菜单搜索 **“环境变量”**，点击 **“编辑系统环境变量”**。
    2. 在 **“系统属性”** 窗口中点击 **“环境变量”** 按钮。
    3. 在 **“用户变量”** 中，点击 **“新建”**，输入变量名和值：
        - 变量名：`NODESEEK_COOKIE`，值：`cookie1&cookie2&cookie3`（多个cookie用&分隔）
        - 变量名：`TG_BOT_TOKEN`，值：`your_telegram_bot_token`
        - 变量名：`TG_USER_ID`，值：`your_telegram_chat_id`
    4. 点击 **“确定”** 保存并关闭窗口。

#### 2. 运行脚本

1. 安装`cloudscraper` 库和`requests` 库。
    ```bash
    pip install cloudscraper requests
    ```

2. 运行脚本：
    ```bash
    python nodeseek_signin.py
    ```

#### 3. 脚本功能

- **多账号**：支持多账号 Cookie 进行签到。
- **延迟设置**：每次签到前，脚本会随机等待 20 到 59 分钟，模拟用户签到的非准时现象。
- **异常通知**：如果脚本发生错误或签到失败，会通过 Telegram 发送通知。
