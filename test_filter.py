from subtitle_filter import SubtitleFilter


f = SubtitleFilter()


print(
    f.filter(
        "I did it. I did it. I did it."
    )
)


print(
    f.filter(
        "I did it. I did it."
    )
)