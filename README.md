# 🐆 jaguar — MongoDB Log Analysis Toolkit

🔍 Making parsing of `mongodb.log` files simpler using a standard Linux pipeline.

All tools accept piped stdin and are registered as shell aliases via `alias.fish` or `alias.bash`.

---

## ⚡ Quick Start

```bash
# 1. Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and enter the project
git clone https://github.com/Dennis-Spera/jaguar
cd jaguar

# 3. Create and activate venv
uv venv .venv
source .venv/bin/activate.fish #fish
or 
source .venv/bin/activate #bash

# 4. Install dependencies
uv add commandlines>=0.4.1 tabulate>=0.10.0

# 5. Register aliases
source alias.fish
or
source alias.bash

# 6. Try it out
cat mongodb.log | millis -ge 100 | phead -r 10
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install `uv` (if needed)

`uv` is a fast Python package installer. Check if it's installed:

```bash
uv --version
```

If not installed, install it:

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or use your system package manager (Homebrew, apt, etc.).

---

### 2️⃣ Create a Virtual Environment

From the project root, create a Python virtual environment:

```bash
uv venv .venv
```

Activate it in your shell:

**Fish:**
```fish
source .venv/bin/activate.fish
```

**Bash / Zsh:**
```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

The project dependencies are defined in `pyproject.toml`:
- **`commandlines`** ≥ 0.4.1 — command-line argument parsing
- **`tabulate`** ≥ 0.10.0 — formatted table output

Install them with `uv`:

```bash
uv add commandlines>=0.4.1 tabulate>=0.10.0
```

Or install directly from `pyproject.toml`:

```bash
uv pip install --no-build-isolation .
```

Alternative — install specific packages:

```bash
uv pip install commandlines tabulate
```

---

### 4️⃣ Register Aliases

Source the alias file to register all tools:

```fish
source alias.fish        # register all aliases in the current fish session
```

`alias.fish` sets two variables you can override before sourcing:

| Variable | Default | Purpose |
|---|---|---|
| `PYTHON_BIN` | `python` | Path to Python executable |
| `SCRIPTS_DIR` | `$PWD` | Directory containing the scripts |

**Example — use a specific Python:**
```fish
set -g PYTHON_BIN /home/user/.venv/bin/python
source alias.fish
```

---

## 🛠️ Tools

### 📛 `appName` → `appName.py`
Extract and total application names from `mongod.log` on stdin.
Includes both user and system application names.

```
cat mongodb.log | appName
```

---

### 💾 `bytesRead` → `bytesRead.py`
Sort entries by `bytesRead` from highest to lowest.

```
cat mongodb.log | bytesRead
```

---

### 🔎 `collScans` → `collScans.py`
List collection scans (`COLLSCAN`) grouped by namespace.

```
cat mongodb.log | collScans
```

---

### 🎛️ `control` → `controlPrint.py`
Pretty-print `CONTROL` component log entries with structured field extraction.
Handles: Process Details, Build Info, Operating System, Options, Replica Set config,
Log Rotation, Session Cache failures, and a generic fallback for all other CONTROL messages.

```
cat mongodb.log | control
```

---

### ⚡ `cpuc` → `cpuc.py`
Sort entries by `cpuNanos` from highest to lowest.
Optionally filter by context.

```
cat mongodb.log | cpuc -ge <cpuNanos> [-ctx <context>]
```

---

### 🗄️ `cpuPerDatabase` → `cpuPerDatabase.py`
Calculate total CPU cycles spent, aggregated per database.

```
cat mongodb.log | cpuPerDatabase
```

---

### 📄 `docsExamined` → `docsExamined.py`
Sort entries by `docsExamined` from highest to lowest.

```
cat mongodb.log | docsExamined
```

---

### 🚗 `drivers` → `drivers.py`
Extract and total MongoDB driver names from `mongod.log` on stdin.

```
cat mongodb.log | drivers
```

---

### 📋 `formatOne` → `formatOne.py`
Present json in a more readable format from `mongod.log` entries on stdin.

```
cat mongodb.log | formatOne
```

---

### 🕐 `jsonFetcher` → `jsonFetcher.py`
Filter log entries by a datetime range. Useful for pre-filtering before piping into other tools.

