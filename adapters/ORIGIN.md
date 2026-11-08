# Adapter sources

The official Claude adapter remains in the unmodified upstream tree. Local
adapters use cross-harness concepts from backnotprop/pstack at
`a6342ded43a2437e3c664b46c2cff103787773fd`. Its workflow policy changes and Windows
statechart patch are not imported.

The Python tools were retained from this library's earlier adaptation at
`07b86cb5d2db2cc691a0fe12c94457d13ba1c599`. They are optional host resources,
outside the official source.
