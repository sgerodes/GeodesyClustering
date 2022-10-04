from src.v2.enums import GeodeProjectionType as Gpt


projection_layout_1 = [
    [Gpt.SHARD, Gpt.BUD,],
    [Gpt.EMPTY, Gpt.SHARD,]
]
projection_layout_2 = [
    [Gpt.BUD, Gpt.BUD, Gpt.SHARD,],
    [Gpt.SHARD, Gpt.SHARD, Gpt.SHARD,],
    [Gpt.EMPTY, Gpt.EMPTY, Gpt.EMPTY,],
]
projection_layout_3 = [
    [Gpt.BUD, Gpt.SHARD, Gpt.SHARD, Gpt.BUD,],
    [Gpt.BUD, Gpt.SHARD, Gpt.SHARD, Gpt.BUD,],
    [Gpt.BUD, Gpt.SHARD, Gpt.SHARD, Gpt.BUD,],
]
projection_layout_4 = [
    [Gpt.EMPTY,     Gpt.EMPTY,  Gpt.EMPTY,  Gpt.EMPTY,  Gpt.EMPTY, ],
    [Gpt.EMPTY,     Gpt.BUD,    Gpt.BUD,    Gpt.SHARD,  Gpt.EMPTY, ],
    [Gpt.EMPTY,     Gpt.SHARD,  Gpt.SHARD,  Gpt.SHARD,  Gpt.EMPTY, ],
    [Gpt.EMPTY,     Gpt.EMPTY,  Gpt.EMPTY,  Gpt.EMPTY,  Gpt.EMPTY, ],
    [Gpt.EMPTY,     Gpt.EMPTY,  Gpt.EMPTY,  Gpt.EMPTY,  Gpt.EMPTY, ],
]
projection_layout_5 = [
    [Gpt.BUD, Gpt.SHARD,  Gpt.BUD, Gpt.SHARD, ],
    [Gpt.BUD, Gpt.SHARD,  Gpt.BUD, Gpt.SHARD, ],
    [Gpt.BUD, Gpt.SHARD,  Gpt.BUD, Gpt.SHARD, ],
]