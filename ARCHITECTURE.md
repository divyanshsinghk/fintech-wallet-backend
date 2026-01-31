🔒 Core Business Rules (Final – Do Not Change)

Copy this as-is and then read it until it’s clear:

One User → One Wallet

A user can never have more than one wallet.

Wallet is created automatically after successful registration.

No Negative Balance

Debit transactions must fail if balance is insufficient.

Balance checks happen before any update.

Atomic Transactions

Balance update + transaction record must succeed or fail together.

MongoDB sessions are mandatory for credit/debit.

Immutable Transaction Logs

Transactions are never updated or deleted.

Failures are logged as separate FAILED transactions.

Authorization First

Only authenticated users can access wallet or transaction APIs.

A user can only access their own wallet.

Read-Only History

Transaction history APIs are strictly read-only.

No edit, no delete.

Explicit Status Handling

Wallet status: ACTIVE / FROZEN

Frozen wallets cannot process transactions.