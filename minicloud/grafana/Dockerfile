FROM grafana/grafana:latest

COPY provisioning /etc/grafana/provisioning
COPY provisioning/dashboards/system-health.json /var/lib/grafana/dashboards/system-health.json

EXPOSE 3000