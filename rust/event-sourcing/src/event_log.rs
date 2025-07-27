pub struct EventLog<E, S> {
    events: Vec<E>,
    snapshots: Vec<S>,
}

impl<E, S> EventLog<E, S> {
    pub fn new() -> Self {
        EventLog {
            events: Vec::new(),
            snapshots: Vec::new(),
        }
    }
}
