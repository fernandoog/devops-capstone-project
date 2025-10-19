#!/bin/bash

# Setup script for Tekton CD Pipeline
# This script sets up the Tekton pipeline components for the DevOps Capstone Project

echo "Setting up Tekton CD Pipeline..."

# Set environment variables
export GITHUB_ACCOUNT=${GITHUB_ACCOUNT:-"your-github-account"}
export SN_ICR_NAMESPACE=${SN_ICR_NAMESPACE:-"your-namespace"}

echo "GitHub Account: $GITHUB_ACCOUNT"
echo "ICR Namespace: $SN_ICR_NAMESPACE"

# Create PVC for pipeline workspace
echo "Creating PVC for pipeline workspace..."
oc create -f tekton/pvc.yaml

# Apply tasks
echo "Applying Tekton tasks..."
oc apply -f tekton/tasks.yaml

# Install required ClusterTasks from Tekton Hub
echo "Installing git-clone task from Tekton Hub..."
tkn hub install task git-clone

echo "Installing flake8 task from Tekton Hub..."
tkn hub install task flake8

# Apply pipeline
echo "Applying CD pipeline..."
oc apply -f tekton/pipeline.yaml

echo "Setup complete!"
echo ""
echo "To run the pipeline, use:"
echo "tkn pipeline start cd-pipeline \\"
echo "    -p repo-url=\"https://github.com/$GITHUB_ACCOUNT/devops-capstone-project.git\" \\"
echo "    -p branch=main \\"
echo "    -p build-image=image-registry.openshift-image-registry.svc:5000/$SN_ICR_NAMESPACE/accounts:1 \\"
echo "    -w name=pipeline-workspace,claimName=pipelinerun-pvc \\"
echo "    -s pipeline \\"
echo "    --showlog"
