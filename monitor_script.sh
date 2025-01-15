#!/bin/bash

LOG_DIR="/home/root/logs"
#LOG_DIR="/home/amantya/final_script/application/logs"
MAX_LOG_FILES=5

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

while true; do
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    LOG_FILE="$LOG_DIR/5GCamera_$TIMESTAMP.log"

    # Run binary
    /home/root/app_suresh/testproject/5GCamera >> "$LOG_FILE" 2>&1
    #/home/amantya/final_script/application/5GCamera >> "$LOG_FILE" 2>&1

    # Check the exit status
    if [ $? -eq 0 ]; then
        echo "Binary exited successfully."
    else
        echo "Binary crashed or exited with an error. Rebooting..."
        # delay before rebooting to avoid immediate restart
        sleep 5
        reboot
    fi

    # Delete old log files if exceeding the maximum count
    CURRENT_LOG_COUNT=$(ls -1 "$LOG_DIR" | grep -c "5GCamera_")
    if [ "$CURRENT_LOG_COUNT" -gt "$MAX_LOG_FILES" ]; then
        # Sort files by timestamp and delete the oldest one
        OLDEST_LOG_FILE=$(ls -1t "$LOG_DIR" | grep "5GCamera_" | tail -n 1)
        rm "$LOG_DIR/$OLDEST_LOG_FILE"
    fi
done

