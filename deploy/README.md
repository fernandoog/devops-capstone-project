# Kubernetes Deployment

This directory contains Kubernetes manifests for deploying the Account Service to OpenShift.

## Files

- `deployment.yaml` - Kubernetes deployment for the accounts service
- `service.yaml` - Kubernetes service to expose the accounts service
- `route.yaml` - OpenShift route for external access
- `postgresql-ephemeral-template.json` - PostgreSQL database template

## Deployment Steps

### 1. Deploy PostgreSQL Database

```bash
# Create the PostgreSQL template
oc create -f postgresql-ephemeral-template.json

# Deploy PostgreSQL instance
oc new-app postgresql-ephemeral -p POSTGRESQL_DATABASE=accounts -p POSTGRESQL_USER=user1 -p POSTGRESQL_PASSWORD=password123
```

### 2. Deploy the Account Service

```bash
# Apply the deployment
oc apply -f deployment.yaml

# Apply the service
oc apply -f service.yaml

# Apply the route
oc apply -f route.yaml
```

### 3. Verify Deployment

```bash
# Check all resources
oc get all -l app=accounts

# Get the route URL
oc get routes
```

## Environment Variables

The deployment uses the following environment variables from the PostgreSQL secret:

- `DATABASE_HOST`: postgresql
- `DATABASE_NAME`: from postgresql secret
- `DATABASE_PASSWORD`: from postgresql secret  
- `DATABASE_USER`: from postgresql secret

## Scaling

To scale the service:

```bash
oc scale deployment accounts --replicas=5
```

## Health Checks

The service includes a health check endpoint at `/health` that returns the service status.
