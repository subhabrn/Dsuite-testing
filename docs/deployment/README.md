# Deployment Guide for Resource Allocation AI

This document provides instructions for deploying the Resource Allocation AI application to production environments.

## Prerequisites

- AWS account with appropriate permissions
- Kubernetes cluster (EKS recommended)
- Docker registry access
- Terraform >= 1.0.0
- kubectl configured to access the cluster

## Deployment Steps

### 1. Configure Infrastructure with Terraform

Navigate to the `/infra/terraform` directory:
