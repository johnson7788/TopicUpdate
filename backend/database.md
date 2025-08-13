# MedBrief Pro 数据库结构文档

本文档详细说明了 MedBrief Pro 后端应用所使用的数据库表结构。数据库采用 SQLite，通过 SQLAlchemy ORM 进行管理。

---

## 1. `topics` - 监控主题表

此表存储用户创建的、需要长期追踪的文献主题的核心信息和配置。

| 字段名                  | 数据类型   | 描述                                     | 示例                           |
| ----------------------- | ---------- | ---------------------------------------- |------------------------------|
| `id`                    | Integer    | 主键，唯一标识符                         | `1`                          |
| `name`                  | String     | 用户定义的主题名称                       | `"糖尿病最新研究"`                  |
| `keywords`              | JSON       | 用于文献检索的核心关键词列表             | `["Diabetes", "GLP-1"]`      |
| `created_at`            | DateTime   | 记录创建时间                             | `"2025-08-12 10:00:00"`      |
| `last_updated`          | DateTime   | 记录最后更新时间                         | `"2025-08-12 10:00:00"`      |
| `frequency`             | String     | 文献更新的频率                           | `"daily"`, `"weekly"` `"monthly"` |    |
| `custom_date_range`     | String     | 自定义检测的日期范围 (可为空)            | `"2025-01-01 to 2025-03-01"` |
| `detection_time`        | Time       | 每日检测的时间点 (可为空)                | `"09:00:00"`                 |
| `notification_channels` | JSON       | 通知渠道列表                             | `["email", "app_push"]`      |
| `template`              | String     | 生成PPT时使用的模板名称                  | `"modern_blue"`              |

---

## 2. `update_records` - 主题更新历史表

记录了每个主题历次文献更新任务的执行情况。

| 字段名             | 数据类型 | 描述                                     | 示例                            |
| ------------------ | -------- | ---------------------------------------- |-------------------------------|
| `id`               | Integer  | 主键，唯一标识符                         | `101`                         |
| `topic_id`         | Integer  | 外键，关联到 `topics` 表的 `id`          | `1`                           |
| `timestamp`        | DateTime | 本次更新任务执行的时间戳                 | `"2025-08-12 09:05:00"`       |
| `status`           | String   | 更新任务的状态                           | `"success"`, `"failed"`       |
| `ppt_preview_link` | String   | 指向生成的PPT预览文件或下载地址 (可为空) | `"https://xxxx/topic_1.pptx"` |

---

## 3. `literature` - 文献信息表

存储通过监控主题检索到的所有文献的详细信息。

| 字段名             | 数据类型 | 描述                               | 示例                                      |
| ------------------ | -------- | ---------------------------------- | ----------------------------------------- |
| `id`               | Integer  | 主键，唯一标识符                   | `201`                                     |
| `topic_id`         | Integer  | 外键，关联到 `topics` 表的 `id`    | `1`                                       |
| `title`            | String   | 文献标题                           | `"Efficacy of GLP-1 in T2DM"`             |
| `authors`          | JSON     | 作者列表                           | `["Smith J", "Johnson A"]`              |
| `publication_date` | DateTime | 发表日期                           | `"2025-07-20 00:00:00"`                   |
| `journal_name`     | String   | 发表期刊的名称                     | `"The Lancet"`                            |
| `keywords`         | JSON     | 文献自带的关键词列表               | `["T2DM", "Cardiovascular"]`            |
| `summary`          | Text     | 文献摘要                           | `"This study evaluates the..."`           |
| `literature_type`  | String   | 文献类型（由系统分析或原文提供）   | `"Clinical Trial"`, `"Meta-Analysis"`   |

---

## 4. `ppt_push_records` - PPT推送记录表

记录了系统自动或手动推送PPT报告的历史。

| 字段名         | 数据类型 | 描述                               | 示例                                      |
| -------------- | -------- | ---------------------------------- | ----------------------------------------- |
| `id`           | Integer  | 主键，唯一标识符                   | `301`                                     |
| `push_time`    | DateTime | 推送操作发生的时间                 | `"2025-08-12 09:10:00"`                   |
| `topic_name`   | String   | 关联的主题名称                     | `"糖尿病最新研究"`                        |
| `ppt_filename` | String   | 推送的PPT文件名                    | `"Diabetes_Report_2025-08-12.pptx"`       |
| `recipients`   | JSON     | 接收人列表（如邮箱地址）           | `["manager@example.com"]`                 |
| `channel`      | String   | 推送使用的渠道                     | `"Email"`                                 |
| `status`       | String   | 推送任务的状态                     | `"success"`, `"failed"`, `"pending"`    |



## 5. `ppt_diffs` - PPT版本差异记录表

记录同一主题PPT推送记录之间的差异内容摘要。

| 字段名                  | 数据类型     | 描述                | 示例                      |
| -------------------- | -------- | ----------------- | ----------------------- |
| `id`                 | Integer  | 主键，唯一标识符          | `401`                   |
| `current_record_id`  | Integer  | 外键，指向最新的PPT推送记录ID | `305`                   |
| `previous_record_id` | Integer  | 外键，指向前一个PPT推送记录ID | `304`                   |
| `summary`            | Text     | 差异摘要内容            | `"新增了2条临床试验数据"`         |
| `created_at`         | DateTime | 记录创建时间            | `"2025-08-12 09:15:00"` |

---
