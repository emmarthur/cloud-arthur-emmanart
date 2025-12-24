#!/bin/bash
# Quick rebuild and redeploy script for Cloud Run
# Run this from the final/server/ directory in Git Bash
# IMPORTANT: Replace YOUR_ALPHA_VANTAGE_KEY and YOUR_FRED_KEY with actual keys from your .env file

echo "Building Docker image..."
gcloud builds submit --tag gcr.io/cloud-arthur-emmanart/final

echo ""
echo "Deploying to Cloud Run..."
# Get API keys from .env file (if it exists) or use placeholders
if [ -f .env ]; then
    source .env
    gcloud run deploy final \
      --image gcr.io/cloud-arthur-emmanart/final \
      --region us-west1 \
      --platform managed \
      --allow-unauthenticated \
      --set-env-vars ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY},FRED_API_KEY=${FRED_API_KEY}
else
    echo "  .env file not found. Please manually set API keys:"
    echo "gcloud run deploy final \\"
    echo "  --image gcr.io/cloud-arthur-emmanart/final \\"
    echo "  --region us-west1 \\"
    echo "  --platform managed \\"
    echo "  --allow-unauthenticated \\"
    echo "  --set-env-vars ALPHA_VANTAGE_API_KEY=YOUR_KEY,FRED_API_KEY=YOUR_KEY"
fi

echo ""
echo "[OK] Deployment complete! Test with: cd ../client && python client.py"

