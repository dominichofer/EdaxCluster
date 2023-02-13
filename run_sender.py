from workspread import TaskDispatchClient


def on_report(index: int, result: str):
    print(index, result)


if __name__ == '__main__':
    #ip = sys.argv[1]
    ip = 'localhost'

    client = TaskDispatchClient(ip)

    task = [
        ('O--OOOOX-OOOOOOXOOXXOOOXOOXOOOXXOOOOOOXX---OOOOX----O--X-------- X', 60),
        ('-OOOOO----OOOOX--OOOOOO-XXXXXOO--XXOOX--OOXOXX----OXXO---OOO--O- X', 60),
        ('--OOO-------XX-OOOOOOXOO-OOOOXOOX-OOOXXO---OOXOO---OOOXO--OOOO-- X', 60),
        ('--XXXXX---XXXX---OOOXX---OOXXXX--OOXXXO-OOOOXOO----XOX----XXXXX- O', 60),
        ('--O-X-O---O-XO-O-OOXXXOOOOOOXXXOOOOOXX--XXOOXO----XXXX-----XXX-- O', 60),
        ('---XXXX-X-XXXO--XXOXOO--XXXOXO--XXOXXO---OXXXOO-O-OOOO------OO-- X', 60),
        ('---XXX----OOOX----OOOXX--OOOOXXX--OOOOXX--OXOXXX--XXOO---XXXX-O- X', 60),
        ('-OOOOO----OOOO---OOOOX--XXXXXX---OXOOX--OOOXOX----OOXX----XXXX-- O', 60),
        ('-----X--X-XXX---XXXXOO--XOXOOXX-XOOXXX--XOOXX-----OOOX---XXXXXX- O', 60),
        ('--OX-O----XXOO--OOOOOXX-OOOOOX--OOOXOXX-OOOOXX-----OOX----X-O--- X', 60),
        ('----X-----XXX----OOOXOOO-OOOXOOO-OXOXOXO-OOXXOOO--OOXO----O--O-- X', 60),
        ('----O-X------X-----XXXO-OXXXXXOO-XXOOXOOXXOXXXOO--OOOO-O----OO-- O', 60),
        ('---X-------OX--X--XOOXXXXXXOXXXXXXXOOXXXXXXOOOXX--XO---X-------- O', 60),
        ('----OO-----OOO---XXXXOOO--XXOOXO-XXXXXOO--OOOXOO--X-OX-O-----X-- X', 60),
        ('--OOO---XXOO----XXXXOOOOXXXXOX--XXXOXX--XXOOO------OOO-----O---- X', 60),
        ('--------X-X------XXXXOOOOOXOXX--OOOXXXX-OOXXXX--O-OOOX-----OO--- O', 60),
        ('--XXXXX---XXXX---OOOXX---OOXOX---OXXXXX-OOOOOXO----OXX---------- O', 60),
        ('-------------------XXOOO--XXXOOO--XXOXOO-OOOXXXO--OXOO-O-OOOOO-- X', 60),
        ('--XOOO----OOO----OOOXOO--OOOOXO--OXOXXX-OOXXXX----X-XX---------- X', 60),
        ('-----------------------O--OOOOO---OOOOOXOOOOXXXX--XXOOXX--XX-O-X X', 60),
        ]

    results = client.dispatch(task, on_report)
    print(results)
