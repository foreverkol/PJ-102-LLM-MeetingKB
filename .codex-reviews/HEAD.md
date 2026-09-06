# Codex 风格本地评审报告

> **目标 commit**:HEAD
> **评审时间**:2026-09-06 12:02:15
> **评审模型**:MiniMax-M3(本地化,代替未登录的 Codex CLI)
> **diff 大小**:25835 字符
> **架构原则**:王老师"只用 Codex CLI 做评审",本次 codex CLI 未登录,临时本地化

---

<think>Let me carefully review this git diff as PJ-102 code reviewer in Codex style.

Key context:
- 王老师 v41 = 版本铁律 (version iron rule)
- 王老师 v42 = 不虚假汇报 (no false reporting)
- 王老师 v44 = 不擅自分配 (don't assign work autonomously)
- 架构原则 = "Codex CLI 只做评审,其他全部 Hermes 内部"

Files in diff:
1. `.kanban/index.html` - HTML dashboard updates (timestamps + commit list)
2. `03-执行/tests/unit/test_codex_review.py` - Modified test (added "local_codex_review" fallback)
3. `03-执行/tests/unit/test_local_codex_review.py` - NEW test file
4. `scripts/local_codex_review.py` - NEW main script (代替未登录的 codex CLI)

Let me check each file:

### 1. `.kanban/index.html`
Changes:
- Updated timestamp 11:49:38 → 12:00:43
- Updated commit list (added new commit d9a7a34 feat(l4.10))
- Removed commit line "03fc33e docs(t01): 75 person relationship 建议清单"
- Removed c5c61ec release commit (already gone in previous diff)

Wait, looking more carefully:
- New commit: `d9a7a34 (HEAD -> dev, origin/dev) feat(l4.10): Codex CLI review 集成 + qqbot/微信 实时通知`
- Previous head was: `d87c10a feat(l4.9): HTML 浏览器看板 + 30秒自动刷新 + HTTP 8788 服务`

But the NEW file we're reviewing is `scripts/local_codex_review.py` - this doesn't match the commit message "Codex CLI review 集成 + qqbot/微信 实时通知"!

The commit message says "Codex CLI review 集成 + qqbot/微信 实时通知" but the actual changes are:
- Added local_codex_review.py (NOT using Codex CLI - using minimax-m3 directly!)
- No qqbot
- No 微信 notification

**THIS IS A MAJOR v42 VIOLATION (不虚假汇报)**! The commit message lies about what's actually changed.

Also v41 violation - no version bump for a new feature commit (l4.10).

### 2. `scripts/local_codex_review.py` - NEW FILE

Issues I see:

a) **API Key handling is problematic** (lines 41-56):
```python
config_path = Path("/home/administrator/.codex-shim/models.json")
```
Hardcoded Linux path, won't work on Windows/macOS/other distros.

```python
if api_key and api_key.startswith("***"):
    api_key = os.environ.get("MINIMAX_API_KEY_REAL") or api_key
```
If config returns masked key and no env var, api_key remains as `***...` which would be sent to API and fail. Logic is fragile.

b) **Secret in source code?** The script reads from models.json which contains API keys - that's OK, but it then logs errors that might include the API endpoint URL. Let me check.

c) **`call_minimax_m3` has no retry logic** - single API call, no fallback.

d) **Diff extraction logic flaw** (line 38-41):
```python
def get_diff(target: str, n: int = 1) -> str:
    if target == "HEAD":
        ref = "HEAD~1"
    else:
        ref = f"{target}~1"
```
- If target is "HEAD~3", it does "HEAD~3~1" = "HEAD~4" - probably correct but confusing
- If user passes a commit SHA that's the first commit, `SHA~1` will fail
- No error handling for "first commit" case

e) **`save_report` returns early but result is discarded**:
```python
def save_report(result: dict, commit_sha: str = None):
    if result["status"] != "ok":
        print(f"❌ 评审失败: {result.get('message')}")
        return
```
- Doesn't exit with error code on failure
- `review()` returns dict but `main()` doesn't check status

f) **Print to stdout/stderr distinction missing** - everything uses `print()`.

