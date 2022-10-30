def decode(str):
    out=[]
    s=""
    for i in range(len(str)):
        a=str[i]
        if(a=='/' or a=='>'):
            if s!="" and s!=" ":
                out.append(s)
            break
        if(a==" " and str[i-1]!='='):
            if(s!=" "):

                out.append(s)
            s=""
        if(a!='<'):
            s+=a
        
    print(out)
    return out

print(decode("""<AddOrder book="book-2" operation="SELL" price="101.00" volume="87" orderId="9363" />"""))
# ['AddOrder', 'book="book-2"', 'operation="SELL"', 'price="101.00"', 'volume="87"', 'orderId="9363"']
# <DeleteOrder book="book-3" orderId="9036" />

def decode_list(l):
    if l[0]=='AddOrder':
        l[1]=l[1][6:len(l[1])-1]
        l[2]=l[2][11:len(l[2])-1]
        l[3]=float(l[3][7:len(l[3])-1])
        l[4]=int(l[4][8:len(l[4])-1])
        l[5]=int(l[5][9:len(l[5])-1])

    elif l[0]=='DeleteOrder':
        l[1]=l[1][6:len(l[1])-1]
        l[2]=int(l[2][9:len(l[2])-1])
    print(l)
    return l

print(decode_list(decode("""<Orders>""")))
print(decode_list(decode("""<DeleteOrder book="book-3" orderId="9036" />""")))
class Book:
    def __init__ (self,name):
        self.name=name
        self.buy_tup=[]
        self.sell_tup=[]
    def last(self,n):
        return n[0] 
    def add_buy(self,tup):
        self.buy_tup.append(tup)
        self.buy_tup=sorted(self.buy_tup,key=self.last,reverse=True)
    def add_sell(self,tup):
        self.sell_tup.append(tup)
        self.sell_tup=sorted(self.sell_tup,key=self.last,reverse=False)
    def pop_buy(self,n):
        self.buy_tup=self.buy_tup.pop(n)
    def pop_sell(self,n):
        self.sell_tup=self.sell_tup.pop(n)
    

def function(book_list,book,str):
    list=decode_list(decode(str))
    if(list[0]=='AddOrder'):
        temp_book=None
        if list[1] not in book_list:
            bookk=Book(list[1])
            book_list.append(list[1])
            book.append(bookk)
            temp_book=bookk
        else:
            for i in range(book):
                if book[i].name==list[1]:
                    temp_book=book[i]
                    break
        if list[2]=='SELL':
            temp_book.add_sell([list[3],list[4],list[5]])
        if list[2]=='BUY':
            temp_book.add_buy([list[3],list[4],list[5]])

        while( len(temp_book.buy_tup)!=0 and len(temp_book.sell_tup)!=0 and temp_book.buy_tup[0][0]>=temp_book.sell_tup[0][0]):
            if(temp_book.buy_tup[0][1]<temp_book.sell_tup[0][1]):
                temp_book.sell_tup[0][1]=temp_book.sell_tup[0][1]-temp_book.buy_tup[0][1]
                temp_book.pop_buy(0)
            if(temp_book.buy_tup[0][1]>temp_book.sell_tup[0][1]):
                temp_book.buy_tup[0][1]=temp_book.buy_tup[0][1]-temp_book.sell_tup[0][1]
                temp_book.pop_sell(0)
            if(temp_book.buy_tup[0][1]==temp_book.sell_tup[0][1]):
                temp_book.pop_buy(0)
                temp_book.pop_sell(0)
    if(list[0]=='DeleteOrder'):
        temp=None
        for i in range(book):
            if book[i].name==list[1]:
                temp=book[i]
                break
        for i in  range(temp.buy_tup):
            if temp.buy_tup[i][2]==list[2]:
                temp.pop_buy(i)
        for i in  range(temp.sell_tup):
            if temp.sell_tup[i][2]==list[2]:
                temp.pop_sell(i)
f = open("orders.xml", "r")
book=[]
book_list=[]
for x in f:
    print(x)
    
    function(book_list,book,x)

print(f.readline())
print(f.readline())
print(f.readline())
print(f.readline())
print(f.readline())
print(f.readline())
print(f.readline())
print(f.readline())

