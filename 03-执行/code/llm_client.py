"""
LLM 客户端 - PJ-102-LLM-MeetingKB v1.0

支持的 provider（按优先级）：
1. MiniMax M3（中国区，api.minimaxi.com）- 默认
2. DeepSeek
3. OpenAI
4. Anthropic
5. Mock（测试用）

修复：
- MiniMax 中国区 base_url 是 https://api.minimaxi.com/v1（不是 api.minimax.chat）
- 端点路径不含 /v1 前缀（base_url 已含）
"""

import json
import os
import re
import time
import urllib.error
import urllib.request
from typing import Optional


class LLMClient:
    """统一的 LLM 客户端"""

    def __init__(self, provider: str = "auto"):
        self.deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self.minimax_key = os.environ.get("MINIMAX_API_KEY", "")
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")

        # 默认用 MiniMax M3（王老师指定）
        if provider == "auto":
            if self.minimax_key:
                provider = "minimax"
            elif self.deepseek_key:
                provider = "deepseek"
            elif self.openai_key:
                provider = "openai"
            elif self.anthropic_key:
                provider = "anthropic"
            else:
                provider = "mock"

        self.provider = provider
        self.models = {
            "minimax": "MiniMax-M3",   # v3.0 修正:王老师指定 MiniMax-M3,不是 MiniMax-Text-01
            "deepseek": "deepseek-chat",
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-haiku-20240307",
            "mock": "mock",
        }
        self.model = self.models.get(provider, "mock")

    def call(self, prompt: str, system: str = "", max_tokens: int = 2000, max_retries: int = 3) -> str:
        """调用 LLM（带重试）"""
        for attempt in range(max_retries):
            try:
                if self.provider == "minimax":
                    return self._call_minimax(prompt, system, max_tokens)
                elif self.provider == "deepseek":
                    return self._call_deepseek(prompt, system, max_tokens)
                elif self.provider == "openai":
                    return self._call_openai(prompt, system, max_tokens)
                elif self.provider == "anthropic":
                    return self._call_anthropic(prompt, system, max_tokens)
                else:
                    return self._mock_response()
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"⚠️  限流，等待 {wait}s 后重试...")
                    time.sleep(wait)
                else:
                    print(f"⚠️  LLM 调用失败 (HTTP {e.code}): {e}")
                    return ""
            except Exception as e:
                print(f"⚠️  LLM 调用异常: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return ""
        return ""

    def _call_minimax(self, prompt: str, system: str, max_tokens: int) -> str:
        """MiniMax M3 真实调用（中国区）"""
        base_url = os.environ.get("MINIMAX_CN_BASE_URL", "https://api.minimax.chat")
        base_url = base_url.rstrip("/")
        if not base_url.endswith("/v1"):
            base_url = base_url + "/v1"
        url = f"{base_url}/text/chatcompletion_v2"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system or "你是一个专业的中文会议纪要分析师。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.minimax_key}"
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # v3.0 S9: debug print
            if os.environ.get("DEBUG_LLM"):
                print(f"[DEBUG LLM] status=200, raw_data_keys={list(data.keys())}")
                if "choices" in data and data["choices"]:
                    content = data["choices"][0].get("message", {}).get("content", "")
                    print(f"[DEBUG LLM] content_len={len(content)}, preview={content[:200]!r}")
                    if not content:
                        print(f"[DEBUG LLM] full_response={json.dumps(data, ensure_ascii=False)[:1000]}")
            # v3.0 S9: MiniMax-M3 走 thinking, content 可能为空或被截断
            # 优先 content,fallback reasoning_content
            msg = data["choices"][0].get("message", {})
            content = msg.get("content", "") or msg.get("reasoning_content", "")
            return content

    def _call_deepseek(self, prompt: str, system: str, max_tokens: int) -> str:
        """DeepSeek 调用"""
        url = "https://api.deepseek.com/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system or "你是一个专业的中文会议纪要分析师。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.deepseek_key}"
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def _call_openai(self, prompt: str, system: str, max_tokens: int) -> str:
        """OpenAI 调用"""
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system or "你是一个专业的中文会议纪要分析师。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_key}"
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def _call_anthropic(self, prompt: str, system: str, max_tokens: int) -> str:
        """Anthropic 调用"""
        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system or "你是一个专业的中文会议纪要分析师。",
            "messages": [{"role": "user", "content": prompt}],
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.anthropic_key,
                "anthropic-version": "2023-06-01"
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["content"][0]["text"]

    def _mock_response(self) -> str:
        """Mock 响应（无 LLM key 时）"""
        return '{"mock": true}'


def safe_json_parse(content: str, default=None) -> dict:
    """安全解析 JSON(处理 markdown 包裹、尾随逗号等)

    支持返回 dict 或 list(default 可为同类型)
    """
    if not content:
        return default if default is not None else {}
    content = content.strip()

    # 移除 markdown 围栏
    content = re.sub(r"^```(?:json)?\s?", "", content)
    content = re.sub(r"\s?```$", "", content)

    # 尝试解析(优先整个 content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 提取 JSON 块(dict 或 list)
    for pattern in [r"\{[\s\S]*\}", r"\[[\s\S]*\]"]:
        m = re.search(pattern, content)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                continue

    # 修复尾随逗号重试
    for pattern in [r"\{[\s\S]*\}", r"\[[\s\S]*\]"]:
        m = re.search(pattern, content)
        if m:
            try:
                fixed = re.sub(r",\s*}", "}", m.group(0))
                fixed = re.sub(r",\s*]", "]", fixed)
                return json.loads(fixed)
            except json.JSONDecodeError:
                continue

    return default if default is not None else {}