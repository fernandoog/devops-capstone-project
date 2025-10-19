#!/bin/bash

# Test the deployed Account Service

echo "Testing Account Service deployment..."

# Get the route URL
ROUTE_URL=$(oc get route accounts -o jsonpath='{.spec.host}')
echo "Service URL: http://$ROUTE_URL"

# Test health endpoint
echo "Testing health endpoint..."
curl -f http://$ROUTE_URL/health || echo "Health check failed"

# Test root endpoint
echo "Testing root endpoint..."
curl -f http://$ROUTE_URL/ || echo "Root endpoint failed"

# Test accounts endpoint
echo "Testing accounts endpoint..."
curl -f http://$ROUTE_URL/accounts || echo "Accounts endpoint failed"

echo "Testing complete!"
