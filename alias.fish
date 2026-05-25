# Path to Python executable.
set -g PYTHON_BIN python

# Directory containing the Python scripts.
set -g SCRIPTS_DIR $PWD

alias appName "$PYTHON_BIN $SCRIPTS_DIR/appName.py"
alias bytesRead "$PYTHON_BIN $SCRIPTS_DIR/bytesRead.py"
alias collScans "$PYTHON_BIN $SCRIPTS_DIR/collScans.py"
alias connpool "$PYTHON_BIN $SCRIPTS_DIR/connpool.py"
alias connections "$PYTHON_BIN $SCRIPTS_DIR/connections.py"
alias control "$PYTHON_BIN $SCRIPTS_DIR/control.py"
alias cpuc "$PYTHON_BIN $SCRIPTS_DIR/cpuc.py"
alias cpuPerDatabase "$PYTHON_BIN $SCRIPTS_DIR/cpuPerDatabase.py"
alias docsExamined "$PYTHON_BIN $SCRIPTS_DIR/docsExamined.py"
alias drivers "$PYTHON_BIN $SCRIPTS_DIR/drivers.py"
alias formatOne "$PYTHON_BIN $SCRIPTS_DIR/formatOne.py"
alias formatTwo "$PYTHON_BIN $SCRIPTS_DIR/formatOne.py --legacy"
alias jsonFetcher "$PYTHON_BIN $SCRIPTS_DIR/jsonFetcher.py"
alias keysExamined "$PYTHON_BIN $SCRIPTS_DIR/keysExamined.py"
alias millis "$PYTHON_BIN $SCRIPTS_DIR/millis.py"
alias ns "$PYTHON_BIN $SCRIPTS_DIR/ns.py"
alias nsCount "$PYTHON_BIN $SCRIPTS_DIR/nsCount.py"
alias nsCountUser "$PYTHON_BIN $SCRIPTS_DIR/nsCountUser.py"
alias nsIndexes "$PYTHON_BIN $SCRIPTS_DIR/nsIndexes.py"
alias phead "$PYTHON_BIN $SCRIPTS_DIR/phead.py"
alias queryHash "$PYTHON_BIN $SCRIPTS_DIR/queryHash.py"
alias queryTargetting "$PYTHON_BIN $SCRIPTS_DIR/queryTargetting.py"
alias startup "$PYTHON_BIN $SCRIPTS_DIR/startup.py"