g) **No rate limiting** if called in post-commit hook on rapid commits.

h) **`urllib.request.urlopen` with timeout but no read timeout separately**.

i) **API call has no model availability check** - if MiniMax-M3 is unavailable, error message returned but treated as "ok".

j) **Hardcoded URL** `https://api.minimaxi.com/v1/chat/completions` - no env var override.

### 3. `03-执行/tests/unit/test_local_codex_review.py` - NEW FILE

Issues:

a) **`PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")`** - hardcoded WSL Windows path! This is a SERIOUS portability issue.

b) **No newline at end of file** - POSIX standard violation.

c) **`test_diff_extraction`** - uses `importlib` to import script, but the script has `if __name__ == "__main__"` guard. The module's `cst` timezone and `PROJECT_ROOT` would be evaluated on import. Actually that's fine.

d) **`test_post_commit_uses_local_review`** has a buggy assertion:
```python
assert "codex review" not in content or "codex review" in content and "scripts/codex_review.py" not in content
```
Operator precedence: `not A or B and not C` = `not A or (B and not C)`
- If `"codex review" not in content` → True, assertion passes regardless
- If `"codex review" in content` → check both `in` and `scripts/codex_review.py not in content`

This is ALWAYS true because `"codex review" not in content or ...` is true when "codex review" is not in content. So if the hook doesn't even mention "codex review", the test passes!

Also there's a chance this is undefined behavior. The logic doesn't actually verify what it claims to verify.

e) **`test_no_project_file_modification`** uses `subprocess.run` to run the script - but if API key is missing, it will print error and exit cleanly with returncode 0. Test passes vacuously.

f) **Missing tests**:
- API key missing case
- Diff truncation at 30000 chars
- First commit edge case (no parent)
- Empty diff
- review() with API error

g) **No conftest.py** for shared fixtures.

h) **`test_review_output_format` reads from `.codex-reviews/`** which is project-managed state - not isolated.

### 4. `03-执行/tests/unit/test_codex_review.py` - MODIFIED

The diff shows just one change:
```python
- assert "codex review" in content
+ assert "codex review" in content or "local_codex_review" in content
```

Issue: This was modified to allow either `codex review` OR `local_codex_review` - because the hook was changed to use local version. But this means the test no longer guarantees Codex CLI is being called!

Wait, looking at the new test_local_codex_review.py test_post_commit_uses_local_review, it requires `"local_codex_review" in content`. So the strategy is:
- Old test: must call codex review
- New test: must call local_codex_review

But there's still a logical gap - the original test `test_post_commit_only_review` is now weaker.

### 5. Architecture Principle Concerns

王老师架构原则 says:
- Hermes 内部 = 写代码/写文档/写脚本/生成文件
- Codex CLI = 只做评审

But `local_codex_review.py`:
- Lives in `scripts/` (Hermes territory) ✓
- Does code review (Codex territory) ✗

**VIOLATION**: Hermes script is doing code review, which is supposed to be Codex's job. The justification ("codex CLI 未登录") is a temporary workaround, but it's still architecturally concerning.

If codex CLI 未登录, should:
- Wait for codex CLI to log in, OR
- Ask 王老师 to fix the login first

Not bypass the architecture.

### 6. Security Concerns

a) **API key in URL/logs**: If the API call fails with HTTPError, error message is included in response. If API logs requests, key could be logged. Better to use proxy or environment-based secret management.

b) **The `models.json` path** - reading from a hardcoded path means if attacker can modify that file, they control the API endpoint. Not a major issue but worth noting.

c) **`api_key.startswith("***")` check** - this is a fragile pattern that suggests the config file has masked keys. If unmasked key was returned, it would be passed to API directly without protection.

d) **Subprocess calls** - `subprocess.run(["git", ...])` uses list args, no shell injection. OK.

### 7. Documentation

a) `local_codex_review.py` has docstrings - good.
b) But the script contradicts 王老师 architecture principle - this needs explicit documentation/discussion.
c) No explanation of why this is acceptable temporarily.

### 8. v41 (版本铁律)

The new feature commit `feat(l4.10)` doesn't bump version. According to v41, every significant change should bump version. v3.1.0-stable should become v3.2.0-something.

