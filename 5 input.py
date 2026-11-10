def add_item_buggy(item, order=[]):
    order.append(item)
    return order

def add_item(item, order=None):
    if order is None:           # new list for every call that does not supply one
        order = []
    order.append(item)
    return order

print(add_item_buggy("Tea"), add_item_buggy("Vada"))
print(add_item("Tea"), add_item("Vada"))
print("add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)

# ---------- Test with three customers in sequence ----------
print("\n--- Three customers (fixed design) ---")
for customer, items in enumerate([["Tea", "Vada"], ["Coffee"], ["Dosa", "Tea", "Idli"]], start=1):
    order = None
    for it in items:
        order = add_item(it, order)
    print(f"Customer {customer}: {order}")

# ---------- Positional, keyword and default parameters; returning two values ----------
PRICES = {"Tea": 15, "Vada": 10, "Coffee": 20, "Dosa": 50, "Idli": 30}

def bill(order, gst_rate=0.05, discount=0):
    total = sum(PRICES[i] for i in order) - discount
    gst = round(total * gst_rate, 2)
    return total, gst                       # returns a tuple of two values

total, gst = bill(["Dosa", "Tea"])                          # positional + default gst_rate
print("\nbill(['Dosa','Tea'])                        ->", bill(["Dosa", "Tea"]))
print("bill(['Dosa','Tea'], discount=5)          ->", bill(["Dosa", "Tea"], discount=5))
print("bill(['Dosa','Tea'], gst_rate=0.12)       ->", bill(["Dosa", "Tea"], gst_rate=0.12))

# ---------- local, global, nonlocal ----------
counter = 0                                 # global name

def wrong_increment():
    try:
        counter = counter + 1               # Python sees 'counter' as LOCAL here
    except UnboundLocalError as err:
        print("\nwrong_increment ->", type(err).__name__, ":", err)

def global_increment():
    global counter                          # needed to REBIND a global name
    counter += 1

wrong_increment(); global_increment(); global_increment()
print("counter after two global_increment() calls =", counter)

def make_order_counter():
    count = 0                               # enclosing (non-local) name
    def add_one():
        nonlocal count                      # rebinds the enclosing variable
        count += 1
        return count
    return add_one

tick = make_order_counter()
print("nonlocal counter:", tick(), tick(), tick())

# ---------- Alternative 1: caller always passes the list ----------
def add_item_explicit(item, order):
    order.append(item)
    return order

# ---------- Alternative 2: closure keeps the order ----------
def new_order():
    order = []
    def add(item):
        order.append(item)
        return list(order)                  # a copy is returned
    return add

c1, c2 = new_order(), new_order()
print("\nclosure customer 1:", c1("Tea"), c1("Vada"))
print("closure customer 2:", c2("Coffee"))
