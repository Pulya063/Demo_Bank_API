"use client";

import { useEffect, useState } from "react";
import AccountList from "./components/AccountList";
import AccountForm from "./components/AccountForm";
import SearchBar from "./components/SearchBar";

export default function Page() {
  const [accounts, setAccounts] = useState<any[]>([]);

  const fetchAccounts = async () => {
    try {
      const res = await fetch("http://127.0.0.1:2104/accounts/");
      const data = await res.json();
      setAccounts(data);
    } catch (e) {
      console.error("Error fetching accounts:", e);
    }
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-3xl font-bold">💳 Bank Account Manager</h1>

      <AccountForm onCreated={fetchAccounts} />
      <SearchBar onSearch={setAccounts} />
      <AccountList accounts={accounts} />
    </main>
  );
}
