class SubtitleFilter:

    def __init__(self):
        self.last_text = ""

    def remove_repeat_phrase(self, text):
        words = text.split()
        result = []
        i = 0

        while i < len(words):
            found = False

            for size in range(6, 0, -1):
                if i + size * 2 <= len(words):
                    part1 = words[i:i+size]
                    part2 = words[i+size:i+size*2]

                    if part1 == part2:
                        result.extend(part1)
                        i += size * 2
                        found = True
                        break

            if not found:
                result.append(words[i])
                i += 1

        return " ".join(result)

    def filter(self, text):
        if not text:
            return ""

        text = self.remove_repeat_phrase(text)

        if text == self.last_text:
            return ""

        self.last_text = text

        return text