# MQTT：轻量级发布 / 订阅消息协议

MQTT（Message Queuing Telemetry Transport）是一种基于 **发布/订阅模型** 的轻量级消息协议，特别适合低带宽、高延迟、不稳定网络以及资源受限设备，因此在 IoT、移动端、传感器网络和事件驱动系统里非常常见。

---

## 核心概念

1. **发布 / 订阅模型**
   - **Publisher**：发布消息
   - **Subscriber**：订阅消息
   - **Broker**：中间消息代理
   - **Topic**：主题路径，例如 `agents/status/alpha`

2. **Broker**
   所有消息都经由 broker 转发。它负责连接管理、订阅管理、QoS 处理和消息路由。

3. **QoS（服务质量）**
   - **QoS 0**：最多一次
   - **QoS 1**：至少一次
   - **QoS 2**：恰好一次

4. **Retained Message**
   broker 为某个 topic 保存最后一条保留消息，新订阅者会立刻拿到。

5. **Last Will and Testament（LWT）**
   客户端异常断开时，由 broker 自动发布“遗嘱消息”，通知其他订阅者它已离线。

6. **Clean Session / Persistent Session**
   - Clean：每次连接都从零开始
   - Persistent：保留订阅和离线期间的 QoS 1/2 消息

7. **Keep Alive**
   客户端与 broker 定期保活，否则 broker 会判定掉线。

---

## Python 中使用 MQTT：`paho-mqtt`

### 安装

```bash
pip install paho-mqtt
```

或：

```bash
uv pip install paho-mqtt
```

### 运行前提

你需要一个 MQTT broker，例如：

- 本地 Mosquitto
- `test.mosquitto.org`
- `broker.hivemq.com`
- 云端托管 MQTT 服务

### 原文示例内容

原文提供了一个 `mqtt_combined_client.py`，同时演示：

- 连接 broker
- 订阅一个唯一 topic
- 向该 topic 发布消息
- 接收自己订阅到的消息
- 设置 LWT
- 发布在线 / 离线状态

代码里重点展示了：

- `on_connect`
- `on_disconnect`
- `on_subscribe`
- `on_publish`
- `on_message`
- `client.will_set(...)`
- `client.loop_start()`

这对理解 MQTT 的典型使用方式非常有帮助。

---

## 优势

- 协议头极小，适合弱网络与低功耗设备
- 发布 / 订阅解耦，扩展性强
- 支持不同级别的可靠性保障
- LWT 和保留消息非常适合状态同步
- 生态成熟，跨语言支持广

## 局限

- 依赖 broker，broker 可能成为单点
- 标准 MQTT 基于 TCP，不是最低时延方案
- topic 层级简单，复杂路由要额外设计
- 安全认证与细粒度授权通常依赖 broker 配置

---

## 常见用途

- IoT 设备上报与控制
- 工业监控
- 智能家居
- 遥测、状态广播、告警通知
- 轻量级事件总线

---

## MQTT 在 DACA / A2A 中的意义

MQTT 很适合 DACA 里的事件驱动型 A2A 场景：

- agent 发布状态、心跳、遥测
- 多个 agent 订阅同一事件源
- 边缘设备 agent 与中心 agent 间低成本通信
- 对关键事件使用 QoS 1 / 2 做可靠传递

如果结合 Dapr Pub/Sub，agent 往往无需直接面对 broker 细节，只需面向 Dapr 的统一接口开发。

---

## 协议栈位置

- **层级**：应用层（Layer 7）
- **下层**：通常是 TCP/IP

---

## 进一步阅读

- [MQTT.org](https://mqtt.org/)
- [MQTT 5.0 Standard](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html)
- [Eclipse Paho Python Client](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [HiveMQ MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
