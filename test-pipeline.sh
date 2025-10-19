#!/bin/bash

# Test script for Tekton CD Pipeline
# This script tests the pipeline components

echo "Testing Tekton CD Pipeline components..."

# Check if we're in an OpenShift environment
if ! command -v oc &> /dev/null; then
    echo "Error: OpenShift CLI (oc) not found. Please ensure you're in an OpenShift environment."
    exit 1
fi

# Check if we're logged in to OpenShift
if ! oc whoami &> /dev/null; then
    echo "Error: Not logged in to OpenShift. Please run 'oc login' first."
    exit 1
fi

echo "✓ OpenShift CLI is available and user is logged in"

# Check if Tekton is installed
if ! oc get crd pipelines.tekton.dev &> /dev/null; then
    echo "Error: Tekton is not installed in this cluster."
    exit 1
fi

echo "✓ Tekton is installed"

# Check if required ClusterTasks exist
echo "Checking for required ClusterTasks..."

REQUIRED_TASKS=("git-clone" "flake8" "buildah" "openshift-client")

for task in "${REQUIRED_TASKS[@]}"; do
    if oc get clustertask $task &> /dev/null; then
        echo "✓ $task ClusterTask is available"
    else
        echo "⚠ $task ClusterTask not found - may need to be installed"
    fi
done

# Check if PVC exists
if oc get pvc pipelinerun-pvc &> /dev/null; then
    echo "✓ PVC pipelinerun-pvc exists"
else
    echo "⚠ PVC pipelinerun-pvc not found - run 'oc create -f tekton/pvc.yaml'"
fi

# Check if tasks are applied
if oc get task echo &> /dev/null; then
    echo "✓ Custom tasks are applied"
else
    echo "⚠ Custom tasks not found - run 'oc apply -f tekton/tasks.yaml'"
fi

# Check if pipeline is applied
if oc get pipeline cd-pipeline &> /dev/null; then
    echo "✓ CD pipeline is applied"
else
    echo "⚠ CD pipeline not found - run 'oc apply -f tekton/pipeline.yaml'"
fi

echo ""
echo "Pipeline test complete!"
echo ""
echo "To run the pipeline, ensure all components are set up and use:"
echo "tkn pipeline start cd-pipeline \\"
echo "    -p repo-url=\"https://github.com/\$GITHUB_ACCOUNT/devops-capstone-project.git\" \\"
echo "    -p branch=main \\"
echo "    -p build-image=image-registry.openshift-image-registry.svc:5000/\$SN_ICR_NAMESPACE/accounts:1 \\"
echo "    -w name=pipeline-workspace,claimName=pipelinerun-pvc \\"
echo "    -s pipeline \\"
echo "    --showlog"
