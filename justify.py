class Solution:
    def justify_oneline(self, words, maxWidth):
        total_length = 0
        gap_num = len(words) - 1
        if gap_num == 0:
            return words[0].ljust(maxWidth)
        for w in words:
            total_length += len(w)
        remain_length = maxWidth - total_length - gap_num
        spaces = [ ' ' ] * gap_num
        while remain_length > 0:
            for s in range(gap_num):
                if remain_length == 0 :
                    break
                spaces[s] += ' '
                remain_length -= 1
        r = ''
        for i in range(gap_num):
            r +=words[i]
            r +=spaces[i]
        r += words[-1]
        return r
    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """
        lengths = []
        return_lines = []
        for w in words:
            lengths += [len(w)]
        i = 0
        while i < len(words):
            blank_line = []
            line_length = 0
            for j in range(i, len(words)):
                if j == i:
                    line_length += lengths[j]
                else:
                    line_length += lengths[j] + 1
                if line_length == maxWidth:
                    i = j + 1
                    blank_line += [words[j]]
                    return_lines += [(' ').join(blank_line)]
                    break
                elif line_length > maxWidth:
                    return_lines += [ self.justify_oneline(blank_line,maxWidth) ]
                    i = j
                    break
                blank_line += [words[j]]
                if j == len(words) - 1:
                    i = len(words)
                    last_line = ' '.join(blank_line)
                    extra_space = maxWidth - len(last_line)
                    last_line = last_line + ' ' * extra_space
                    return_lines += [last_line]
        return return_lines

if __name__ == '__main__':
    words = ["What","must","be","acknowledgment","shall","be"]
    w = 16
    s = Solution()
    r = s.fullJustify(words, w)
