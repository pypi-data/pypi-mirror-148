# local imports
from .entry import QueueEntry


class Adapter:

    def __init__(self, store, cache, translator):
        self.store = state_store
        self.cache = cache
        self.translator = translator


    def add(self, chain_spec, tx_hash, signed_tx):
        entry = QueueEntry(self.store, tx_hash) 
        tx = self.translator(chain_spec, signed_tx)
        entry.create(tx.nonce(), signed_tx)
        self.cache.put(chain_spec, tx)


    def get(self, chain_spec, tx_hash):
        entry = self.state_store.get(tx_hash)
        tx = self.translator(chain_spec, signed_tx)


    def upcoming(self, chain_spec):
        pass
