from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection
from algorithm import bubble_sort, selection_sort, linear_search

app = Flask(__name__)

def fetch_all_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory;")
    rows = cur.fetchall()
    
    # Convert SQLite Row objects into standard Python dictionaries
    records = [dict(row) for row in rows]
    
    cur.close()
    conn.close()
    return records

@app.route('/', methods=['GET', 'POST'])
def index():
    records = fetch_all_from_db()
    
    if request.method == 'POST':
        # --- HANDLING SORT ROUTE ---
        if 'sort_submit' in request.form:
            algo = request.form.get('sort_algo')
            column = request.form.get('sort_column')
            order = request.form.get('sort_order')
            
            is_reverse = True if order == 'desc' else False
            
            if algo == 'bubble':
                records = bubble_sort(records, column, reverse=is_reverse)
            elif algo == 'selection':
                records = selection_sort(records, column, reverse=is_reverse)
                
        # --- HANDLING SEARCH ROUTE ---
        elif 'search_submit' in request.form:
            column = request.form.get('search_column')
            search_term = request.form.get('search_term')
            
            records = linear_search(records, column, search_term)

    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add_record():
    # 1. Grab the values using the exact 'name' attributes from your HTML form
    name = request.form.get('item_name')
    price = request.form.get('price')
    date_received = request.form.get('date_received')
    is_fragile = request.form.get('is_fragile')
    
    # Quick server-side validation to make sure fields aren't completely empty
    if not name or not price or not date_received:
        return "Error: Missing required form fields!", 400

    try:
        # Convert types safely for SQLite
        price_float = float(price)
        # Save boolean as 1 (True) or 0 (False) for SQLite compatibility
        is_fragile_int = 1 if is_fragile == 'true' else 0
        
        # 2. Connect to the local database file
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 3. Use '?' placeholders for SQLite execution
        cur.execute("""
            INSERT INTO inventory (item_name, price, date_received, is_fragile)
            VALUES (?, ?, ?, ?);
        """, (name, price_float, date_received, is_fragile_int))
        
        # CRITICAL STEP: Commit the transaction so it physically saves to 'my_dataBase.db'
        conn.commit()
        
    except Exception as e:
        print(f"Database insertion error: {e}")
    finally:
        cur.close()
        conn.close()
        
    # 4. Refresh the home page to display the newly added record instantly
    return redirect(url_for('index'))
if __name__ == '__main__':
    #Configured to accept production networking routing 
    app.run(host='0.0.0.0',port=50000)
    
