use futures::Future;
use std::collections::HashMap;
use tokio::sync::oneshot;
use uuid::Uuid;

/// A set of pending queries keyed by unique id, waiting to be responded to.
#[derive(Debug)]
pub struct Queries<Q, A> {
    pending: HashMap<Uuid, (Q, oneshot::Sender<A>)>,
}

impl<Q, A> Queries<Q, A> {
    /// Create a new empty set of pending queries.
    pub fn new() -> Self {
        Queries {
            pending: HashMap::new(),
        }
    }

    /// Create an unfulfilled request and return its id and the future which
    /// waits on its fulfillment.
    pub fn request(&mut self, query: Q) -> (Uuid, impl Future<Output = Option<A>>) {
        let id = Uuid::new_v4();
        let (sender, recv) = oneshot::channel();
        self.pending.insert(id, (query, sender));
        (id, async { recv.await.ok() })
    }

    /// Attempt to fulfill the request of the given id, returning the given
    /// response if there's an error sending it, or if there is no request with
    /// the specified id.
    pub fn respond(&mut self, id: Uuid, response: A) -> Result<Q, A> {
        if let Some((query, sender)) = self.pending.remove(&id) {
            sender.send(response)?;
            Ok(query)
        } else {
            Err(response)
        }
    }

    /// Get an iterator of all pending queries, paired with their ids.
    pub fn pending(&self) -> impl Iterator<Item = (&Uuid, &Q)> {
        self.pending.iter().map(|(id, (q, _))| (id, q))
    }

    /// Cancel a pending request, so that it will never be answered, and any
    /// future response will do nothing.
    pub fn cancel(&mut self, id: Uuid) {
        self.pending.remove(&id);
    }

    /// Test if the set of pending queries is empty.
    pub fn is_empty(&self) -> bool {
        self.pending.is_empty()
    }
}
