# PJ-102-LLM-MeetingKB Makefile
# 王老师 9-06 B6 修复:框架集成 + install-hooks

.PHONY: help install-hooks uninstall-hooks test lint status clean all

help:
	@echo "PJ-102-LLM-MeetingKB v3.1.0-rc1 Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install-hooks   - 安装 pre-commit hook"
	@echo "  make uninstall-hooks - 卸载 pre-commit hook"
	@echo "  make test            - 跑所有单元测试"
	@echo "  make lint            - 跑 wiki lint"
	@echo "  make status          - 项目状态"
	@echo "  make clean           - 清理 Python cache"

install-hooks:
	@echo "[INSTALL] pre-commit hook"
	@cp scripts/pre-commit-hooks/check-version-consistency.sh .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "[OK] pre-commit hook 已激活"

uninstall-hooks:
	@echo "[UNINSTALL] pre-commit hook"
	@rm -f .git/hooks/pre-commit
	@echo "[OK] pre-commit hook 已卸载"

test:
	@echo "[TEST] 跑所有单元测试"
	@cd $(CURDIR) && python3 -m pytest 03-执行/tests/unit/ -v

lint:
	@echo "[LINT] 跑 wiki lint"
	@cd $(CURDIR)/03-执行/code && python3 lint_wiki.py

status:
	@echo "[STATUS] 项目状态"
	@cd $(CURDIR)/03-执行/code && python3 pj102.py status

clean:
	@echo "[CLEAN] 清理 Python cache"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "[OK] 清理完成"

all: install-hooks test
	@echo "[ALL] install-hooks + test 完成"
