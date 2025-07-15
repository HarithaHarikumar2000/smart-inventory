import streamlit as st

if "inventory" not in st.session_state:
    st.session_state.inventory=[]
def add_product(product_id, name, quantity, price):
    st.session_state.inventory.append({
    "product_id":product_id,
    "name":name,
    "quantity":quantity,
    "price":price
    })
def find_product(product_id):
    for product in st.session_state.inventory:
        if product["product_id"]==product_id:
            return product
    return None
def update_quantity(product_id,change_quantity):
    product=find_product(product_id)
    if product:
        product["quantity"]+=change_quantity
        return True
    return False
def delete_product(product_id):
    new_inventory=[]
    for p in st.session_state.inventory:
        if p["product_id"]!=product_id:
            new_inventory.append(p)
    st.session_state.inventory=new_inventory
def search_products(products):
    results=[]
    for p in st.session_state.inventory:
        if products.lower() in p["name"].lower() or products.lower()==p["product_id"].lower():
            results.append(p)
    return results
st.title("Smart Inventory System")
menu=["Add Product","View Inventory","Update Quantity","Search Product","Delete Product"]

choice=st.sidebar.selectbox("Menu", menu)
if choice=="Add Product":
    st.subheader("Add New Product")
    product_id=st.text_input("Product ID")
    name=st.text_input("Product Name")
    quantity=st.number_input("Quantity", min_value=0, step=1)
    price=st.number_input("Price", min_value=0.0, step=0.01, format="%.2f")

    if st.button("Add Product"):
        if product_id and name:
            if find_product(product_id):
                st.warning("Product with this ID already exists!")
            else:
                add_product(product_id,name,quantity,price)
                st.success(f"Product '{name}' added successfully!")
        else:
            st.error("Please enter Product ID and Product Name.")
elif choice=="View Inventory":
    st.subheader("Inventory List")
    if st.session_state.inventory:
        for p in st.session_state.inventory:
            st.write(f"Product ID: {p['product_id']} | Name: {p['name']} | Quantity: {p['quantity']} | Price: ₹{p['price']:.2f}")
        total_value=0
        for p in st.session_state.inventory:
            total_value+=p["quantity"]*p["price"]
        st.markdown(f"**Total Inventory Value:** ₹{total_value:.2f}")
    else:
        st.info("Inventory is empty.")
elif choice=="Update Quantity":
    st.subheader("Update Product Quantity")
    product_id=st.text_input("Enter Product ID")
    qty_change=st.number_input("Enter Quantity  To Change", value=0, step=1)

    if st.button("Update"):
        if find_product(product_id):
            success=update_quantity(product_id, qty_change)
            if success:
                st.success("Quantity updated successfully.")
            else:
                st.error("Failed to update quantity.")
        else:
            st.error("Product not found.")
elif choice=="Search Product":
    st.subheader("Search Products")
    query=st.text_input("Enter Product ID or Name")
    if st.button("Search"):
        results=search_products(query)
        if results:
            for p in results:
                st.write(f"Product ID: {p['product_id']} | Name: {p['name']} | Quantity: {p['quantity']} | Price: ₹{p['price']:.2f}")
        else:
            st.warning("No matching products found.")
elif choice=="Delete Product":
    st.subheader("Delete Product")
    product_id=st.text_input("Enter Product ID to delete")
    if st.button("Delete"):
        if find_product(product_id):
            delete_product(product_id)
            st.warning(f"Product with ID '{product_id}' deleted.")
        else:
            st.error("Product not found.")

