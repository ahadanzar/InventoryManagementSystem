#*Basic Inventory Management System using json files*#
#Author : Ahad Anzar
#Date : 05/09/2021
#Please run the program in fullscreen mode for a better experience :)


import json
import datetime

def display(json, initial):    #Function that displays a json file in tabular form 
    numberofspaces=12
    space=" "*numberofspaces
    s=initial+space
    for i in json[min(json)]:
        s+=i+space
    print(s+"\n")
    def spacer(id, string):
        return str(json[id][string]) + ' '*(numberofspaces+len(string)-len(str(json[id][string])))
    for i in json:
        s=i+space+" "*(len(initial)-len(min(json)))
        for j in json[min(json)]:
            s+=spacer(i, j)
        print(s)

def inputverify(prompt, allowedvalues):       #This function loops the input prompt until an allowed value is entered
    x=0
    while not int(x) in allowedvalues:
        x=input(prompt) if x==0 else input("\nInvalid choice\n"+prompt)
    return x


def update(record, sales, repeat):          
    operation=int(inputverify("\n1)Update stock\n2)Add new product\n3)Review sales\n4)Go back\nChoose operation : ", (1, 2, 3, 4)))
    if operation==1:
        display(record, "ProductId")
        id = input("Enter product ID: ")
        try:
            record[id]['stock'] += int(input("Enter incoming stock : "))    #Incoming stock is added to existing stock
            display(record, "ProductId")
            print("Stock updated successfully!")
        except KeyError:
            print("Product doesn't exist")
    elif operation==2:
        try:         #The product id is automatically obtained. The remaining values have to be entered
            name=input("\nEnter name : ")
            mrp=int(input("Enter mrp : "))
            stock=int(input("Enter stock : "))
            discount=int(input("Enter discount percent : "))
            specifications=input("Enter specifications : ")
            record[str(int(max(record))+1)] = {'name':name, 'mrp':mrp, 'stock':stock, 'discount %':discount, 'specifications':specifications}
            print("Product added successfully")
        except ValueError:
            print("\nInvalid value entered")
    elif operation==3:       #Displays the current sales data, including income
        display(sales, "Sale Number")
        income=0
        for i in sales:
            if not sales[i]['amount payed']=='-':
                income+=int(sales[i]['amount payed'])
        print("Total income :", income)
        input("Press enter to continue")
    elif operation==4:      
        repeat=False 
    return repeat

def displayproduct(record, product):            #Display product details
    print("\nName : ", record[product]['name'])
    print("MRP : ", record[product]['mrp'], "Rs")
    print("Stock : ", record[product]['stock'])
    print("Discount : ", record[product]['discount %'], "%")
    print("Specifications : ", record[product]['specifications'], '\n')

def purchase(record, sales, cart):         #Function concerned with purchasing of a product
    display(record, "ProductId")
    print("Discounts only applies for orders more than 20 units")
    product = input("Enter the productID of the product you wish to purchase : ")
    try:
        displayproduct(record, product)
        q = int(input("Enter quantity: "))
        if q>record[product]['stock']:
            print(f"We are extremely sorry. The store only has {record[product]['stock']} units of {record[product]['name']}\nWhat is available has been added to cart")
            q=record[product]['stock']
        price=record[product]['mrp']*q
        print("Amount :", price)
        discount=0
        if(q>=20):
            discount = record[product]['discount %']*price/100
        print("Discount =", discount)
        cart.append({"ProductId":product, "name":record[product]['name'], "quantity":q, "price":price, "discount":discount, "amount payed":price-discount, "time":str(datetime.datetime.now())})
        p=int(inputverify("\n1) Continue purchase\n2) Proceed to billing\nChoose Operation :  ", (1, 2)))
        if p==1:return (True, cart)    #Runs the purchase function again 
        elif p==2:
            billing(record, sales, cart)      #Calls the billing function
            return (False, [])
          
    except KeyError:
        print("Invalid selection")

def billing(record, sales, products):       #Function to generate the bill
    bill, price={"0":{"Product":"-", "Quantity":"-", "Amount":"-"}}, 0
    print("------------------------------------------------------------------\nBILL :\n\n")
    for j, i in enumerate(products):
        bill.update({str(j+1):{"Product":i['name'], "Quantity":i['quantity'], "Amount":i['amount payed']}})
        price+=int(i['amount payed'])
        record[i["ProductId"]]['stock'] -= i['quantity']    #Reducing the stock in the inventory
        sales.update({str(int(max(sales))+1) : i})          #Updating sales data
    display(bill, "Sl.Number")
    print(f"******************************************************************\nAmount to pay : {price}\n------------------------------------------------------------------\n")
    input("Purchase Successful! Enter to go back to main menu") 

def load(jsonfile):     #Function to load the json file 
    try:
        with open(jsonfile, 'r') as f:
            txt=f.read()
            return json.loads(txt)
    except FileNotFoundError:
        print(f"{jsonfile} not found.\nPlease make sure the json files are placed in the same directory as the script file")
        exit()

def main():        #Main logic
    runstore=True
    record, sales = load('record.json'), load('sales.json')  #taking json file data as variables  
    operation = int(inputverify("\nWELCOME TO XYZ BAKERY!!\n\n1) Inventory and Sales\n2) Purchase Product\n3) Exit\nChoose Operation : ", (1, 2, 3)))
    repeat=True
    if operation==1:
        while repeat:
            repeat=update(record, sales, repeat)
    elif operation==2:
        products=[]
        while repeat:
            x = purchase(record, sales, products)
            repeat, products=x[0], x[1]
    elif operation==3:
        runstore = False       #Terminates the program after writing changes to the .json file
    with open('record.json', 'w') as f:
        f.write(json.dumps(record))
    with open('sales.json', 'w') as f:
        f.write(json.dumps(sales))
    return runstore

if __name__ == '__main__':
    run = True
    while run:
        run = main()
