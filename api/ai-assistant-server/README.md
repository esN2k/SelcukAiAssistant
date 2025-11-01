# AI Assistant 语音服务

这是AI助手应用的语音识别服务API文档。

## 功能特性

- 支持多种音频格式：WAV, MP3, M4A
- 支持多语言识别：中文、英文、日文、韩文
- 实时语音转文字
- 高准确率识别

## API 接口

### 语音转文字

- **接口地址**: `POST /api/speech-to-text`
- **请求格式**: `multipart/form-data`
- **参数**:
    - `audio`: 音频文件（必需）
    - `language`: 识别语言，默认 `zh-CN`

### 健康检查

- **接口地址**: `GET /api/health`
- **用途**: 检查服务状态

## 使用示例

### cURL 示例

```bash
curl -X POST \
  http://localhost:8080/api/speech-to-text \
  -H 'Content-Type: multipart/form-data' \
  -F 'audio=@/path/to/audio.wav' \
  -F 'language=zh-CN'
```

### 响应示例

```json
{
  "success": true,
  "text": "你好，这是一段测试语音",
  "confidence": 0.95,
  "duration": 3.2
}
```

## 部署说明

1. 确保服务器支持音频处理
2. 配置相应的语音识别引擎（如：百度语音、讯飞语音、Google Speech等）
3. 设置合适的文件上传限制
4. 配置CORS策略以支持跨域请求

## 错误处理

- `400`: 请求参数错误
- `413`: 文件过大
- `415`: 不支持的音频格式
- `500`: 服务器内部错误

## 安全考虑

- 建议使用HTTPS协议
- 实现API密钥认证
- 限制文件大小和请求频率
- 及时清理临时音频文件