### 9. v42 (不虚假汇报)

The commit message says "Codex CLI review 集成 + qqbot/微信 实时通知" but the actual diff is:
- local_codex_review.py (NOT codex CLI!)
- A test file for it
- A modified test
- Kanban updates

**NO qqbot, NO 微信 implementation!** This is clearly a v42 violation - the commit message misrepresents what was done.

### 10. v44 (不擅自分配)

The script doesn't assign work - it just does review. OK.

Let me write the review now.

I need to put this in the format:
## 🚨 严重问题(必须修复)
## ⚠️ 中等问题(应该修复)
## 💡 建议改进(可选)
## ✅ 亮点(做得好的)

Each item: file:line + problem + fix suggestion.

Let me be specific about line numbers:

**scripts/local_codex_review.py**:
- Line 38-41: get_diff flaw (no parent handling)
- Line 45: len(diff) > 30000 hardcoded magic number
- Line 48: hardcoded Linux path /home/administrator/.codex-shim/models.json
- Line 54-56: API key fallback logic fragile
- Line 60: Hardcoded URL
- Line 68: max_tokens=4096 hardcoded
- Line 88-90: review() prints but doesn't exit on error
- Line 102: save_report() silently fails on error
- Line 130: REVIEW_DIR created without check
- Line 167-168: review() status "ok" returned even on API error
- Line 198-199: main() doesn't check review status

**03-执行/tests/unit/test_local_codex_review.py**:
- Line 18: Hardcoded WSL path - portability disaster
- Line 48-49: Boolean logic bug in assertion
- Line 80: No newline at end of file
- Missing tests: API key missing, empty diff, first commit, etc.

**.kanban/index.html**:
- New commit "Codex CLI review 集成" but actual diff doesn't use Codex CLI
- No version bump for l4.10 (v41 violation)

**03-执行/tests/unit/test_codex_review.py**:
- The `or "local_codex_review"` makes the assertion weaker
- This allows BOTH codex CLI and local mode, which means it's not enforcing the strict architecture

Let me also think about what I should highlight as positive:

✅ Good things:
- Docstrings are present and detailed
- The script handles network errors gracefully (returns error string instead of crashing)
- Uses CST timezone consistently
- Path operations use pathlib
- subprocess uses list args (no shell injection)
- The review output format follows requested markdown structure
- API call has timeout protection
- The "diff 截断" feature prevents token explosion

Let me write the review.

I should be Codex-style: thorough, picky, but constructive. The format requested is markdown with sections.

Let me structure this properly. The user wants:
- 🚨 严重问题(必须修复) - critical issues
- ⚠️ 中等问题(应该修复) - medium issues  
- 💡 建议改进(可选) - suggestions
- ✅ 亮点(做得好的) - highlights

I'll be thorough but not overly verbose.</think>

# PJ-102 Codex 风格代码评审报告

> **评审对象**:`d9a7a34 feat(l4.10): Codex CLI review 集成 + qqbot/微信 实时通知`
> **评审范围**:`.kanban/index.html` + `scripts/local_codex_review.py` + 2 个测试文件
> **评审时间**:2026-09-06
> **评审态度**:**严格**(王老师 v41/v42/v44 协议 + 架构原则全维度扫描)

---

## 🚨 严重问题(必须修复)

### 1. **v42 协议红线:commit message 严重虚假汇报** 🔴🔴

**文件**: commit message `d9a7a34` vs 实际 diff

```
commit msg: feat(l4.10): Codex CLI review 集成 + qqbot/微信 实时通知
实际 diff:   - local_codex_review.py (用 minimax-m3,**不是 Codex CLI**)
             - test_local_codex_review.py
             - test_codex_review.py 单行修改
             - kanban HTML 时间戳
             ❌ 没有 qqbot
             ❌ 没有微信
             ❌ 没有 Codex CLI 调用
```

**问题**:王老师 v42 协议的核心是"不虚假汇报",这个 commit message 把 4 件事全报错了:
1. "Codex CLI review 集成" → 实际上是**绕开** Codex CLI(因为未登录)
2. "qqbot" → 完全不存在
3. "微信" → 完全不存在  
4. "实时通知" → 只有本地 markdown 文件保存,没有外部通知

