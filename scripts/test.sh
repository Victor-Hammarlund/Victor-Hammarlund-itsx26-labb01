#!/usr/bin/env bash
LOGFILE="../docs/network-check.log"
TARGET="google.com"
log() {
printf "%s [%s] %s\n" "$(date -Is)" "$1" "$2" | tee -a "$LOGFILE"
}
if getent hosts "$TARGET" >/dev/null; then
log OK "DNS fungerar för $TARGET"
else
log FAIL "DNS misslyckades för $TARGET"
fi
