# Tekton CD Pipeline

This directory contains the Tekton pipeline configuration for the DevOps Capstone Project.

## Files

- `pvc.yaml` - PersistentVolumeClaim for pipeline workspace
- `tasks.yaml` - Custom Tekton tasks (echo, nose)
- `pipeline.yaml` - Main CD pipeline definition

## Pipeline Tasks

The CD pipeline includes the following tasks:

1. **clone** - Clones the repository using git-clone ClusterTask
2. **lint** - Runs flake8 linting using flake8 ClusterTask
3. **tests** - Runs unit tests using custom nose task
4. **build** - Builds Docker image using buildah ClusterTask
5. **deploy** - Deploys to OpenShift using openshift-client ClusterTask

## Setup Instructions

1. Set environment variables:
   ```bash
   export GITHUB_ACCOUNT=your-github-account
   export SN_ICR_NAMESPACE=your-namespace
   ```

2. Run the setup script:
   ```bash
   ./setup-tekton.sh
   ```

3. Start the pipeline:
   ```bash
   tkn pipeline start cd-pipeline \
       -p repo-url="https://github.com/$GITHUB_ACCOUNT/devops-capstone-project.git" \
       -p branch=main \
       -p build-image=image-registry.openshift-image-registry.svc:5000/$SN_ICR_NAMESPACE/accounts:1 \
       -w name=pipeline-workspace,claimName=pipelinerun-pvc \
       -s pipeline \
       --showlog
   ```

## Pipeline Parameters

- `repo-url`: GitHub repository URL
- `branch`: Git branch to build (default: main)
- `build-image`: Container image name for deployment

## Workspaces

- `pipeline-workspace`: Shared workspace for all tasks

## Dependencies

The pipeline requires the following ClusterTasks to be installed:
- git-clone
- flake8
- buildah
- openshift-client

These are typically pre-installed in OpenShift environments.
