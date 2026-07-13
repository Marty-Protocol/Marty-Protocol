from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claim_blocker_is_strongly_typed_in_all_generated_bindings() -> None:
    python = (ROOT / "reference/python/mip_types/models.py").read_text(encoding="utf-8")
    rust = (ROOT / "reference/rust/src/models.rs").read_text(encoding="utf-8")
    typescript = (ROOT / "reference/typescript/src/models.ts").read_text(encoding="utf-8")

    assert "class ClaimBlocker(BaseModel):" in python
    assert "owner: ClaimBlockerOwner" in python
    assert "claim_blocker: ClaimBlocker | None = None" in python

    assert "pub struct ClaimBlocker {" in rust
    assert "pub owner: ClaimBlockerOwner," in rust
    assert "pub claim_blocker: Option<ClaimBlocker>," in rust

    assert "export interface ClaimBlocker {" in typescript
    assert "owner: ClaimBlockerOwner;" in typescript
    assert "claim_blocker?: ClaimBlocker | null;" in typescript
