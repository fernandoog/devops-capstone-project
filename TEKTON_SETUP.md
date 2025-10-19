# Tekton CD Pipeline Setup Guide

This guide explains how to set up and run the Tekton CD pipeline for the DevOps Capstone Project.

## Overview

The CD pipeline automates the following steps:
1. **Clone** - Clones the repository
2. **Lint** - Runs flake8 linting
3. **Test** - Runs unit tests with nose
4. **Build** - Builds Docker image with buildah
5. **Deploy** - Deploys to OpenShift

## Prerequisites

- OpenShift cluster with Tekton installed
- OpenShift CLI (oc) configured and logged in
- GitHub repository with the project code
- PostgreSQL database running in OpenShift (for tests)

## Environment Variables

Set the following environment variables:

```bash
export GITHUB_ACCOUNT=your-github-username
export SN_ICR_NAMESPACE=your-openshift-namespace
```

## Setup Steps

### 1. Create PVC for Pipeline Workspace

```bash
oc create -f tekton/pvc.yaml
```

### 2. Apply Custom Tasks

```bash
oc apply -f tekton/tasks.yaml
```

### 3. Install Required ClusterTasks

```bash
# Install git-clone task
tkn hub install task git-clone

# Install flake8 task
tkn hub install task flake8
```

### 4. Apply the Pipeline

```bash
oc apply -f tekton/pipeline.yaml
```

### 5. Verify Setup

```bash
./test-pipeline.sh
```

## Running the Pipeline

### Manual Pipeline Run

```bash
tkn pipeline start cd-pipeline \
    -p repo-url="https://github.com/$GITHUB_ACCOUNT/devops-capstone-project.git" \
    -p branch=main \
    -p build-image=image-registry.openshift-image-registry.svc:5000/$SN_ICR_NAMESPACE/accounts:1 \
    -w name=pipeline-workspace,claimName=pipelinerun-pvc \
    -s pipeline \
    --showlog
```

### Pipeline Parameters

- `repo-url`: GitHub repository URL
- `branch`: Git branch to build (default: main)
- `build-image`: Container image name for deployment

## Pipeline Tasks Details

### Clone Task
- Uses `git-clone` ClusterTask
- Clones the specified repository and branch
- Outputs to shared workspace

### Lint Task
- Uses `flake8` ClusterTask
- Runs code linting with specified parameters
- Runs in parallel with tests after clone

### Test Task
- Uses custom `nose` task
- Runs unit tests with nose test runner
- Uses SQLite database for testing
- Runs in parallel with lint after clone

### Build Task
- Uses `buildah` ClusterTask
- Builds Docker image from source code
- Pushes to OpenShift internal registry
- Runs after both lint and test complete

### Deploy Task
- Uses `openshift-client` ClusterTask
- Updates deployment manifest with built image
- Applies Kubernetes manifests to cluster
- Runs after build completes

## Monitoring Pipeline

### Check Pipeline Runs

```bash
tkn pipelinerun ls
```

### View Pipeline Logs

```bash
tkn pipelinerun logs --last
```

### Check Pipeline Status

```bash
tkn pipelinerun describe <pipeline-run-name>
```

## Troubleshooting

### Common Issues

1. **PVC not found**: Ensure PVC is created with `oc create -f tekton/pvc.yaml`
2. **ClusterTask not found**: Install required tasks with `tkn hub install task <name>`
3. **Pipeline fails**: Check logs with `tkn pipelinerun logs --last`
4. **Build fails**: Ensure Dockerfile exists and is valid
5. **Deploy fails**: Check that deployment.yaml has correct image placeholder

### Debug Commands

```bash
# Check all pipeline resources
oc get pipeline,pvc,task,pipelinerun

# Check pipeline run details
tkn pipelinerun describe <name>

# View task logs
tkn taskrun logs <task-run-name>
```

## Pipeline Configuration Files

- `tekton/pvc.yaml` - PersistentVolumeClaim for workspace
- `tekton/tasks.yaml` - Custom tasks (echo, nose)
- `tekton/pipeline.yaml` - Main pipeline definition
- `deploy/deployment.yaml` - Kubernetes deployment manifest

## Next Steps

After successful pipeline execution:

1. Verify deployment is running:
   ```bash
   oc get pods -l app=accounts
   ```

2. Check service status:
   ```bash
   oc get svc accounts
   ```

3. Test the deployed application:
   ```bash
   curl http://$(oc get route accounts -o jsonpath='{.spec.host}')/health
   ```

## Evidence Collection

For course submission, collect:

1. Pipeline run logs:
   ```bash
   tkn pipelinerun logs -L > pipelinerun.txt
   ```

2. Screenshot of successful deployment
3. Screenshot of running pods
4. Test results from deployed application
