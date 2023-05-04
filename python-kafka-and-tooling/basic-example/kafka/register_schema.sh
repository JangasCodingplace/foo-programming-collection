curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
--data '{"schema": "{\"type\":\"record\",\"name\":\"LineItem\",\"namespace\":\"CustomerOrders\",\"fields\":[{\"name\":\"customer_id\",\"type\":\"string\"},{\"name\":\"order_id\",\"type\":\"int\"}, {\"name\":\"article_id\",\"type\":\"string\"},{\"name\":\"timestamp\",\"type\":\"int\"}]}"}' \
http://localhost:8081/subjects/line-item-data-pbuf/versions
