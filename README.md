# twitch-rewards — deploy Tailscale Funnel (CGNAT-safe)

Bot twitch-rewards (fork de ada1ne/twitch-rewards) exposto à internet via **Tailscale Funnel** — HTTPS com cert Let's Encrypt automático, sem Cloudflare, sem port forward, funciona atrás de CGNAT.

## Arquitetura
```
Internet → *.ts.net (Tailscale edge, TLS) → tailscaled (Funnel) → 127.0.0.1:5151 (app) → db (postgres 16)
```

## Subir
```bash
sudo systemctl enable --now tailscaled
sudo tailscale up                      # autenticar no link que aparecer
sudo tailscale funnel 5151             # publicar (persistente até tailscale funnel reset)
sudo docker compose up -d --build
```

## .env (ver .env.example)
- `APP_HOST=https://<node>.<tailnet>.ts.net`
- `APP_PORT=443`

## Twitch Console
OAuth Redirect URL: `https://<node>.<tailnet>.ts.net/token`

## Notas
- CGNAT (Vivo, faixa 100.64/10) torna port forward/HTTP-01 impossíveis — por isso Funnel.
- Caddy/cloudflared removidos do compose (obsoletos).
- Fix próprio: `settings` importado em `controllers/authentication.py` (NameError no POST /token).
