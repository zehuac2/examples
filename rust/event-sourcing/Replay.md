<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# In event sourcing design, after reboot, how would a service restore state from the event log? Is the entire event log iterated through or a pointer of some kind maintained?

In event sourcing, the way a service restores state after a reboot is
foundational to its design and efficiency. Here’s how it typically works:

- **Full Event Replay**: The canonical approach is to reconstruct the
  application's state by reading through the entire event log (often called the
  "event stream") for a particular aggregate or entity. Every event is replayed
  in the order it occurred, applying the changes step by step until the current
  state is reached[^1][^2][^3].
- **Snapshots for Efficiency**: Iterating through a very large event log every
  time would be inefficient as event streams grow. To address this, systems
  commonly implement **snapshots**. A snapshot is a record of the complete state
  of an aggregate at a specific point in time. When restoring after a reboot,
  the service first loads the latest snapshot and then only replays events that
  occurred after the snapshot was taken. This dramatically reduces recovery time
  without losing auditability or accuracy[^4][^5][^6][^7].
- **Pointers and Offsets**: Systems generally keep track of where the last
  snapshot was taken, either via metadata or an internal pointer—like a version
  number or event offset—so that when recovery is needed, the system knows from
  which point in the event stream to replay pending events[^8]. This pointer is
  typically stored separately (often in the same durable store as the events and
  snapshots).
- **Read and Write Models**: When using CQRS (Command Query Responsibility
  Segregation), the write model (aggregate) is always rebuilt from the sequence
  of past events before processing a new command, ensuring consistency[^1]. The
  read model, or projection, can similarly be rebuilt by replaying events,
  sometimes from snapshots for efficiency.

**Summary Table**

| Restoration Approach    | Description                                                                                 |
| :---------------------- | :------------------------------------------------------------------------------------------ |
| Full Event Replay       | Replays all events from the beginning to reconstruct current state.                         |
| Snapshot + Event Replay | Loads snapshot, then replays only the newer events to reach the current state.              |
| Use of Pointers/Offsets | Maintains a position in the event log to optimize where replay resumes after last snapshot. |

**Key Takeaways**

- **Full replay** is always possible, but can be slow for large logs.
- **Snapshotting** is a practical optimization for faster startup.
- **Pointers or version markers** ensure efficient, correct rehydration from the
  right spot in the event stream.

Most modern event-sourced systems combine these strategies—using event log
iteration for correctness and snapshotting with pointers for performance and
scalability[^4][^6][^5].

<div style="text-align: center">⁂</div>

[^1]:
    https://softwareengineering.stackexchange.com/questions/365455/recovering-the-state-of-the-write-service-in-an-event-sourced-system

[^2]: https://eventuous.dev/docs/read-models/rm-concept/
[^3]: https://github.com/eugene-khyst/ksqldb-event-souring
[^4]:
    https://www.geeksforgeeks.org/system-design/how-to-restore-state-in-an-event-based-message-driven-microservice-architecture-on-failure-scenario/

[^5]: http://eventsourcing.readthedocs.io/en/v5.0.0/topics/snapshotting.html
[^6]: https://www.kurrent.io/blog/snapshots-in-event-sourcing
[^7]:
    https://codeopinion.com/snapshots-in-event-sourcing-for-rehydrating-aggregates/

[^8]: https://docs.eventsourcingdb.io/fundamentals/snapshots/
[^9]:
    https://stackoverflow.com/questions/56406411/reconstruct-aggragate-state-from-given-point-in-time-using-cqrs-and-event-sourci

[^10]:
    https://www.reddit.com/r/softwarearchitecture/comments/1kpmsf8/i_dont_feel_that_auditability_is_the_most/

[^11]: https://stately.ai/docs/persistence
[^12]:
    https://dev.to/barryosull/event-sourcing-what-it-is-and-why-its-awesome/comments

[^13]:
    https://softwareengineering.stackexchange.com/questions/392863/event-sourcing-vs-event-logging-architecture-pattern

[^14]: https://pekko.apache.org/docs/pekko/1.0/typed/persistence.html
[^15]:
    https://www.couchbase.com/blog/event-sourcing-event-logging-an-essential-microservice-pattern/

[^16]: https://proto.actor/docs/bootcamp/unit-9/lesson-1/
[^17]:
    https://learn.microsoft.com/en-us/windows/win32/eventlog/querying-for-event-source-messages

[^18]:
    https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing

[^19]: https://news.ycombinator.com/item?id=19073734
[^20]:
    https://stackoverflow.com/questions/41698460/event-sourcing-incremental-int-id
