
#!/bin/bash
set -euo pipefail

trap 'rc=$?; echo "EPIAS HATA: satir=$LINENO kod=$rc" >&2' ERR

SECRETS="/config/secrets.yaml"

get_secret() {
  local key="$1"
  local value
  value=$(grep -m1 -E "^${key}:" "$SECRETS" |
    sed -E "s/^[^:]+:[[:space:]]*//")
  value="${value#\"}"
  value="${value%\"}"
  value="${value#\'}"
  value="${value%\'}"
  printf '%s' "$value"
}

USER_NAME=$(get_secret epias_username)
PASSWORD=$(get_secret epias_password)

# EPİAŞ kimlik doğrulama
TGT=$(curl -fsS --max-time 20 \
  -X POST "https://giris.epias.com.tr/cas/v1/tickets" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: text/plain" \
  --data-urlencode "username=$USER_NAME" \
  --data-urlencode "password=$PASSWORD" |
  tr -d '\r\n')

unset USER_NAME PASSWORD

if [[ "$TGT" != TGT-* ]]; then
  echo "EPIAS: TGT alinamadi" >&2
  exit 1
fi

# Türkiye saatine göre mevcut saat
CURRENT_HOUR=$(TZ=Europe/Istanbul date +%Y-%m-%dT%H:)
CURRENT_START="${CURRENT_HOUR}00:00+03:00"

# PTF sorgusu
DATA=$(curl -fsS --max-time 30 \
  -X POST \
  "https://seffaflik.epias.com.tr/electricity-service/v1/markets/dam/data/mcp" \
  -H "TGT: $TGT" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d "{\"startDate\":\"${CURRENT_START}\",\"endDate\":\"${CURRENT_START}\"}")

unset TGT

# Mevcut saatin PTF fiyatı (TL/kWh)
printf '%s' "$DATA" | jq -er \
  --arg hour "$CURRENT_HOUR" '
  [
    .items[]?
    | select(.date | startswith($hour))
    | (.price / 1000)
  ]
  | if length == 1
    then (.[0] * 100000 | round / 100000)
    else error("Guncel saat icin PTF bulunamadi")
    end
'
