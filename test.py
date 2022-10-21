
import time


string = 'test.txt'

print(string[:string.find('.')])

def test(x=1):
    while True:
        yield x
        x += 1


gene = test()
print(type(gene))

for i in gene:

    print(i)
    time.sleep(1)