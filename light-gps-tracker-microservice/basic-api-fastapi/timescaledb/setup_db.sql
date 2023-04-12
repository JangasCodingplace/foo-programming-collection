CREATE TABLE vehicle_position
(
  timestamp  TIMESTAMP        NOT NULL,
  vehicle_id UUID             NOT NULL,
  lat        DOUBLE PRECISION NOT NULL,
  long       DOUBLE PRECISION NOT NULL,
  speed      INTEGER          NOT NULL,
  CONSTRAINT unique_vehicle_position UNIQUE (vehicle_id, timestamp)
);

SELECT create_hypertable('vehicle_position','timestamp');
