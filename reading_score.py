import math

class ReadingScore:
    def get_syllables_word_counts(self, text):
        syll = lambda w:len(''.join(c if c in"aeiouy"else' 'for c in w.rstrip('e')).split())

        sentences = text.split('.')
        n_sentences = 0
        n_words = 0
        n_syllables = 0

        for s in sentences:
            n_sentences += 1

            words = s.split(' ')
            n_words += len(words)
            for w in words:
                n_syllables += syll(w)

        avg_words = n_words / n_sentences
        avg_syllables = n_syllables / n_words

        return (avg_syllables, avg_words)

    def get_percent_hard_words(self, text):
        syll = lambda w:len(''.join(c if c in"aeiouy"else' 'for c in w.rstrip('e')).split())

        words = text.split(' ')
        n_hard_words = 0

        for w in words:
            if len(w) == 0:
                continue

            if w[0].isupper():
                continue

            if '-' in w:
                components = w.split('-')
                breakout = False
                for c in components:
                    if syll(c) < 3:
                        breakout = True
                        break
                if breakout:
                    continue

            if syll(w) >= 3:
                n_hard_words += 1

        return n_hard_words / len(words)

    def flesch(self, text):
        avg_syllables, avg_words = self.get_syllables_word_counts(text)
        return max(0, 206.835 - (1.015 * avg_words) - (84.6 * avg_syllables))

    def flesch_kinkade(self, text):
        avg_syllables, avg_words = self.get_syllables_word_counts(text)
        return max(0, (0.39 * avg_words) + (11.8 * avg_syllables) - 15.59)

    def fog(self, text):
        avg_syllables, avg_words = self.get_syllables_word_counts(text)
        pct_hard_words = self.get_percent_hard_words(text)
        return max(0, 0.4 * (avg_syllables + pct_hard_words))

    def smog(self, text):
        syll = lambda w:len(''.join(c if c in"aeiouy"else' 'for c in w.rstrip('e')).split())

        n_hard_words = 0
        sentences = text.split('.')
        n_sentences = len(sentences)
        beginning = sentences[0:min(n_sentences, 11)]
        middle = sentences[max((n_sentences / 2 - 5),0):min((n_sentences / 2 + 5), n_sentences)]
        end = sentences[max(0,n_sentences - 11):n_sentences - 1]

        merged = beginning + middle + end
        for s in merged:
            words = s.split(' ')
            for w in words:
                syllables = syll(w)
                if syllables >= 3:
                    n_hard_words += 1
        
        return max(0, 3 + (round(math.sqrt(n_hard_words) / 10) * 10))

    def coleman_liau(self, text):
        return 0

    def automated_readability(self, text):
        return 0

    def linsear_write(self, text):
        return 0

    def get_all(self, text):
        return self.flesch(text), self.flesch_kinkade(text), self.fog(text), self.smog(text), \
                self.coleman_liau(text), self.automated_readability(text), self.linsear_write(text)
