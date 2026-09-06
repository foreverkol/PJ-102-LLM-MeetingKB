#!/usr/bin/env node
/**
 * pj102-obsidian-export - Node.js wrapper for PJ-102 atomicstrata → Obsidian exporter
 *
 * 王老师 2026-09-06 Sprint 22 L4.3b:
 *   把 obsidian_export.py(已支持环境变量)封装为可独立 npm install 调用的命令。
 *   使用 child_process 调 Python,不引入新概念。
 *
 * 用法:
 *   npx pj102-obsidian-export                 # 默认(读当前目录的 ../02-设计/atomicstrata-profile.json)
 *   npx pj102-obsidian-export --help
 *   npx pj102-obsidian-export --version
 *   pj102-obsidian-export --schema <path> --wiki <path>
 *
 * 环境变量(覆盖默认值):
 *   PJ102_WIKI_BASE - Wiki 根目录
 *   PJ102_SCHEMA_PATH - atomicstrata profile JSON 路径
 */

const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// 默认路径(PJ-102 项目标准布局)
const DEFAULT_PROJECT_ROOT = path.resolve(__dirname, '..', '..', '..');
const DEFAULT_WIKI_BASE = path.join('/mnt/d/BaiduSyncdisk/hermes/02-知识库/PJ-102-LLM-MeetingKB');
const DEFAULT_SCHEMA_PATH = path.join(DEFAULT_PROJECT_ROOT, '02-设计/atomicstrata-profile.json');
const PYTHON_SCRIPT = path.join(DEFAULT_PROJECT_ROOT, '03-执行/code/obsidian_export.py');

function parseArgs(argv) {
  const args = {
    help: false,
    version: false,
    schema: process.env.PJ102_SCHEMA_PATH || DEFAULT_SCHEMA_PATH,
    wiki: process.env.PJ102_WIKI_BASE || DEFAULT_WIKI_BASE,
    verbose: false,
    type: 'all',
  };
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    switch (arg) {
      case '--help':
      case '-h':
        args.help = true;
        break;
      case '--version':
      case '-v':
        args.version = true;
        break;
      case '--schema':
      case '-s':
        args.schema = argv[++i];
        break;
      case '--wiki':
      case '-w':
        args.wiki = argv[++i];
        break;
      case '--type':
      case '-t':
        args.type = argv[++i];
        break;
      case '--verbose':
        args.verbose = true;
        break;
      default:
        console.error(`未知参数: ${arg}`);
        process.exit(1);
    }
  }
  return args;
}

function showHelp() {
  console.log(`
pj102-obsidian-export v0.1.0-alpha1

PJ-102 atomicstrata → Obsidian Bases/CLAUDE.md 自动生成器(Node.js wrapper)。

用法:
  pj102-obsidian-export [options]

选项:
  -h, --help       显示此帮助
  -v, --version    显示版本
  -s, --schema <path>  atomicstrata profile JSON 路径
                       (默认: env PJ102_SCHEMA_PATH 或 02-设计/atomicstrata-profile.json)
  -w, --wiki <path>    Wiki 根目录
                       (默认: env PJ102_WIKI_BASE 或 02-知识库/PJ-102-LLM-MeetingKB)
  -t, --type <type>    仅生成指定类型 (meetings/persons/concepts/judgments/all)
                       (默认: all)
  --verbose         显示详细输出

环境变量:
  PJ102_WIKI_BASE      Wiki 根目录覆盖
  PJ102_SCHEMA_PATH    Profile JSON 路径覆盖

示例:
  pj102-obsidian-export
  pj102-obsidian-export --type meetings --verbose
  PJ102_WIKI_BASE=/tmp/wiki pj102-obsidian-export

更多信息: https://github.com/foreverkol/PJ-102-LLM-MeetingKB
`);
}

function run(args) {
  // 检查 Python 脚本存在
  if (!fs.existsSync(PYTHON_SCRIPT)) {
    console.error(`❌ Python 脚本不存在: ${PYTHON_SCRIPT}`);
    process.exit(1);
  }
  // 检查 schema 存在
  if (!fs.existsSync(args.schema)) {
    console.error(`❌ Schema 不存在: ${args.schema}`);
    process.exit(1);
  }
  // 检查 wiki 存在
  if (!fs.existsSync(args.wiki)) {
    console.error(`❌ Wiki 目录不存在: ${args.wiki}`);
    process.exit(1);
  }

  console.log(`pj102-obsidian-export v0.1.0-alpha1`);
  console.log(`  Schema: ${args.schema}`);
  console.log(`  Wiki: ${args.wiki}`);
  console.log(`  Type: ${args.type}`);
  console.log();

  // 调 Python 脚本
  try {
    const env = {
      ...process.env,
      PJ102_WIKI_BASE: args.wiki,
      PJ102_SCHEMA_PATH: args.schema,
    };
    const result = execFileSync(
      'python3',
      [PYTHON_SCRIPT, '--type', args.type],
      { env, encoding: 'utf-8', stdio: 'inherit' }
    );
    console.log(`\n✅ 生成完成`);
  } catch (err) {
    console.error(`❌ 执行失败: ${err.message}`);
    process.exit(1);
  }
}

// 主入口
const args = parseArgs(process.argv);
if (args.help) {
  showHelp();
  process.exit(0);
} else if (args.version) {
  console.log('pj102-obsidian-export v0.1.0-alpha1');
  process.exit(0);
} else {
  run(args);
}