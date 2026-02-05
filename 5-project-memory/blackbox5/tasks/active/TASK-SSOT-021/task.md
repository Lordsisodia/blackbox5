# TASK-SSOT-021: Implement StorageBackend Abstract Base Class

**Status:** pending
**Priority:** HIGH
**Created:** 2026-02-06
**Parent:** Issue #3 - Missing Storage Abstraction Layer

## Objective
Create the foundation StorageBackend ABC with YAMLStorage and JSONStorage implementations.

## Success Criteria
- [ ] Create `storage/base.py` with StorageBackend ABC
- [ ] Create `storage/file_storage.py` with YAMLStorage class
- [ ] Create `storage/file_storage.py` with JSONStorage class
- [ ] Implement atomic write operations (temp file + rename)
- [ ] Add proper error handling
- [ ] Create `storage/factory.py` with StorageFactory
- [ ] Write unit tests

## Context
35+ files currently use raw yaml.safe_load()/json.load(). This creates:
- Code duplication
- Inconsistent error handling (~30% have no try/except)
- No atomic writes (corruption risk)
- Hard to test

## Design
```python
class StorageBackend(ABC):
    @abstractmethod
    def load(self, path: Path) -> Dict[str, Any]
    @abstractmethod
    def save(self, path: Path, data: Dict[str, Any]) -> None
    @abstractmethod
    def exists(self, path: Path) -> bool
    @abstractmethod
    def delete(self, path: Path) -> bool
```

## Related Files
- All 35+ files identified in storage-pattern-inventory.md
- scout-abstraction-layers.md

## Rollback Strategy
Keep existing code paths until migration verified.
