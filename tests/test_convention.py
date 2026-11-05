from sqlmodel import SQLModel

import app.models  # noqa


def test_naming_convention():
    for table in SQLModel.metadata.tables.values():
        # Check table name is plural snake_case (basic check)
        assert table.name.islower() or '_' in table.name
        for col in table.columns:
            assert col.name.islower() or '_' in col.name
        for fk in table.foreign_keys:
            # FK column should end with _uuid
            assert fk.parent.name.endswith('_uuid'), f"{table.name}.{fk.parent.name}"
        # Every FK column should be indexed
        fk_cols = {fk.parent.name for fk in table.foreign_keys}
        indexed_cols = set()
        for idx in table.indexes:
            for c in idx.columns:
                indexed_cols.add(c.name)
        for fk_col in fk_cols:
            assert fk_col in indexed_cols, f"FK {table.name}.{fk_col} not indexed"
        # Every index named idx_* or uq_* (unique constraints)
        for idx in table.indexes:
            assert idx.name.startswith('idx_') or idx.name.startswith('uq_'), f"Index {idx.name} not named idx_* or uq_*"
