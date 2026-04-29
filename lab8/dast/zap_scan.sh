set -e

# Переменные
ZAP_IMAGE="${ZAP_IMAGE:-ghcr.io/zaproxy/zaproxy:stable}"
TARGET_URL="${TARGET_URL:-http://host.docker.internal:8080}"
REPORT_DIR="$(cd "$(dirname "$0")" && pwd)/reports"
CONFIG_FILE="$(cd "$(dirname "$0")" && pwd)/zap-baseline.conf"

# Создаём директорию для отчётов
mkdir -p "$REPORT_DIR"

echo "Запуск OWASP ZAP baseline scan..."
echo "Цель: $TARGET_URL"
echo "Отчёты: $REPORT_DIR"

# Запуск ZAP в Docker
docker run -t --rm \
    -v "$REPORT_DIR:/zap/wrk/:rw" \
    -v "$CONFIG_FILE:/zap/config.conf:ro" \
    "$ZAP_IMAGE" \
    zap-baseline.py \
    -t "$TARGET_URL" \
    -c /zap/config.conf \
    -r zap_report.html \
    -J zap_report.json \
    -x zap_report.xml \
    -w zap_report.md \
    -m 2 \
    -d

echo "Сканирование завершено. Отчёты сохранены в $REPORT_DIR"