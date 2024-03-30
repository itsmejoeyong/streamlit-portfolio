#!/bin/bash

SESSION_NAME="streamlit"
SESSION_PATH="/home/ubuntu/streamlit-portfolio/"
ACTIVATE_VENV="source .venv/bin/activate"
PYTHON_PIPELINE_CMD="python pipeline.py"
STREAMLIT_CMD="python -m streamlit run app.py"
MAX_RETRIES=5
RETRY_DELAY=2  # seconds

# Function to check if tmux session exists
function session_exists {
    tmux has-session -t $SESSION_NAME 2>/dev/null
}

# Function to create and setup tmux session
function setup_session {
    tmux new-session -d -s $SESSION_NAME
    tmux send-keys -t $SESSION_NAME "cd $SESSION_PATH" C-m
    tmux send-keys -t $SESSION_NAME "$ACTIVATE_VENV" C-m
    tmux send-keys -t $SESSION_NAME "$PYTHON_PIPELINE_CMD" C-m
    tmux send-keys -t $SESSION_NAME "$STREAMLIT_CMD" C-m
}

# Main script logic with retry mechanism
attempt=0
while [ $attempt -lt $MAX_RETRIES ]; do
    if session_exists; then
        echo "Session $SESSION_NAME exists. Killing the session."
        tmux kill-session -t $SESSION_NAME
    fi

    echo "Attempting to set up tmux session: $SESSION_NAME (Attempt: $((attempt+1)))"
    setup_session

    # Give tmux some time to start the session and check if it exists
    sleep $RETRY_DELAY
    if session_exists; then
        echo "Session $SESSION_NAME successfully created."
        exit 0
    else
        echo "Failed to create session $SESSION_NAME. Retrying in $RETRY_DELAY seconds..."
        sleep $RETRY_DELAY
    fi

    attempt=$((attempt+1))
done

echo "Failed to create tmux session $SESSION_NAME after $MAX_RETRIES attempts."
exit 1
