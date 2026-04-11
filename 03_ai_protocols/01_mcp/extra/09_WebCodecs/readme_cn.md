# WebCodecs：浏览器中的底层媒体编解码能力

WebCodecs 是浏览器里的低层媒体 API，用于直接访问系统内置的音视频编码器和解码器，通常还能利用硬件加速。它不是“播放媒体”的 API，而是“处理原始帧和编码块”的 API，适合高性能实时媒体场景。

---

## WebCodecs 的核心概念

1. **编码器 / 解码器**
   - `VideoEncoder`
   - `VideoDecoder`
   - `AudioEncoder`
   - `AudioDecoder`

2. **配置对象**
   可以指定 codec、分辨率、码率、帧率、延迟模式等。

3. **数据对象**
   - `VideoFrame`
   - `AudioData`
   - `EncodedVideoChunk`
   - `EncodedAudioChunk`

4. **异步回调**
   编码和解码结果通过 `output` 回调返回，错误通过 `error` 回调处理。

5. **与其他 Web API 协作**
   WebCodecs 常与以下技术组合：
   - MediaStreamTrack
   - WebRTC
   - WebTransport / WebSocket
   - WebGL / WebGPU

---

## Python 的角色：服务端媒体处理

WebCodecs 本身是**浏览器 API**，不是 Python 库。Python 一般负责服务端处理，常见做法是使用 **PyAV（FFmpeg 绑定）** 来：

- 生成原始视频帧
- 编码视频文件
- 解码浏览器上传的编码数据
- 为 WebCodecs 客户端准备兼容媒体流

### 安装

```bash
pip install av numpy
```

或：

```bash
uv pip install av numpy
```

### 原文中的 Python 示例

原文提供了 `python_media_processor.py`，核心演示三件事：

1. 生成原始视频帧（NumPy 数组）
2. 用 PyAV 将帧编码成 MP4 文件
3. 再把编码后的视频解码回来，模拟服务端接收客户端媒体数据后的处理流程

这个例子本质上说明：

- 浏览器用 WebCodecs 负责前端编解码
- Python 服务端用 PyAV 等库负责后端媒体处理
- 二者通过 WebTransport / WebSocket / WebRTC 等通道交换编码块或原始帧

---

## 优势

- 提供对媒体处理的细粒度控制
- 可利用浏览器内建和硬件加速 codec
- 不必在前端引入大型 JS / WASM codec 包
- 适合实时视频处理、云游戏、浏览器内剪辑等场景

## 局限

- API 偏底层，使用复杂度高
- 仅限浏览器侧
- 不负责媒体容器处理（如 MP4 封装）
- 编码能力受浏览器与操作系统支持限制

---

## 常见用途

- 浏览器内视频编辑
- 低延迟流媒体客户端
- 实时视频特效与分析
- 浏览器端转码 / 片段重编码
- 与 WebRTC / WebTransport 组合构建自定义媒体链路

---

## WebCodecs 在 DACA / Agent 系统中的意义

WebCodecs 更偏向 **DACA 的前端边界层能力**：

- 浏览器 UI 中解码来自后端 agent 的视频 / 音频流
- 将用户摄像头或麦克风数据编码后上传给后端 agent
- 支持更复杂的多模态交互，如实时视觉分析、视频理解、边缘推理展示

后端 Python agent 自己不会直接调用 WebCodecs，但会配合 PyAV、FFmpeg、GStreamer 等工具与前端完成媒体协同。

---

## 进一步阅读

- [MDN WebCodecs API](https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API)
- [WebCodecs Samples](https://github.com/GoogleChromeLabs/webcodecs-samples)
- [PyAV Documentation](https://pyav.org/docs/stable/)
