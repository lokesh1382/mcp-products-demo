# 🛒 MCP Products Server

A hands-on Python project demonstrating **Model Context Protocol (MCP)** by building a product management server that integrates with Claude Desktop and GitHub Copilot.



## 🗂️ Project Structure

```
create_new_mcp/
│
├── mcp_server.py        # MCP Server with tools, resource, and prompt template
├── add_product.py       # DB logic to INSERT a product
├── fetch_products.py    # DB logic to SELECT all products
├── db_connect.py        # Database connection helper
├── .env                 # API keys and DB credentials (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ MCP Server — `mcp_server.py`



## 🔌 Configuration

### Claude Desktop
Update `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "products": {
      "command": "uv.exe",
      "args": [
        "--directory", "C:\\path\\to\\create_new_mcp",
        "run", "mcp_server.py"
      ]
    }
  }
}
```

### GitHub Copilot
Update `mcp.json` with the same server details.


## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `uv` package manager
- MySQL database
- Claude Desktop or GitHub Copilot


## 📚 Key Learnings

- ✅ MCP Tools are invoked directly by the LLM
- ✅ MCP Resources are fetched manually via host UI and injected into context
- ✅ Prompt Templates enable consistent prompt generation via `/` command
- ⚠️ MCP Sampling (server → LLM callback) is **not yet supported** by Claude Desktop or GitHub Copilot in practice
- 💡 Workaround for sampling: call Anthropic API directly from the MCP server



