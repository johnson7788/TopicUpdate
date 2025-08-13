# 生成PPT的结果

import uuid
import httpx
import asyncio
import os
import json
from pathlib import Path
from a2a.client import A2AClient
from a2a.types import MessageSendParams, SendStreamingMessageRequest

# -------- 配置部分 --------
OUTLINE_AGENT_URL = "http://localhost:10001"  # 生成大纲
PPT_AGENT_URL = "http://localhost:10011"      # 生成 PPT 内容
TIMEOUT = 60.0

async def run_agent(prompt, agent_url, metadata=None, collect_text=False):
    """通用调用 A2A Agent 的异步函数"""
    async with httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT)) as httpx_client:
        client = await A2AClient.get_client_from_agent_card_url(httpx_client, agent_url)
        request_id = uuid.uuid4().hex

        send_message_payload = {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": prompt}],
                "messageId": request_id,
            }
        }
        if metadata:
            send_message_payload["message"]["metadata"] = metadata

        streaming_request = SendStreamingMessageRequest(
            id=request_id,
            params=MessageSendParams(**send_message_payload)
        )

        stream_response = client.send_message_streaming(streaming_request)

        collected_chunks = []
        async for chunk in stream_response:
            chunk_data = chunk.model_dump(mode="json")
            result = chunk_data.get("result", {})
            artifact = result.get("artifact")
            if artifact:
                parts = artifact.get("parts", [])
                for part in parts:
                    if part.get("kind") == "text":
                        text_content = part.get("text", "")
                        collected_chunks.append(text_content)
                        if collect_text:
                            print(text_content)
            else:
                status_message = result.get("status", {}).get("message", {})
                parts = status_message.get("parts", [])
                for part in parts:
                    if part.get("kind") == "text":
                        collected_chunks.append(part.get("text", ""))

        return "\n".join(collected_chunks)


async def main(topic):
    # Step 1: 调用第一个 Agent 生成大纲
    print("\n=== Step 1: 生成大纲 ===")
    outline_metadata = {
        "language": "Chinese",
        "select_time": [{"sTimeYear": 2011, "eTimeYear": 2025}]
    }
    outline_text = await run_agent(topic, OUTLINE_AGENT_URL, metadata=outline_metadata, collect_text=True)

    # Step 2: 调用第二个 Agent 生成 PPT 内容
    print("\n=== Step 2: 根据大纲生成 PPT 内容 ===")
    ppt_metadata = {"numSlides": 12}
    ppt_content = await run_agent(outline_text, PPT_AGENT_URL, metadata=ppt_metadata, collect_text=True)

    # Step 3: 保存结果
    if os.environ.get("USER") == "admin":
        output_file = "/Users/admin/Downloads/output.md"
    else:
        output_file = "E:/Downloads/output.md"

    Path(output_file).write_text(ppt_content, encoding="utf-8")
    print(f"\n✅ 已保存到 {output_file}")


if __name__ == "__main__":
    topic = """PDL1-41BB双抗在肺癌治疗领域的临床研究进展"""
    asyncio.run(main(topic))
