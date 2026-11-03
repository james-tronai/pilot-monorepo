# pilot-monorepo

Demo monorepo for two experiments on the k3s homelab (design: k3s-infra `docs/preview-devspace-design.md`):

1. **PR preview environments**: comment `/preview` on a PR → `https://pr-<n>.preview.zenbyte.biz` (Keycloak login).
   `/preview ttl=7d` changes the TTL (default 48h), `/preview off` tears it down. Max 2 at a time.
2. **DevSpace**: `devspace dev` gives one developer a full environment in the cluster with hot reload.

| Service | Stack | Routes |
| --- | --- | --- |
| `apps/api-orders` | FastAPI, MongoDB, Redis | `/api/orders/*` |
| `apps/api-chat` | FastAPI, OpenRouter | `/api/chat/*` |
| `apps/web` | React + TypeScript + Vite | `/` |

`deploy/chart` is the single Helm chart both experiments use. Images are built by GitHub Actions
into `ghcr.io/james-tronai/pilot-monorepo/<service>:<sha>`.
# preview test 2
