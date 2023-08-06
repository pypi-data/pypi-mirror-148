# ������� �� ���������� � ����� ������� ���������
# ���������:
#   Number : int -> ����� ������� ����� ���������
#   Notation : int -> ������� � ������� ����� ���������
# ������������ ��������
#   ����� ������� ���������� ����� ��������
def from_decimal(Number : int, Notation : int) -> int:
    Buffer = 0
    BufferNumber = Number
    while BufferNumber > 0:
        Buffer = Buffer * 10 + (BufferNumber % Notation)
        BufferNumber //= Notation
    return int(str(Buffer)[::-1])

# ������� �� �������� � ����� ������� ���������
# ���������:
#   Number : int -> ����� ������� ����� ���������
#   Notation : int -> ������� � ������� ����� ���������
# ������������ ��������
#   ����� ������� ���������� ����� ��������
def from_binary(Number : int, Notation : int) -> int:
    Buffer = 0
    for i in range(len(str(Number))):
        Buffer += (int(str(Number)[i]) * 2 ** (len(str(Number)) - 1 - i))
    if Notation != 10:
        return from_decimal(Buffer, Notation)
    return Buffer

# ��������� ������� ����� 4
# ���������:
#   Number : int -> ����� ������� ����� ��������
# ������������ ��������
#   ����� � ���������� ������� ����� ���������� ��������������
def mcko_question_4(Number : int) -> int:
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