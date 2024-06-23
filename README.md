# TTN Gateways Monitoring – TGM

For gateways monitoring, we use an open-source time series database InfluxDB and an open-source analytical and interactive visualization web application Grafana. Gateway data is loaded from The Things Stack using our TGM. The TGM makes a GET requests, parses the data received in the response, and then stores the data in the InfluxDB database.

## More information

- More information on deploying the new Grafana, InfluxDB v1.8.10 and TGM 1 on the site: https://lora.vsb.cz/index.php/ttn-gateways-monitoring-tgm/
