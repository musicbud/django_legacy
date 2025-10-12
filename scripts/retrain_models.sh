#!/bin/bash
################################################################################
# Recommendation Model Retraining Script
# 
# This script retrains recommendation models and can be run via cron
# Add to crontab with: 0 2 * * * /path/to/retrain_models.sh
################################################################################

# Configuration
PROJECT_DIR="/home/mahmoud/Documents/GitHub/backend"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="/var/log/musicbud"
LOG_FILE="$LOG_DIR/model_retraining.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
set -e
trap 'log "ERROR: Script failed on line $LINENO"' ERR

log "================================================"
log "Starting model retraining"
log "================================================"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
log "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Run training
log "Training models..."
python manage.py train_recommendations --type all 2>&1 | tee -a "$LOG_FILE"

log "================================================"
log "Model retraining completed successfully"
log "================================================"

# Optional: Send notification (uncomment if needed)
# echo "Model retraining completed at $(date)" | mail -s "MusicBud: Model Training Complete" admin@example.com

exit 0