```
cat mongodb.log | jsonFetcher -b <start> -e <end> | millis
```

Example — fetch records from March 25, 2025 between 1:50 p.m. and 2:50 p.m.:

```
cat mongodb.log | jsonFetcher -b 20250325135000 -e 20250325145000
```

---

### 🔑 `keysExamined` → `keysExamined.py`
Sort entries by `keysExamined` from highest to lowest.

```
cat mongodb.log | keysExamined
```

---

### ⏱️ `millis` → `millis.py`
Sort entries by `durationMillis` from highest to lowest.
Optionally filter by context or deduplicate by `queryHash`.

```
cat mongodb.log | millis [-ge <ms>] [-ctx <context>] [-u]
```

| Flag | Description |
|---|---|
| `-ge <ms>` | Only show entries ≥ this duration |
| `-ctx <ctx>` | Filter by context (default: all) |
| `-u` | Show only the first occurrence of each unique queryHash |

---

### 🗂️ `ns` → `ns.py`
Sort log entries by namespace.

```
cat mongodb.log | ns
```

---

### 🔢 `nsCount` → `nsCount.py`
Display operation counts grouped by namespace. Supports multiple output formats.

```
cat mongodb.log | nsCount              # tabular (default)
cat mongodb.log | nsCount -o tab
cat mongodb.log | nsCount -o md
cat mongodb.log | nsCount -o csv
```

---

### 👤 `nsCountUser` → `nsCountUser.py`
Display operation counts grouped by namespace and user.

```
cat mongodb.log | nsCountUser              # tabular (default)
cat mongodb.log | nsCountUser -o tab
cat mongodb.log | nsCountUser -o md
cat mongodb.log | nsCountUser -o csv
```

---

### 📇 `nsIndexes` → `nsIndexes.py`
List indexes used, grouped by namespace.

```
cat mongodb.log | nsIndexes
```

---

### 🔝 `phead` → `phead.py`
Emulate the Linux `head` command for piped Python workflows (avoids `SIGTERM` issues).
Default is 6 records; override with `-r <n>`.

```
cat mongodb.log | millis | phead -r 20
```

---

### #️⃣ `queryHash` → `queryHash.py`
Aggregate and count query shapes by `queryHash`.

```
cat mongodb.log | queryHash
```

---

### 🎯 `queryTargetting` → `queryTargetting.py`
Report query targeting ratio — the ratio of documents examined to documents returned.
A ratio significantly above 1.0 indicates poor index selectivity.

```
Targeting Ratio = docsExamined / nreturned
```

| Ratio | Meaning |
|---|---|
| 1.0 | ✅ Perfect — index is highly selective |
| 2–10 | ⚠️ Acceptable for some workloads |
| > 10 | 🚨 Poor targeting — review indexes |

```
cat mongodb.log | queryTargetting
```

---

## 🔧 Typical Workflows

```fish
# Top 10 slowest queries
cat mongodb.log | millis -ge 100 | phead -r 10

# Collection scans with namespace
cat mongodb.log | collScans

# CPU usage by database
cat mongodb.log | cpuPerDatabase

# CONTROL events pretty-printed
cat mongodb.log | control

# Filter a time window then analyse
cat mongodb.log | jsonFetcher -b 20250101000000 -e 20250101010000 | millis

# Query targeting issues
cat mongodb.log | queryTargetting

# Driver breakdown
cat mongodb.log | drivers
```

  ```md
  example: to fetch all the json records from a mongodb.log file from March 25, 20205 at 1:50 p.m. - 2:50 p.m. 
    cat mongodb | jsonFetcher -b 20250325135000 -e 20250325145000
  ```

  > **appName** - 
   selects json based on a begin date and an end date, from all [components](https://www.mongodb.com/docs/manual/reference/log-messages/?msockid=3e74b29d9143687c3bd6a66a906a69ea#components)
  
  ```md
  example: to fetch all the json records from a mongodb.log file from March 25, 20205 at 1:50 p.m. - 2:50 p.m. 
    cat mongodb | jsonFetcher -b 20250325135000 -e 20250325145000
  ```

