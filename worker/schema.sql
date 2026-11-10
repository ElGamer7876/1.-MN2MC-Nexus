-- MySQL 8.0+ / MariaDB 10.6+, utf8mb4 recommended
CREATE TABLE IF NOT EXISTS rooms (
  region VARCHAR(32) NOT NULL,
  room_id VARCHAR(128) NOT NULL,
  account_alias VARCHAR(128) NOT NULL,
  players SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  capacity SMALLINT UNSIGNED NOT NULL DEFAULT 40,
  status ENUM('open', 'full', 'offline') NOT NULL DEFAULT 'open',
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (region, room_id),
  UNIQUE KEY uq_region_account (region, account_alias),
  INDEX idx_region_status (region, status),
  CONSTRAINT chk_players CHECK (players <= capacity),
  CONSTRAINT chk_capacity CHECK (capacity BETWEEN 1 AND 40)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
