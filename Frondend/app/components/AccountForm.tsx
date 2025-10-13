"use client";

import { useState } from "react";

export default function AccountForm({ onCreated }: { onCreated: () => void }) {
  const [form, setForm] = useState({
    name: "",
    surname: "",
    date: "",
    balance: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:2104/accounts/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          balance: parseFloat(form.balance),
        }),
      });

      if (!res.ok) throw new Error("Failed to create account");
      onCreated();
      setForm({ name: "", surname: "", date: "", balance: "" });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 items-end">
      <input name="name" value={form.name} onChange={handleChange} placeholder="Name" className="border p-2 rounded-md" required />
      <input name="surname" value={form.surname} onChange={handleChange} placeholder="Surname" className="border p-2 rounded-md" required />
      <input name="date" value={form.date} onChange={handleChange} placeholder="YYYY-MM-DD" className="border p-2 rounded-md" required />
      <input name="balance" value={form.balance} onChange={handleChange} placeholder="Balance" className="border p-2 rounded-md" required />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded-md">Add</button>
    </form>
  );
}
