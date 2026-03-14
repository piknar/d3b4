---
name: "d3b4-deploy"
description: "VPS-first deployment workflow for d3b4. Enforces testing on VPS before pushing to GitHub or Docker Hub. Use for all d3b4 code changes, new features, API integrations, and releases."
version: "1.0.0"
author: "Deby"
tags: ["d3b4", "deploy", "vps", "docker", "release", "testing"]
trigger_patterns:
  - "deploy d3b4"
  - "push d3b4"
  - "release d3b4"
  - "test on vps"
  - "push to hub"
  - "build d3b4"
  - "apply changes"
  - "add to d3b4"
---

# d3b4 VPS-First Deployment Skill

## ⚠️ Golden Rule

**NEVER push to GitHub or Docker Hub without a confirmed working build on the VPS test container first.**

## Environment

| Item | Value |
|------|-------|
| VPS IP | 168.231.72.66 |
| VPS SSH password | Piknar&Zosia13 |
| VPS build path | /opt/d3b4-build/ |
| Test container | d3b4-test |
| Test port | 8081 |
| Test URL | http://168.231.72.66:8081 |
| Local repo | /a0/usr/workdir/d3b4-repo/ |
| Docker image | piknar/d3b4:test-latest |
| GitHub remote | https://github.com/piknar/d3b4.git |

## SSH Access

Always use sshpass for VPS SSH access:
```bash
sshpass -p 'Piknar&Zosia13' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@168.231.72.66 'COMMAND'
```

For rsync:
```bash
rsync -avz --exclude='.git' --exclude='venv' --exclude='__pycache__' --exclude='node_modules' \
  -e "sshpass -p 'Piknar&Zosia13' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
  /a0/usr/workdir/d3b4-repo/ root@168.231.72.66:/opt/d3b4-build/
```

## Full Deployment Workflow

### Phase 1: Make Changes Locally

1. Make all code changes in `/a0/usr/workdir/d3b4-repo/`
2. Verify changes are correct with `git diff`
3. **DO NOT commit or push yet**

### Phase 2: Sync to VPS and Build Test Image

```bash
# Step 1: Sync code to VPS
rsync -avz --exclude='.git' --exclude='venv' --exclude='__pycache__' --exclude='node_modules' \
  -e "sshpass -p 'Piknar&Zosia13' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
  /a0/usr/workdir/d3b4-repo/ root@168.231.72.66:/opt/d3b4-build/

# Step 2: Build Docker image on VPS
sshpass -p 'Piknar&Zosia13' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@168.231.72.66 \
  'cd /opt/d3b4-build && docker build -t piknar/d3b4:test-latest . 2>&1 | tail -15'
```

### Phase 3: Restart Test Container

```bash
sshpass -p 'Piknar&Zosia13' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@168.231.72.66 \
  'docker stop d3b4-test && docker rm d3b4-test && docker run -d \
    --name d3b4-test \
    -p 8081:8080 \
    -e PORT=8080 \
    -e A0_CHAT_MODEL_NAME="venice/claude-sonnet-4-6" \
    -e A0_UTIL_MODEL_NAME="venice/claude-sonnet-4-6" \
    piknar/d3b4:test-latest && sleep 10 && \
    docker ps --filter "name=d3b4-test" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

### Phase 4: Verify Container Running

```bash
sshpass -p 'Piknar&Zosia13' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@168.231.72.66 \
  'docker logs d3b4-test --tail 20'
```

✅ Container should show: `[d3b4] Starting on 0.0.0.0:8080...`

### Phase 5: Test on VPS

**Tell the user to test at:** http://168.231.72.66:8081

For API key testing, test directly with curl first:
```bash
curl -s https://API_ENDPOINT/v1/chat/completions \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "MODEL_NAME", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 10}'
```

✅ **Wait for user confirmation: "it works"**  
❌ **If not working: fix issues and repeat Phase 1-5**

### Phase 6: Push to GitHub (ONLY after VPS confirmed working)

```bash
cd /a0/usr/workdir/d3b4-repo

# Commit the changes
git add -A
git commit -m "feat: description of changes"
git push origin main
```

### Phase 7: Tag Version to Trigger Docker Hub Build

```bash
# Check current latest tag
git tag -l | sort -V | tail -5

# Create and push new version tag (increments patch version)
git tag vX.Y.Z
git push origin vX.Y.Z
```

This triggers GitHub Actions workflow which:
1. Builds Docker image
2. Runs smoke test
3. Pushes to Docker Hub as `piknar/d3b4:latest` and `piknar/d3b4:vX.Y.Z`

### Phase 8: Verify Docker Hub Build

```bash
# Check Docker Hub tags
curl -s https://hub.docker.com/v2/repositories/piknar/d3b4/tags/ | grep -o '"name":"[^"]*"' | head -10
```

## Quick Reference Checklist

```
[ ] 1. Make local code changes
[ ] 2. git diff - verify changes
[ ] 3. rsync to VPS
[ ] 4. docker build on VPS
[ ] 5. restart d3b4-test container
[ ] 6. check container logs - confirm startup
[ ] 7. user tests at http://168.231.72.66:8081
[ ] 8. ✅ USER CONFIRMS WORKING
[ ] 9. git add + commit + push to main
[ ] 10. git tag + push tag for Docker Hub build
```

## Common Issues

### Container crashes on startup
```bash
# Check logs for errors
sshpass -p 'Piknar&Zosia13' ssh ... 'docker logs d3b4-test 2>&1 | tail -50'
```

### Build fails
```bash
# Run full build output
sshpass -p 'Piknar&Zosia13' ssh ... 'cd /opt/d3b4-build && docker build -t piknar/d3b4:test-latest . 2>&1'
```

### Revert to previous version
```bash
cd /a0/usr/workdir/d3b4-repo
git checkout conf/model_providers.yaml .env.example  # revert specific files
# OR
git revert HEAD  # revert last commit
git push origin main
# Then re-rsync, rebuild and restart
```

## Notes

- The test container on port 8081 is for testing ONLY
- Port 80/443 (production) runs the stable `latest` tag from Docker Hub
- Always increment patch version (v0.2.0 → v0.2.1) for minor changes
- Increment minor version (v0.2.0 → v0.3.0) for new features
