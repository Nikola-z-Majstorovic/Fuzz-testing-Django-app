# Fuzz-testing-Django-app

## This is Django project which is integrated with OWASP ZAP tool and ELK Stack 

It's important to download tools mentioned above

### Configuration of the Owasp Zap Tool

#### ZAP requires Java 11+ to run.

#### In order to OWASP be able to intercept HTTPS requests, it is necessary to generate a certificate by OWASP that we import into the browser. 
In OWASP go to tools/options/dynamic SSL certificates and then generate certificate and copy it into browser certificate list.

#### In order to Filebeat  be able to register changes that occur in Django's log file, it is necessary to add the following lines to the filebeat.yml file:

```
filebeat.inputs:
- type: log
  enabled: true
    - path/to/log_file
  fields:
    app_name: bookmarks
  processors:
    - decode_json_fields:
        fields: ["message"]
        target: ""
        overwrite_keys: true
        add_error_key: true
```

#### To integrate Kibana with ElasticSearch, we need to edit the kibana.yaml file located in the config directory in the Kibana download directory, and uncomment line:

```
elasticsearch.hosts: ["http://localhost:9200"]
```