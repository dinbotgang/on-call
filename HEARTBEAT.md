# HEARTBEAT.md

## Polymarket Bot Trade Notifications

Check for new trades on the esports bot and notify George on Telegram.

State file: `/root/polymarket-bot/data/esports_state.json`
Last known trade count stored in: `/home/node/.openclaw/workspace/memory/bot-trade-state.json`

### Steps:
1. Read the state file
2. Read `memory/bot-trade-state.json` (create if missing: `{"lastTradeCount": 0, "notifiedIds": []}`)
3. Compare tradeHistory against notifiedIds
4. For any NEW trade NOT in notifiedIds:
   - If status = "closed": send Telegram message with entry %, exit %, PnL, and trigger reason (event.detail)
   - If status = "open": send Telegram message with entry %, trigger reason, and estimated close time
5. Update `memory/bot-trade-state.json` with new notifiedIds
6. If no new trades: HEARTBEAT_OK

## Cost Guard
- If daily API spend exceeds $3: clear this file (write just a comment), then send a Telegram message explaining it was turned off due to cost.
