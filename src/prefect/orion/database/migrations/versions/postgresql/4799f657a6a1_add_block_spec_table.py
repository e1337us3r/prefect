"""Add block_spec table

Revision ID: 4799f657a6a1
Revises: d9d98a9ebb6f
Create Date: 2022-02-20 10:38:44.972308

"""
import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "4799f657a6a1"
down_revision = "d9d98a9ebb6f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "block_spec",
        sa.Column(
            "id",
            prefect.orion.utilities.database.UUID(),
            server_default=sa.text("(GEN_RANDOM_UUID())"),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.orion.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.orion.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column(
            "fields",
            prefect.orion.utilities.database.JSON(astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_block_spec")),
    )
    with op.batch_alter_table("block_spec", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_block_spec__updated"), ["updated"], unique=False
        )
        batch_op.create_index(
            "uq_block_spec_name_version", ["name", "version"], unique=True
        )

    with op.batch_alter_table("block", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "block_spec_id", prefect.orion.utilities.database.UUID(), nullable=True
            )
        )
        batch_op.drop_index("ix_block_data__name")
        batch_op.drop_index("ix_block_data__updated")
        batch_op.create_index(
            batch_op.f("ix_block__block_spec_id"), ["block_spec_id"], unique=False
        )
        batch_op.create_index(batch_op.f("ix_block__name"), ["name"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_block__updated"), ["updated"], unique=False
        )
        batch_op.create_unique_constraint(batch_op.f("uq_block__name"), ["name"])
        batch_op.create_foreign_key(
            batch_op.f("fk_block__block_spec_id__block_spec"),
            "block_spec",
            ["block_spec_id"],
            ["id"],
            ondelete="cascade",
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("block", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_block__block_spec_id__block_spec"), type_="foreignkey"
        )
        batch_op.drop_constraint(batch_op.f("uq_block__name"), type_="unique")
        batch_op.drop_index(batch_op.f("ix_block__updated"))
        batch_op.drop_index(batch_op.f("ix_block__name"))
        batch_op.drop_index(batch_op.f("ix_block__block_spec_id"))
        batch_op.create_index("ix_block_data__updated", ["updated"], unique=False)
        batch_op.create_index("ix_block_data__name", ["name"], unique=False)
        batch_op.drop_column("block_spec_id")

    with op.batch_alter_table("block_spec", schema=None) as batch_op:
        batch_op.drop_index("uq_block_spec_name_version")
        batch_op.drop_index(batch_op.f("ix_block_spec__updated"))

    op.drop_table("block_spec")
    # ### end Alembic commands ###
