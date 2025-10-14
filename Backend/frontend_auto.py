import gradio as gr
import requests
from uuid import uuid4

BACKEND_URL = "http://127.0.0.1:3121/accounts"

def get_all_accounts():
    res = requests.get(f"{BACKEND_URL}/show_accounts")
    if res.status_code == 200:
        return res.json()
    return {"error": f"Backend returned {res.status_code}"}

def create_account(name, surname, date, balance):
    info = {"name": name, "surname": surname, "date": date, "balance": balance}
    res = requests.post(f"{BACKEND_URL}/", json=info)
    if res.status_code == 200:
        gr.Info("✅ Account created successfully!")
        return res.json()
    else:
        gr.Warning(f"⚠️ Failed to create account: {res.status_code}")
        return {"error": f"Backend returned {res.status_code}"}

def search_account(item):
    res = requests.get(f"{BACKEND_URL}/search/{item}")
    if res.status_code == 200:
        data = res.json()
        if data:
            gr.Info(f"✅ Found {len(data)} accounts")
        else:
            gr.Warning("🔍 No accounts found")
        return data
    gr.Error("❌ Failed to fetch data from backend")
    return {"error": f"Backend returned {res.status_code}"}

def change_account(account_id, name, surname, date, balance):
    info = {"name": name, "surname": surname, "date": date, "balance": balance}
    res = requests.put(f"{BACKEND_URL}/change_all_danes/{account_id}", json=info)
    if res.status_code == 200:
        gr.Info("✅ Data changed successfully!")
        return res.json()
    elif res.status_code == 404:
        gr.Warning("🔍 No account found with this ID")
        return {"error": "Account not found"}
    else:
        gr.Error(f"❌ Backend error: {res.status_code}")
        return {"error": f"Backend returned {res.status_code}"}

def delete_account(account_id):
    res = requests.delete(f"{BACKEND_URL}/delete/{account_id}")
    if res.status_code == 200:
        gr.Info("✅ Account deleted successfully!")
        return res.json()
    else:
        gr.Warning(f"⚠️ Failed to delete account: {res.status_code}")
        return {"error": f"Backend returned {res.status_code}"}

with gr.Blocks(title="Bank Demo") as demo:
    gr.Markdown("# 💳 Bank Account Manager")

    with gr.Tab("All Accounts"):
        btn = gr.Button("Update all accounts")
        output = gr.JSON(label="All accounts")
        btn.click(get_all_accounts, outputs=output)

    with gr.Tab("Create Account"):
        name_inp = gr.Textbox(label="Name")
        surname_inp = gr.Textbox(label="Surname")
        date_inp = gr.Textbox(label="Date")
        balance_inp = gr.Number(label="Balance")
        create_btn = gr.Button("Create Account")
        output_js = gr.JSON(label="Created Account")
        create_btn.click(create_account,
                         inputs=[name_inp, surname_inp, date_inp, balance_inp],
                         outputs=output_js)

    with gr.Tab("Search Account"):
        item_inp = gr.Textbox(label="Search query")
        search_btn = gr.Button("Search Account")
        search_out = gr.JSON(label="Search Results")
        search_btn.click(search_account, inputs=item_inp, outputs=search_out)

    with gr.Tab("Delete Account"):
        account = gr.Textbox(label="Account to delete")
        del_btn = gr.Button("Delete Account")
        del_out = gr.JSON(label="Other Accounts")
        del_btn.click(delete_account, inputs=[account], outputs=del_out)

    with gr.Tab("Change Account"):
        account = gr.Textbox(label="Account to change")
        name_inp = gr.Textbox(label="Name")
        surname_inp = gr.Textbox(label="Surname")
        date_inp = gr.Textbox(label="Date")
        balance_inp = gr.Number(label="Balance")
        change_btn = gr.Button("Change Account")
        change_out = gr.JSON(label="Other Accounts")
        change_btn.click(change_account, inputs=[account, name_inp, surname_inp, date_inp, balance_inp], outputs=change_out)

demo.launch()
