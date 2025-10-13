import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:2104"

def get_all_accounts():
    res = requests.get(f"{BACKEND_URL}/accounts/show_accounts/")
    if res.status_code == 200:
        return res.json()
    return {"error": f"Backend returned {res.status_code}"}

def create_account(name, surname, date, balance):
    info = {"name": name, "surname": surname, "date": date, "balance": balance}
    res = requests.post(f"{BACKEND_URL}/accounts/", json=info)
    if res.status_code == 200:
        gr.Info("✅ Account created successfully!")
        return res.json()
    else:
        gr.Warning(f"⚠️ Failed to create account: {res.status_code}")
        return {"error": f"Backend returned {res.status_code}"}

def search_account(item):
    res = requests.get(f"{BACKEND_URL}/accounts/search/{item}")
    if res.status_code == 200:
        if res.json():
            gr.Info(f"✅ Found {len(res.json())} accounts")
        else:
            gr.Warning("🔍 No accounts found")
        return res.json()
    gr.Error("❌ Failed to fetch data from backend")
    return {"error": f"Backend returned {res.status_code}"}

def delete_account(account):
    res = requests.delete(f"{BACKEND_URL}/accounts/delete/{account}")
    if res.status_code == 200:
        gr.Info("✅ Account deleted successfully!")  # ✅ Toast повідомлення
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


        create_btn.click(search_account, inputs=[item_inp], outputs=output_js)

    with gr.Tab("Delete Account"):
        account = gr.Textbox(label="Account to delete")
        create_btn = gr.Button(label="Delete Account")
        output_js = gr.JSON(label="Other Accounts")

        create_btn.click(delete_account, inputs=[account], outputs=output_js)
demo.launch()