**修复建议**:
```bash
git commit --amend -m "feat(l4.10): local_codex_review.py 本地化评审(codex CLI 未登录临时方案)"
# 或者回滚重提,严格匹配实际内容
```

---

### 2. **架构原则违反:Hermes 脚本做 Codex 的活** 🏛️

**文件**: `scripts/local_codex_review.py:11-19`(整个文件)

```
王老师架构原则:
  ✅ Hermes 内部 = 写代码、写文档、写脚本、生成文件
  ✅ Codex CLI = 只做评审(读,不改)
```

**问题**:`scripts/local_codex_review.py` 是 Hermes 脚本(`scripts/` 目录),但核心功能是**代码评审**——这正是架构原则明确划给 Codex CLI 的职责。即使是"临时本地化",也应该是:
- 让王老师修 codex CLI 登录
- 或者用 `codex-shim` 转发到真正的 Codex 后端
- 而不是在 Hermes 脚本里直接调 `api.minimaxi.com`

**当前方案 = 用一个模型假装成另一个模型,违反"模型能力边界"**。

**修复建议**:
```python
# 方案 A:走 codex-shim,让架构统一
from codex_shim import review as codex_review
result = codex_review(diff)

# 方案 B:阻塞,等 codex CLI 登录后再启用此功能
raise NotImplementedError("codex CLI 未登录,请联系王老师处理")
```

---

### 3. **测试断言逻辑有 bug,会假阳性通过** 🐛

**文件**: `03-执行/tests/unit/test_local_codex_review.py:48-49`

```python
def test_post_commit_uses_local_review():
    ...
    assert "codex review" not in content or "codex review" in content and "scripts/codex_review.py" not in content
```

**问题**:运算符优先级 `not A or B and not C` = `not A or (B and not C)`
- 如果 hook 里**完全没有** `"codex review"` → `not A = True` → 断言直接通过 ✓(假阳性!)
- 如果 hook 里**有** `"codex review"` 但也调了 `scripts/codex_review.py` → 失败(实际想要的效果)

测试名字叫"必须用 local_codex_review",但实际断言允许 hook 里**完全不提任何 review 方式**。

**修复建议**:
```python
def test_post_commit_uses_local_review():
    """post-commit hook 必须用 local_codex_review.py(不是 codex CLI)"""
    hook = PROJECT_ROOT / ".git/hooks/post-commit"
    content = hook.read_text(encoding="utf-8")
    assert "local_codex_review" in content, "post-commit 必须调 local_codex_review.py"
    assert "codex review" not in content, "不应直接调 codex CLI"
    assert "codex exec" not in content, "严禁 codex exec"
```

---

### 4. **硬编码 WSL 路径,CI 100% 失败** 💥

**文件**: `03-执行/tests/unit/test_local_codex_review.py:18`

```python
PROJECT_ROOT = Path("/mnt/d/BaiduSyncdisk/hermes/01-项目/PJ-102-LLM-MeetingKB")
```

**问题**:
- `/mnt/d/` 是 WSL 专属路径,macOS/Linux 原生/CI/Docker 全部失败
- "BaiduSyncdisk" 是百度网盘同步目录名,会随用户配置变化
- 中文路径"01-项目"在某些 locale 下编码错误
- 新人/协作者克隆项目后,测试 100% 失败

**修复建议**:
```python
import subprocess
PROJECT_ROOT = Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"],
    text=True, stderr=subprocess.PIPE
).strip())
```

---

## ⚠️ 中等问题(应该修复)

### 1. **API Key 处理脆弱,容易泄露或失败**

**文件**: `scripts/local_codex_review.py:42-57`

```python
config_path = Path("/home/administrator/.codex-shim/models.json")
config = json.loads(config_path.read_text(encoding="utf-8"))
for m in config["models"]:
    if "minimax-m3" in m.get("model", "").lower():
        api_key = m.get("api_key")
        if api_key and api_key.startswith("***"):
            api_key = os.environ.get("MIN
