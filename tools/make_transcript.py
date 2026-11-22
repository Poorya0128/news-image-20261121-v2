#!/usr/bin/env python3
"""Turns the raw Kiro session log into a readable Markdown transcript.

Keeps every user prompt, assistant message, reasoning note and tool call, but
drops the base64 image blobs (screenshots the agent viewed) so the file is small
and human-readable. The untouched raw log ships beside it as transcript.raw.jsonl.gz.
"""
import json
import os
import re
import sys

SRC = sys.argv[1]
OUT = sys.argv[2]


def clean(text):
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)
    # strip data URIs / long base64 runs
    text = re.sub(r"data:image/[^;]+;base64,[A-Za-z0-9+/=]+", "[image]", text)
    text = re.sub(r"[A-Za-z0-9+/]{400,}={0,2}", "[binary omitted]", text)
    return text.strip()


out = ["# Agent transcript — The One-Day World (news-image-20261121)",
       "",
       "Built with Kiro in Vibe mode. This is the readable transcript; the full raw log is `transcript.raw.jsonl.gz`.",
       "Base64 screenshots the agent viewed have been replaced with `[image]` for size; all text, reasoning and tool calls are intact.",
       ""]
n_user = n_asst = n_tool = 0
for ln in open(SRC, encoding="utf-8"):
    ln = ln.strip()
    if not ln:
        continue
    try:
        o = json.loads(ln)
    except Exception:
        continue
    p = o.get("payload", {})
    t = p.get("type")
    ts = (o.get("timestamp") or "")[:19].replace("T", " ")
    if t == "user":
        c = clean(p.get("content", ""))
        if not c:
            continue
        n_user += 1
        out += [f"\n## 🧑 User · {ts}", "", c, ""]
    elif t == "assistant":
        c = clean(p.get("content", ""))
        if not c:
            continue
        op = p.get("operationType", "")
        if op == "Reasoning":
            n_asst += 1
            out += [f"\n### 💭 Kiro (thinking) · {ts}", "", "> " + c.replace("\n", "\n> "), ""]
        else:
            n_asst += 1
            out += [f"\n## 🤖 Kiro · {ts}", "", c, ""]
    elif t == "tool_call":
        name = p.get("toolName", "tool")
        args = p.get("args", {})
        args = {k: v for k, v in args.items() if k != "toolName"}
        a = clean(json.dumps(args, ensure_ascii=False))
        if len(a) > 600:
            a = a[:600] + " …"
        n_tool += 1
        out += [f"\n<details><summary>🔧 {name} · {ts}</summary>", "", "```json", a, "```", "</details>", ""]

out[4:4] = [f"**{n_user} user prompts · {n_asst} assistant messages · {n_tool} tool calls.**", ""]
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print("wrote", OUT, os.path.getsize(OUT), "bytes;", n_user, "prompts,", n_asst, "msgs,", n_tool, "tools")
