#!/bin/bash

# Deploy Account Service to OpenShift

echo "Deploying Account Service to OpenShift..."

# Create PostgreSQL template
echo "Creating PostgreSQL template..."
oc create -f postgresql-ephemeral-template.json

# Deploy PostgreSQL instance
echo "Deploying PostgreSQL database..."
oc new-app postgresql-ephemeral \
  -p POSTGRESQL_DATABASE=accounts \
  -p POSTGRESQL_USER=user1 \
  -p POSTGRESQL_PASSWORD=password123

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
oc wait --for=condition=ready pod -l name=accounts --timeout=300s

# Deploy the Account Service
echo "Deploying Account Service..."
oc apply -f deployment.yaml
oc apply -f service.yaml
oc apply -f route.yaml

# Wait for deployment to be ready
echo "Waiting for Account Service to be ready..."
oc wait --for=condition=ready pod -l app=accounts --timeout=300s

# Display status
echo "Deployment complete!"
echo "Resources:"
oc get all -l app=accounts

echo "Route:"
oc get routes
