## Level 1: Offline-First Architecture

### Q1. How do you design an Offline-First News App?

**Pattern**: "Database as Source of Truth".

1.  **Read Path**: UI always observes Database (Room/SQLite). Never observes Network directly.
2.  **Write Path**:
    - Network -> Fetch Data -> Write to DB -> UI Updates (via Flow/LiveData).
3.  **Error Handling**: If Network fails, DB still has old data. UI shows "Offline" snackbar.

### Q2. How to handle conflicting edits (Conflict Resolution)?

**Scenario**: User edits a note Offline. Server has a newer version.
**Strategies**:

1.  **Last Write Wins (LWW)**: Simple, based on Timestamp. Prone to data loss.
2.  **Manual Merge**: Show user both versions ("Keep yours" vs "Take Server's").
3.  **Conflict-free Replicated Data Types (CRDTs)**: Advanced math to automatic merge.
4.  **Operational Transformation (OT)**: Google Docs style.
