# Sentry DingTalk

Sentry 集成钉钉机器人通知

## Requirments 
- sentry >= 21.5.1

## 特性
- 发送异常通知到钉钉
- 支持钉钉关键字、签名
## 快速使用
### 安装
1. 使用 `pip` 命令
    ```bash
    $ pip install 
    ```

2. 写入依赖文件 `onpremise-xxx/sentry/requirements.txt`
    ```bash
    $ echo https://github.com/lostncg/sentry-dingtalk/archive/master.zip >> requirements.txt
    ```

### 钉钉机器人
[配置](https://developers.dingtalk.com/document/app/custom-robot-access)钉钉机器人并拿到对应的 webhook, 可以对机器人设置 关键词、签名、IP限制

### 配置
在 Sentry 面板 Settings > Integrations 中找到 DingTalk 并配置 webhook、关键词等信息，添加项目，创建告警规则

### 测试
1. Enable Plugin
2. Test Plugin
