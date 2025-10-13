"use client";

export default function AccountList({ accounts }: { accounts: any[] }) {
  if (!accounts.length) {
    return <p className="text-gray-500">No accounts found</p>;
  }

  return (
    <ul className="space-y-2">
      {accounts.map(acc => (
        <li key={acc.id} className="border p-3 rounded-md bg-gray-50">
          <b>{acc.name} {acc.surname}</b> — {acc.date} — 💰 {acc.balance}
        </li>
      ))}
    </ul>
  );
}
