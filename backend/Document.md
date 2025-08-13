以下是 MedBrief 后端 API 文档的中文翻译：

# MedBrief 后端 API 文档

本文档提供了 MedBrief 后端 API 的详细说明。

## 基础 URL

`http://localhost:8000`

---

## 主题管理 API

### 1. 创建主题

- **方法：** `POST`
- **端点：** `/topics/`
- **描述：** 创建一个新的主题用于跟踪。
- **状态码：** `201 Created`

- **请求体：**

```json
{
  "name": "string",
  "keywords": [
    "string"
  ],
  "related_items": [
    "string"
  ],
  "settings": {
    "frequency": "daily",
    "custom_date_range": "string",
    "detection_time": "HH:MM:SS",
    "notification_channels": [
      "email"
    ]
  },
  "ppt_settings": {
    "template": "string",
    "content_scope": [
      "summary"
    ],
    "auto_save": true
  }
}
```


- **响应体：**

```json
{
  "name": "string",
  "keywords": [
    "string"
  ],
  "related_items": [
    "string"
  ],
  "id": 0,
  "created_at": "YYYY-MM-DDTHH:MM:SS.ffffff",
  "last_updated": "YYYY-MM-DDTHH:MM:SS.ffffff",
  "frequency": "daily",
  "custom_date_range": "string",
  "detection_time": "HH:MM:SS",
  "notification_channels": [
    "email"
  ],
  "template": "string",
  "content_scope": [
    "summary"
  ],
  "auto_save": true
}
```


### 2. 列出主题

- **方法：** `GET`
- **端点：** `/topics/`
- **描述：** 获取所有主题的列表。
- **查询参数：**
    - `skip`（可选，整数，默认值：0）：跳过的记录数。
    - `limit`（可选，整数，默认值：100）：返回的最大记录数。
- **状态码：** `200 OK`
- **响应体：** Topic 对象数组（参见"创建主题"的响应）。

### 3. 获取主题

- **方法：** `GET`
- **端点：** `/topics/{topic_id}`
- **描述：** 获取特定主题的详细信息。
- **路径参数：**
    - [topic_id](file:///Users/admin/Documents/yifu/MedBrief/backend/models.py#L34-L34)（必需，整数）：要获取的主题 ID。
- **状态码：**
    - `200 OK`
    - `404 Not Found`：如果指定 ID 的主题不存在。
- **响应体：** 单个 Topic 对象。

### 4. 更新主题

- **方法：** `PUT`
- **端点：** `/topics/{topic_id}`
- **描述：** 更新现有主题。
- **路径参数：**
    - [topic_id](file:///Users/admin/Documents/yifu/MedBrief/backend/models.py#L34-L34)（必需，整数）：要更新的主题 ID。
- **状态码：**
    - `200 OK`
    - `404 Not Found`：如果指定 ID 的主题不存在。
- **请求体：** 与"创建主题"相同。
- **响应体：** 更新后的 Topic 对象。

### 5. 删除主题

- **方法：** `DELETE`
- **端点：** `/topics/{topic_id}`
- **描述：** 删除一个主题。
- **路径参数：**
    - [topic_id](file:///Users/admin/Documents/yifu/MedBrief/backend/models.py#L34-L34)（必需，整数）：要删除的主题 ID。
- **状态码：**
    - `204 No Content`：删除成功。
    - `404 Not Found`：如果指定 ID 的主题不存在。

### 6. 获取主题更新历史

- **方法：** `GET`
- **端点：** `/topics/{topic_id}/history`
- **描述：** 获取特定主题的更新历史。
- **路径参数：**
    - [topic_id](file:///Users/admin/Documents/yifu/MedBrief/backend/models.py#L34-L34)（必需，整数）：主题的 ID。
- **状态码：**
    - `200 OK`
    - `404 Not Found`：如果指定 ID 的主题不存在。
- **响应体：**

```json
{
  "topic_id": 0,
  "updates": [
    {
      "timestamp": "YYYY-MM-DDTHH:MM:SS.ffffff",
      "status": "success",
      "ppt_preview_link": "string"
    }
  ]
}
```


---

## 文献更新 API

### 1. 获取近期文献

- **方法：** `GET`
- **端点：** `/literature/`
- **描述：** 获取近期的文献更新。（注意：目前返回数据库中的数据，可能为空）。
- **查询参数：**
    - `skip`（可选，整数，默认值：0）：跳过的记录数。
    - `limit`（可选，整数，默认值：100）：返回的最大记录数。
- **状态码：** `200 OK`
- **响应体：** Literature 对象数组。

```json
{
  "id": 0,
  "title": "string",
  "authors": [
    "string"
  ],
  "publication_date": "YYYY-MM-DDTHH:MM:SS.ffffff",
  "journal_name": "string",
  "keywords": [
    "string"
  ],
  "summary": "string",
  "literature_type": "string"
}
```


---

## PPT 推送历史 API

### 1. 获取 PPT 推送历史

- **方法：** `GET`
- **端点：** `/ppt-history/`
- **描述：** 获取 PPT 推送的历史记录。（注意：目前返回数据库中的数据，可能为空）。
- **查询参数：**
    - `skip`（可选，整数，默认值：0）：跳过的记录数。
    - `limit`（可选，整数，默认值：100）：返回的最大记录数。
- **状态码：** `200 OK`
- **响应体：** PPTPushRecord 对象数组。

```json
{
  "id": 0,
  "push_time": "YYYY-MM-DDTHH:MM:SS.ffffff",
  "topic_name": "string",
  "ppt_filename": "string",
  "recipients": [
    "string"
  ],
  "channel": "string",
  "status": "success"
}
```
