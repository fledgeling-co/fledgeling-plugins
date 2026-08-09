-- 0007: retire the pre-2024 accounts table.
-- legacy_accounts was superseded by accounts in 0004. Nothing reads it.
DROP TABLE legacy_accounts;
