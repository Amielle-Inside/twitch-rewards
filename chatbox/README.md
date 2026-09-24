# Chatbox Overlay — Firebot v5 + twitch-rewards

Overlay de chat pro OBS que mostra **pronomes customizados** do bot twitch-rewards em destaque, com fallback pros pronomes nativos do Firebot.

Baseado no [chat_overlay_events](https://github.com/djnrrd/chat_overlay_events) de @djnrrd (licença em `LICENSE-firebot-overlay`), modificado por Amielle.

## Layout resultante

```
(ela/dela)              ← pronomes do bot, bold 22px, só aparece se cadastrado
Nome: mensagem do chat  ← cor da Twitch preservada, contorno preto, fundo transparente
```

## Requisitos

| Componente | Função |
|---|---|
| [Firebot v5](https://github.com/crowbartools/Firebot) | recebe o chat da Twitch e emite eventos via WebSocket local (`ws://localhost:7472`) |
| twitch-rewards (este repo) | fonte dos pronomes customizados em `https://<seu-host>/users/<displayName>` |
| OBS Studio | Browser Source apontando pro `chat.html` local |

**Nova dependência:** nenhuma adicional — o overlay usa `fetch` nativo do browser do OBS. A única dependência externa nova é o bot twitch-rewards rodando (docker compose up).

## Instalação passo a passo

### 1. Subir o bot
```bash
git clone https://github.com/Amielle-Inside/twitch-rewards.git
cd twitch-rewards
cp .env.example .env   # preencher POSTGRES_PASSWORD, JWT_ENCODING_KEY, TWITCH_APP_CLIENT_ID/SECRET, APP_HOST
sudo docker compose up -d --build
```

### 2. Configurar o Firebot
- Importar `chat_overlay_events.firebotsetup` (File → Import → Setup File)
- Ele cria o event group "Chat Overlay": Chat Message, Chat Cleared, Banned, Timeout e Message Deleted → todos enviados como custom WebSocket events (`chat_overlay_msg`, `chat_overlay_clear`, etc.)
- Firebot conecta no Twitch e abre o servidor WebSocket na porta **7472**

### 3. Configurar o overlay
- Editar `firebot-overlay/chat.js` linha 6:
  ```js
  const rewardsServer = "https://bazzite.tail6360a1.ts.net"; // URL do seu bot
  ```
- OBS → Source → **Browser** → Local file: `firebot-overlay/chat.html`
- Largura/altura: 1920x1080 (ou a resolução do overlay no Firebot)
- **Deixar o campo Custom CSS do OBS vazio** (o estilo já está todo em `chat_style.css`; CSS custom externo é sobrescrito pelo arquivo e some com o pronome)

### 4. Usar
- Usuário cadastra pronomes em `https://<seu-host>` (login Twitch) → Aparece `(pronomes)` acima do nome nas mensagens
- Sem cadastro no bot → usa o pronome do Firebot
- Sem pronome em nenhuma fonte → linha omitida

## O que foi alterado em relação ao original (djnrrd)

### `chat.js`
| Linha(s) | Alteração | Motivo |
|---|---|---|
| 6–8 | `rewardsServer`, `pronounsCache` (Map) | URL do bot + cache de 1 fetch por usuário (evita spam de requisições a cada mensagem) |
| 10–32 | `getBotPronouns(displayName)` | busca pronome no bot com cache; `null` se 404/offline (try/catch pra bot caído não quebrar o overlay) |
| 80 | `add_chat_msg` virou `async` | precisa `await` do pronome do bot antes de montar o DOM |
| 87–106 | removidas as badges; linha de pronomes própria | badges saíram do layout a pedido; pronome ganhou linha dedicada, só renderizada se existir |
| 108–124 | `line_div` com nome + `: ` inline | nome e texto na mesma linha, separados por dois-pontos |
| 139–141 | `text_div` movido pra dentro de `line_div`; `msg_div` recebe `user_div` | o texto faz parte da linha do nome; quebra de linha natural em mensagens longas |
| 190–196 | chamada do `add_chat_msg` com `.then()` | `clear_out_of_bounds` e `timeout_message` só depois da mensagem montada (evita medir DOM incompleto) |

### `chat_style.css` (reescrito)
| Bloco | Alteração | Motivo |
|---|---|---|
| `html, body` | fundo transparente + `overflow: hidden` | overlay de OBS não pode ter fundo/scroll |
| `.chat_message` | gradiente arco-íris removido; 28px bold branco, contorno preto (`-webkit-text-stroke`), sombra | legibilidade sobre gameplay, visual limpo |
| `.pronoun_line` / `.pronoun_line p` | linha dedicada pro pronome, `width: fit-content` | pronome em destaque, linha some quando vazio |
| `.pronoun_tag` | 22px, weight 900, `#e5e5e5`, alinhado `vertical-align: middle` | mesmo tamanho do nome, bem visível |
| `.display_name` | 22px weight 900, **sem `color`** | cor do usuário vem do style inline da Twitch |
| `.msg_colon` | dois-pontos estilizado | separador nome/texto |
| `.msg_text` | `display: inline`, margens zeradas | texto cola na linha do nome |
| pseudo-elementos (`::before/::after`) | `content: none` | remove resíduos de gradiente do tema original |

## Deploy do bot (resumo)

Ver `README.md` na raiz. HTTPS público via **Tailscale Funnel** (funciona atrás de CGNAT, sem Cloudflare/port forward):
```bash
sudo systemctl enable --now tailscaled
sudo tailscale up
sudo tailscale funnel 5151
sudo docker compose up -d --build
```

Redirect URI na [Twitch Console](https://dev.twitch.tv/console): `https://<seu-host>/token`
