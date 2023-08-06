#!/bin/bash
set -e

# Move to project root
cd ../../

# Build Docker container
echo -e  "\n==============================="
echo -e  "|  Running Docker container   |"
echo -e  "===============================\n"

if [[ "x$LIVE" == "xFalse" ]]; then
    echo "Running without live code changes."
    docker run -p8888:8888 -it timeseria
else
    # DEFAULT_PLOT_TYPE=image ./run.sh
    echo "Running with live code changes. Use LIVE=False to disable."
    docker run -p8888:8888 -eDEFAULT_PLOT_TYPE=$DEFAULT_PLOT_TYPE -v $PWD:/opt/Timeseria -v $PWD/notebooks:/notebooks -v /Users/ste/Library/Mobile\ Documents/com~apple~CloudDocs/Workspace/Notebooks:/notebooks/Workspace/Notebooks/ -it timeseria    
fi

