//! MemoryBackend trait for all storage backends.

use tlow_core::{TLOWError, RetrievalResult};
use serde_json::Value;

pub trait MemoryBackend: Send + Sync {
    fn backend_id(&self) -> &str;
    fn store(
        &self,
        content: &str,
        source: &str,
        metadata: Option<&Value>,
    ) -> Result<String, TLOWError>;
    fn retrieve(
        &self,
        query: &str,
        top_k: usize,
    ) -> Result<Vec<RetrievalResult>, TLOWError>;
    fn delete(&self, doc_id: &str) -> Result<bool, TLOWError>;
    fn clear(&self) -> Result<(), TLOWError>;
    fn count(&self) -> Result<usize, TLOWError>;
}
