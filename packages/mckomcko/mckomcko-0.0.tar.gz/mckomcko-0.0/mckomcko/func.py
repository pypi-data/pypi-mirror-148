def mcko_question_10(a: str) -> int:
    res = []
    num = 0
    s = a.split()
    for i in range(len(s)):
        if s[i] in '–+':
            res.append(s[i])
        else:
            t = s[i].split('**')
            r = int(t[0]) ** int(t[1])
            res.append(r)
    if res[1] == '+':
        num += (int(res[0]) + int(res[2]))
    elif res[1] == '–':
        num += (int(res[0]) - int(res[2]))
    if res[3] == '+':
        num += int(res[4])
    elif res[3] == '–':
        num -= int(res[4])

    b = ''
    while num > 0:
        b = str(num % 4) + b
        num = num // 4

    max_item = lambda s: max(t := {i: s.count(i) for i in s}, key=t.get)

    return max_item(b)


def mcko_question_4(Number: int) -> int:
    Counter = 0
    while 1:
        Buffer = 0

        if Counter % 2 == 0:
            Buffer = from_decimal(Counter, 2) * 100 + 10
        else:
            Buffer = from_decimal(Counter, 2) * 100 + 11

        if str(Buffer).count('1') % 2 == 0:
            Buffer = Buffer * 10
        else:
            Buffer = Buffer * 10 + 1

        if from_binary(Buffer, 10) > Number:
            return from_binary(Counter, 10)

        Counter += 1



def from_decimal(Number: int, Notation: int) -> int:
    Buffer = 0
    BufferNumber = Number
    while BufferNumber > 0:
        Buffer = Buffer * 10 + (BufferNumber % Notation)
        BufferNumber //= Notation
    return int(str(Buffer)[::-1])


def from_binary(Number: int, Notation: int) -> int:
    Buffer = 0
    for i in range(len(str(Number))):
        Buffer += (int(str(Number)[i]) * 2 ** (len(str(Number)) - 1 - i))
    if Notation != 10:
        return from_decimal(Buffer, Notation)
    return Buffer
