#!/bin/bash
# Setup script for RALF on Kubernetes
# Run this after you have a K8s cluster

set -e

echo "═══════════════════════════════════════════════════════════"
echo "  RALF Kubernetes Setup"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check prerequisites
command -v kubectl >/dev/null 2>&1 || { echo "kubectl required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "docker required but not installed."; exit 1; }

# Configuration
NAMESPACE="ralf"
IMAGE_NAME="blackbox5/ralf-agent"
IMAGE_TAG="latest"

echo "Step 1: Build RALF Agent Docker Image"
echo "───────────────────────────────────────────────────────────"
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
echo "✓ Image built: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""

echo "Step 2: Push to Registry (optional for local k3s)"
echo "───────────────────────────────────────────────────────────"
read -p "Push to Docker Hub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker push ${IMAGE_NAME}:${IMAGE_TAG}
    echo "✓ Image pushed"
else
    echo "Skipping push (for local k3s, image will be available locally)"
fi
echo ""

echo "Step 3: Create Namespace and Storage"
echo "───────────────────────────────────────────────────────────"
kubectl apply -f ralf-deployment.yaml
echo "✓ Namespace and PVCs created"
echo ""

echo "Step 4: Configure Secrets"
echo "───────────────────────────────────────────────────────────"
echo "You need to provide:"
echo "  1. Anthropic API Key (for Claude)"
echo "  2. GitHub Personal Access Token (for repo access)"
echo ""

read -p "Enter Anthropic API Key: " ANTHROPIC_KEY
read -p "Enter GitHub Token: " GITHUB_TOKEN

kubectl create secret generic ralf-secrets -n ${NAMESPACE} \
    --from-literal=anthropic-api-key="${ANTHROPIC_KEY}" \
    --from-literal=github-token="${GITHUB_TOKEN}" \
    --dry-run=client -o yaml | kubectl apply -f -

echo "✓ Secrets created"
echo ""

echo "Step 5: Clone Blackbox5 to Persistent Volume"
echo "───────────────────────────────────────────────────────────"
echo "Creating init pod to clone repository..."

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: blackbox5-init
  namespace: ${NAMESPACE}
spec:
  containers:
    - name: git
      image: alpine/git
      command:
        - sh
        - -c
        - |
          cd /data
          git clone https://github.com/Lordsisodia/blackbox5.git . || \
          (git pull origin main)
          chown -R 1000:1000 /data
      volumeMounts:
        - name: code
          mountPath: /data
  volumes:
    - name: code
      persistentVolumeClaim:
        claimName: blackbox5-code
  restartPolicy: Never
EOF

echo "Waiting for clone to complete..."
kubectl wait --for=condition=Succeeded pod/blackbox5-init -n ${NAMESPACE} --timeout=300s
kubectl delete pod blackbox5-init -n ${NAMESPACE}
echo "✓ Blackbox5 cloned to persistent volume"
echo ""

echo "Step 6: Start RALF Agent"
echo "───────────────────────────────────────────────────────────"
kubectl scale deployment ralf-agent -n ${NAMESPACE} --replicas=1
echo "✓ RALF agent started"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  Setup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Useful commands:"
echo "  kubectl logs -n ${NAMESPACE} deployment/ralf-agent -f    # View logs"
echo "  kubectl exec -n ${NAMESPACE} -it deployment/ralf-agent -- /bin/bash  # Shell"
echo "  kubectl get pods -n ${NAMESPACE}                          # Check status"
echo ""
echo "RALF is now running and will continuously improve Blackbox5"
echo ""
